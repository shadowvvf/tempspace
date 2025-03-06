# ScriptTemp - Temporary Project Directory Manager

A Python script that helps manage temporary project directories by creating them with automatic cleanup capabilities.

## Features

- Creates temporary project directories with unique UUIDs
- Automatically opens the created directory in your system's file explorer
- Configurable deletion time for temporary directories
- Automatic cleanup of expired directories
- Cross-platform support (Windows, macOS, Linux)

## New Feature

- **List Temporary Directories**: You can now view all existing temporary project directories along with their deletion statuses by running the script. This feature helps you keep track of your temporary projects and their scheduled deletion times.
- **Custom Name for Temporary Directories**: Users can now specify a custom name for the temporary directory when creating it, providing more flexibility in naming.

## Recent Changes

- **Confirmation Dialog**: Added a confirmation dialog before creating temporary directories to prevent accidental creations.
- **Enhanced Directory Listing**: Improved the output format of the list of temporary directories for better readability.

## Requirements

- Python 3.x
- Standard Python libraries (all built-in):
  - os
  - time
  - uuid
  - platform
  - subprocess
  - shutil

## Installation

1. Download the `temp.py` script
2. Ensure you have Python 3.x installed on your system

## Usage

Run the script using Python:

```bash
python temp.py
```

The script will:
1. Create a new temporary project directory in `~/ScriptTemp_projects/`
2. Open the directory automatically in your system's file explorer
3. Prompt you to specify when the directory should be deleted:
   - Enter number of days (e.g., `7` for one week)
   - Enter `0` to delete the directory on next script execution
4. List all existing temporary project directories and their deletion statuses.

## Directory Structure

The script creates and manages two main directories:
- `~/.ScriptTemp/` - Stores metadata files for tracking temporary directories
- `~/ScriptTemp_projects/` - Contains the actual temporary project directories

## How It Works

1. On startup, the script checks for and removes any expired temporary directories
2. Creates a new UUID-based directory
3. Stores deletion metadata in a `.meta` file
4. Opens the new directory automatically
5. Waits for user input to set deletion time

## Notes

- Directories marked for deletion (with days = 0) will be removed on the next script execution
- The script uses `.meta` files to track directory locations and deletion times
- All temporary directories are created with unique UUIDs to prevent conflicts

## Security

The script only deletes directories that:
1. Exist within the `ScriptTemp_projects` directory
2. Have a corresponding `.meta` file
3. Have reached their deletion time

# GUI Application

## Running the GUI

To run the GUI application, execute the following command:

```bash
python gui.py
```

This will launch the GUI interface built with PySide6.

## Automatic Cleanup of Expired Directories

The script now automatically removes any expired temporary directories upon startup, ensuring that your workspace remains clean and organized. 