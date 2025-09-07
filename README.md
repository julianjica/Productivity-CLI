# ⏱️ Productivity Timer & Reporter CLI

A robust command-line interface (CLI) tool designed for tracking time spent on projects and tasks, and generating insightful productivity reports. This tool draws inspiration from the elegant CLI experience of [Chronologicon](https://github.com/rutherfordcraze/chronologicon).

## ✨ Features

This application provides powerful features to help you understand and manage your time:

-   **Flexible Time Tracking**: Log time spent on any `project` and `task` combination. Ideal for tracking work sessions, study time, or any activity.
-   **Interactive Timer**: A real-time command-line timer that displays elapsed time and progress. Features include:
    -   **Pause/Resume**: Easily pause and resume your active session by pressing `Enter`.
    -   **Exit**: Save your current session's progress and exit cleanly with `Ctrl+C`.
-   **Comprehensive Reporting**: Gain insights into your productivity with various report types:
    -   **Overall Summary**: View total time spent across all your projects.
    -   **Project-Specific Reports**: Get a detailed breakdown of time spent on individual tasks within a chosen project.
    -   **Hourly Productivity Graph**: Visualize your activity patterns throughout the day with an ASCII histogram.
    -   **Daily Productivity Graph**: See your productivity distribution across the days of the week.
    -   **Recent History Graph**: See your daily productivity trends over the last 30 days (or a custom period) with an ASCII histogram.
-   **Data Persistence**: All your logged sessions are saved to a `productivity_log.csv` file, ensuring your data is never lost.
-   **Configurable Intervals**: Set a default timer interval for new sessions, saved in `config.json`.
-   **Rich CLI Experience**: Leverages the `rich` library for beautiful, readable, and interactive terminal output.

## 🚀 Getting Started

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/julianjica/Productivity-CLI.git
    cd productivity-timer-cli
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -e .
    ```

### Usage

Run the timer and generate reports directly from your terminal:

-   **Start a new tracking session**:
    ```bash
    python productivity_timer.py "My Project Name" "Specific Task Description"
    ```
    *(The timer will start, and you can pause/resume with `Enter` or save/exit with `Ctrl+C`.)*

-   **Set a default timer interval** (e.g., 25 minutes):
    ```bash
    python productivity_timer.py --set-interval 25
    ```

-   **Start a session with a custom interval for this run only** (e.g., 45 minutes):
    ```bash
    python productivity_timer.py "Deep Work" "Coding Feature X" --interval 45
    ```

-   **Generate an overall productivity summary report** (includes all graphs for all projects):
    ```bash
    python productivity_timer.py --report
    ```

-   **Generate a detailed report for a specific project** (e.g., "My Project Name"), including task breakdown and graphs:
    ```bash
    python productivity_timer.py --report "My Project Name"
    ```

-   **Generate a detailed report for a specific task** within a project:
    ```bash
    python productivity_timer.py --report "My Project Name" "Specific Task Description"
    ```

-   **Get help and see all available commands**:
    ```bash
    python productivity_timer.py --help
    ```

## ❤️ Inspiration

This project draws significant inspiration from [Chronologicon](https://github.com/rutherfordcraze/chronologicon), a fantastic CLI tool for time tracking and task management, which sadly is not in development anymore.