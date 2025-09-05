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
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.live import Live
from rich.console import Group
from rich.layout import Layout
from rich.text import Text

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

def log_session(project, task, seconds_spent):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Project', 'Task', 'Duration'])
        
        duration = str(timedelta(seconds=seconds_spent))
        writer.writerow([datetime.now().strftime('%Y-%m-%d'), project, task, duration])

def run_timer(project_name, task, interval_minutes):
    seconds = 0
    color_index = 0
    block_count = 1
    colors = ['blue', 'green', 'yellow', 'red']
    interval_seconds = interval_minutes * 60
    paused = False

    # Create layout
    layout = Layout()
    layout.split(
        Layout(name="main"),
        Layout(name="footer", size=1)
    )
    footer_text = Text("Press Enter to pause/resume. Press Ctrl+C to save and exit.", justify="center", style="dim")
    layout["footer"].update(footer_text)

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        with Live(layout, screen=True, redirect_stderr=False, auto_refresh=False) as live:
            while True:
                current_color = colors[color_index % len(colors)]
                
                header_panel = Panel(f"[bold]Project:[/ ] {project_name}\n[bold]Task:[/ ] {task}", title="Productivity Timer", border_style="magenta")
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
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        log_session(project_name, task, seconds)
        print("\nTimer stopped.")
        duration_str = str(timedelta(seconds=seconds))
        print(f"Total time spent: {duration_str}")

def main():
    parser = argparse.ArgumentParser(description='A productivity timer with persistent settings, logging, and pause/resume.')
    parser.add_argument('project_name', type=str, nargs='?', help='The name of the project.')
    parser.add_argument('task', type=str, nargs='?', help='The description of the task.')
    parser.add_argument('--set-interval', type=int, metavar='MINUTES', help='Set the default timer interval in minutes for future runs.')
    parser.add_argument('--interval', type=int, metavar='MINUTES', help='Override the default interval for this run.')
    args = parser.parse_args()
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