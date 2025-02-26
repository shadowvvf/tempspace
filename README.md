# ScriptTemp - Temporary Project Directory Manager

A Python script that helps manage temporary project directories by creating them with automatic cleanup capabilities.

## Features

- Creates temporary project directories with unique UUIDs
- Automatically opens the created directory in your system's file explorer
- Configurable deletion time for temporary directories
- Automatic cleanup of expired directories
- Cross-platform support (Windows, macOS, Linux)

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