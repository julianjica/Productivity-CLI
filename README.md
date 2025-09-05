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
    -   **Recent History Graph**: See your daily productivity trends over the last 30 days (or a custom period) with an ASCII histogram.
-   **Data Persistence**: All your logged sessions are saved to a `productivity_log.csv` file, ensuring your data is never lost.
-   **Configurable Intervals**: Set a default timer interval for new sessions, saved in `config.json`.
-   **Rich CLI Experience**: Leverages the `rich` library for beautiful, readable, and interactive terminal output.

## 🚀 Getting Started

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/julianjica/Productivity-CLI/edit/master/README.md
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
    productivity_timer "My Project Name" "Specific Task Description"
    ```
    *(The timer will start, and you can pause/resume with `Enter` or save/exit with `Ctrl+C`.)*

-   **Set a default timer interval** (e.g., 25 minutes):
    ```bash
    productivity_timer --set-interval 25
    ```

-   **Start a session with a custom interval for this run only** (e.g., 45 minutes):
    ```bash
    productivity_timer "Deep Work" "Coding Feature X" --interval 45
    ```

-   **Generate an overall productivity summary report** (includes hourly and recent history graphs for all projects):
    ```bash
    productivity_timer --report
    ```

-   **Generate a detailed report for a specific project** (e.g., "My Project Name"), including task breakdown and graphs:
    ```bash
    productivity_timer --report "My Project Name"
    ```

-   **Get help and see all available commands**:
    ```bash
    productivity_timer --help
    ```

## ❤️ Inspiration

This project draws significant inspiration from [Chronologicon](https://github.com/rutherfordcraze/chronologicon), a fantastic CLI tool for time tracking and task management, which sadly is not in development anymore.
