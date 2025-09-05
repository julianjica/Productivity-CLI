import argparse
import time
import os

def main():
    parser = argparse.ArgumentParser(description='CLI productivity timer.')
    parser.add_argument('project_name', type=str, help='The name of the project.')
    parser.add_argument('task', type=str, help='The description of the task.')
    args = parser.parse_args()

    print(f"Project: {args.project_name}")
    print(f"Task: {args.task}")
    print("Starting timer... Press Ctrl+C to stop.")

    seconds = 0
    try:
        while True:
            mins, secs = divmod(seconds, 60)
            hours, mins = divmod(mins, 60)
            timer_display = f'{hours:02d}:{mins:02d}:{secs:02d}'
            
            # Use carriage return to overwrite the line
            print(timer_display, end='\r')
            
            time.sleep(1)
            seconds += 1
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        # Recalculate to show the final time before exiting
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        print(f"Total time spent: {hours:02d}:{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    main()
