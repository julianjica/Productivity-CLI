#  Productivity Timer

A command-line time tracking tool designed for developers and anyone who wants to monitor time spent on projects and tasks directly from the terminal.

This tool provides a visually rich timer, persistent logging, and detailed reporting to help you understand your workflow and improve your productivity.
## Features

*   **Interactive Timer:** A full-screen timer with a progress bar that cycles through colors for each work interval.
*   **Persistent Logging:** Automatically saves your sessions to a `productivity_log.csv` file. It intelligently consolidates time, summing up durations for the same project/task.
*   **Configurable Intervals:** Set a default work interval (in minutes) that persists between sessions.
*   **Intuitive Controls:**
    *   **Enter:** Pause and resume the timer.
    *   **Ctrl+C:** Instantly save the session and exit.
*   **Detailed Reporting:**
    *   Generate a summary report showing time spent per project and its percentage of the total.
    *   Generate a detailed report for a specific project, breaking down time by task.
*   **Historical Context:** When you start a timer, it shows you the total time you've previously logged for that specific task.
## Requirements
*   Python 3
*   `rich` library
## Installation

1.  Ensure you have Python 3 installed.
2.  Install the `rich` library (using `pip`)
    ```bash
    pip install rich
    ```
## Usage
The script is controlled via command-line arguments.
### Running the Timer
To start a timer, provide a project name and a task name.
```bash
python3 productivity_timer.py "My Awesome Project" "Implement feature X"
```
*   **To Pause/Resume:** Press `Enter`.
*   **To Stop & Save:** Press `Ctrl+C`.
### Configuration
Set a default interval (e.g., 45 minutes) that will be used for all future timer sessions.
```bash
python3 productivity_timer.py --set-interval 45
```

You can override the default for a single session:

```bash
python3 productivity_timer.py "Project" "Task" --interval 15
```
### Generating Reports

**Summary Report:**
To see a summary of time spent on all projects, run the `--report` flag without a project name.

```bash
python3 productivity_timer.py --report
```

**Project-Specific Report:**
To get a detailed report for a single project, provide the project name.

```bash
python3 productivity_timer.py --report "My Awesome Project"
```

## Files

*   `productivity_log.csv`: This file stores your session data. Each row contains the date of the last session, project name, task name, and the total duration.
*   `config.json`: This file stores your default interval setting.
