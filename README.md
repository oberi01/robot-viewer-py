# robot-viewer-py
Interactive terminal viewer for RobotFramework output.xml file.

## Intended use
The scope of this little tool is to provide the user with an overview
of a RobotFramework test result when accessing the output.xml file
e.g. in a ssh session.

It is not meant to duplicate functionality of RobotFramework log.html
and report.html. If those exist and html rendering is available,
those should be used.

## Intended audience
This tool is intended to be used by developers and testers which have
basic knowledge of Robot Framework.

## Features
- **Filtered**: Switch between all and only failed tests (Key `a`).
- **Detail View**: View of Error messages and Keywords in terminal session.
- **Windowing**: Support for large test suites.
- **Navigation**: via Arrow Up/Down keys.

## Installation

1. Clone Repository
   ```bash
   cd ~/gitwork
   git clone https://github.com/oberi01/robot-viewer-py.git

2. Install venv with Dependencies
   ```bash
   cd ~/gitwork/robot-viewer-py
   uv venv .venv -p /path/to/python3.13

## Run Tool
   ```bash
   cd ~/gitwork/robot-viewer-py
   uv run robot-view output.xml