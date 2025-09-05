import argparse
import time
import json
import os
import csv
import sys
import select
import tty
import termios
from datetime import datetime, timedelta
from collections import defaultdict
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.live import Live
from rich.console import Console, Group
from rich.layout import Layout
from rich.table import Table
from rich.text import Text

console = Console()

CONFIG_FILE = 'config.json'
LOG_FILE = 'productivity_log.csv'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {'interval': 60}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def parse_duration(duration_str):
    try:
        # Handle cases with days (e.g., "1 day, 0:00:00")
        if ',' in duration_str:
            days_str, time_str = duration_str.split(', ')
            days = int(days_str.split()[0])
        else:
            days = 0
            time_str = duration_str

        # Handle microseconds by splitting at the dot
        if '.' in time_str:
            time_str = time_str.split('.')[0]

        parts = list(map(int, time_str.split(':')))
        return timedelta(days=days, hours=parts[0], minutes=parts[1], seconds=parts[2])
    except (ValueError, IndexError):
        return timedelta()

def get_historical_time(project, task):
    if not os.path.isfile(LOG_FILE):
        return "0:00:00"
    total_duration = timedelta()
    with open(LOG_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                if row['Project'] == project and row['Task'] == task:
                    total_duration += parse_duration(row['Duration'])
        except KeyError:
            console.print(f"[bold red]Warning:[/bold red] The log file '{LOG_FILE}' has an outdated format. Please delete it to start a new log.")
            return "0:00:00"
    return str(total_duration)

def log_session(project, task, start_time, end_time):
    duration = end_time - start_time
    if duration.total_seconds() < 1:
        return

    fieldnames = ['Date', 'Project', 'Task', 'Start Time', 'End Time', 'Duration']
    
    log_entry = {
        'Date': start_time.strftime('%Y-%m-%d'),
        'Project': project,
        'Task': task,
        'Start Time': start_time.strftime('%H:%M:%S'),
        'End Time': end_time.strftime('%H:%M:%S'),
        'Duration': str(duration)
    }

    file_exists = os.path.isfile(LOG_FILE)
    if file_exists:
        with open(LOG_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != fieldnames:
                # If header doesn't match, assume old format or corrupted, and rewrite
                # For simplicity, we'll just create a new file with the correct header
                # In a real app, you might want to migrate data or warn the user.
                file_exists = False # Force rewrite

    with open(LOG_FILE, 'a' if file_exists else 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

def generate_summary_report():
    if not os.path.isfile(LOG_FILE):
        console.print(f"[yellow]Log file '{LOG_FILE}' not found.[/yellow]")
        return

    project_times = defaultdict(timedelta)
    with open(LOG_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                project_times[row['Project']] += parse_duration(row['Duration'])
        except KeyError:
            console.print(f"[bold red]Warning:[/bold red] The log file '{LOG_FILE}' has an outdated format. Please delete it to start a new log.")
            return

    if not project_times:
        console.print("[yellow]No data found in log file.[/yellow]")
        return

    grand_total_time = sum(project_times.values(), timedelta())

    table = Table()
    table.add_column("Project", style="magenta")
    table.add_column("Total Time Spent", style="green")
    table.add_column("Percentage of Total", style="blue")

    for project, total_time in sorted(project_times.items()):
        if grand_total_time.total_seconds() > 0:
            percentage = (total_time.total_seconds() / grand_total_time.total_seconds()) * 100
        else:
            percentage = 0
        table.add_row(project, str(total_time), f"{percentage:.2f}%")
    
    console.print("Overall Productivity Summary")
    console.print(table)
    console.print(f"[bold]Grand total time for all projects:[/bold] {grand_total_time}")

def generate_project_report(project_name):
    if not os.path.isfile(LOG_FILE):
        console.print(f"[yellow]Log file '{LOG_FILE}' not found.[/yellow]")
        return

    task_times = defaultdict(timedelta)
    with open(LOG_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                if row.get('Project') == project_name:
                    task_times[row['Task']] += parse_duration(row['Duration'])
        except KeyError:
            console.print(f"[bold red]Warning:[/bold red] The log file '{LOG_FILE}' has an outdated format. Please delete it to start a new log.")
            return

    if not task_times:
        console.print(f"[yellow]No data found for project '{project_name}'.[/yellow]")
        return

    total_project_time = sum(task_times.values(), timedelta())

    table = Table()
    table.add_column("Task", style="magenta")
    table.add_column("Time Spent", style="green")
    table.add_column("Percentage", style="blue")

    for task, total_time in sorted(task_times.items()):
        if total_project_time.total_seconds() > 0:
            percentage = (total_time.total_seconds() / total_project_time.total_seconds()) * 100
        else:
            percentage = 0
        table.add_row(task, str(total_time), f"{percentage:.2f}%")
    
    console.print(f"Productivity Report for Project: [bold cyan]{project_name}[/bold cyan]")
    console.print(table)
    console.print(f"[bold]Total time for project '{project_name}':[/bold] {total_project_time}")

def run_timer(project_name, task, interval_minutes):
    seconds = 0
    color_index = 0
    block_count = 1
    colors = ['blue', 'green', 'yellow', 'red']
    interval_seconds = interval_minutes * 60
    paused = False

    historical_time = get_historical_time(project_name, task)

    layout = Layout()
    layout.split(Layout(name="main"), Layout(name="footer", size=1))
    footer_text = Text("Enter:pause/resume. Ctrl+C:save and exit.", justify="center", style="dim")
    layout["footer"].update(footer_text)

    old_settings = termios.tcgetattr(sys.stdin)
    start_time = datetime.now()
    try:
        tty.setcbreak(sys.stdin.fileno())
        with Live(layout, screen=True, redirect_stderr=False, auto_refresh=False) as live:
            while True:
                current_color = colors[color_index % len(colors)]
                
                header_text = f"[bold]Project:[/bold] {project_name}\n[bold]Task:[/bold] {task}\n[bold]Previously Logged:[/bold] {historical_time}"
                header_panel = Panel(header_text, title="Productivity Timer", border_style="magenta")
                block_text = Text(f"Block {block_count} of {interval_minutes} minutes.", justify="center", style="cyan bold")
                progress = Progress(
                    TextColumn(f"[bold {current_color}]" + "Total Time: {task.fields[timer_display]}"),
                    BarColumn(bar_width=None, style=current_color),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                )
                
                task_id = progress.add_task("interval_progress", total=interval_seconds, timer_display="00:00:00")
                main_content = Group(header_panel, block_text, progress)
                layout["main"].update(main_content)
                live.refresh()

                for i in range(interval_seconds):
                    if select.select([sys.stdin], [], [], 0)[0]:
                        key = sys.stdin.read(1)
                        if key == '\n':
                            paused = not paused

                    if paused:
                        pause_text = Text("PAUSED", justify="center", style="yellow")
                        paused_content = Group(header_panel, block_text, progress, pause_text)
                        layout["main"].update(paused_content)
                        live.refresh()
                        while paused:
                            if select.select([sys.stdin], [], [], 0.1)[0]:
                                key = sys.stdin.read(1)
                                if key == '\n':
                                    paused = False
                        continue

                    mins, secs = divmod(seconds, 60)
                    hours, mins = divmod(mins, 60)
                    timer_display = f'{hours:02d}:{mins:02d}:{secs:02d}'
                    progress.update(task_id, advance=1, timer_display=timer_display)
                    
                    main_content = Group(header_panel, block_text, progress)
                    layout["main"].update(main_content)
                    live.refresh()
                    
                    time.sleep(1)
                    seconds += 1
                
                color_index += 1
                block_count += 1

    except KeyboardInterrupt:
        pass
    finally:
        end_time = datetime.now()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        log_session(project_name, task, start_time, end_time)
        print("\nTimer stopped.")
        duration_str = str(timedelta(seconds=int(seconds)))
        print(f"Total time spent this session: {duration_str}")

def main():
    parser = argparse.ArgumentParser(description='A productivity timer with reporting features.')
    parser.add_argument('project_name', type=str, nargs='?', help='The name of the project.')
    parser.add_argument('task', type=str, nargs='?', help='The description of the task.')
    parser.add_argument('--set-interval', type=int, metavar='MINUTES', help='Set the default timer interval in minutes for future runs.')
    parser.add_argument('--interval', type=int, metavar='MINUTES', help='Override the default interval for this run.')
    parser.add_argument('--report', nargs='?', const='_ALL_PROJECTS_', default=None, help='Generate a report. Provide a project name for a detailed report, or no name for a summary.')

    args = parser.parse_args()
    
    if args.report is not None:
        if args.report == '_ALL_PROJECTS_':
            generate_summary_report()
        else:
            generate_project_report(args.report)
        return

    config = load_config()

    if args.set_interval is not None:
        config['interval'] = args.set_interval
        save_config(config)
        print(f"Default timer interval set to {args.set_interval} minutes.")
        return

    if not args.project_name or not args.task:
        parser.print_help()
        return

    current_interval = args.interval if args.interval is not None else config.get('interval', 60)
    run_timer(args.project_name, args.task, current_interval)

if __name__ == "__main__":
    main()
