# TechToolkit

TechToolkit is a modular GUI-based application built for service technicians. It allows users to run and log various tasks and commands often used for system diagnostics. It comes with a friendly and customizable interface which can be modified through a configuration file. 

TechToolkit's features include:
- Running system diagnostic commands
- Capturing system information (system name, OS version, CPU, RAM, GPU, etc.)
- Capturing network information
- Listing installed devices and software
- Logging the output of these tasks
- Highlighting specific information in the log
- Sending the log to a Discord webhook
- (Further cloud integrations can be added)

## Installation

Before using the application, you need to install Python and some Python libraries.

1. Install Python from [the official website](https://www.python.org/downloads/).
2. Clone this repository or download it as a ZIP file and extract it.
3. Open a terminal (Command Prompt, PowerShell, or Terminal) and navigate to the directory containing the application.
4. Run `pip install -r requirements.txt` to install the required Python libraries.

## Configuration

The application's functionality can be customized by editing the `config.ini` file located in the same directory as the application.

This configuration file is used to define the menus, buttons, patterns for highlighting text in the log, and the Discord webhook URL.

Each section in the `config.ini` file represents a menu or another part of the application. Each key-value pair in a section defines an item in that menu or a property of the application. For example, to define a menu with two items, you could use:

```ini
[File]
Run Command = cmd.exe /C dir
Run PowerShell Script = powershell.exe -ExecutionPolicy Bypass -File script.ps1
```
Patterns for highlighting text in the log are defined in the Patterns section. Each key-value pair in this section defines a pattern and the color to use for highlighting that pattern. For example, to highlight "169.254" in red and "192.168" in blue, you could use:
```ini
[Patterns]
169.254 = red
192.168 = blue
```
## Usage
To use the application, simply run `python techtoolkit.py` from a terminal in the application's directory. The application will start, and you can use the menus and buttons to run the configured commands.

The output of the commands is displayed in the application's console, and any patterns defined in the `config.ini` file are highlighted.

You can also send the log to the Discord webhook defined in the `config.ini` file by clicking the `"Send Log"` button.

## Extending Functionality

The modular nature of the TechToolkit allows it to be easily extended. Users can add their own commands, scripts, or even integrations with other services. 

To add new menu items, add them to the appropriate section in the `config.ini` file. For instance:

```ini
[Tools]
Ping Localhost = cmd.exe /C ping 127.0.0.1
```
This will create a new menu item in the "Tools" menu that pings localhost when clicked.

To add new patterns for highlighting, add them to the `Patterns` section:
```ini
[Patterns]
Error = red
Warning = yellow
```
This will highlight `"Error"` in red and `"Warning"` in yellow in the console.

The application also includes a basic logging function. It logs all the output from the executed commands in the console and can send the logs to a Discord webhook. This can be set up by defining the webhook URL in the Discord section in the `config.ini` file.
```ini
[Discord]
WebhookURL = your_discord_webhook_url
```
This functionality can be extended to support more services like Google Drive, Dropbox, etc., by implementing new methods in the Python code.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests. If you find any issues or have suggestions, please open an issue in the GitHub repository.

## License
TechToolkit is released under the `GNU GPLv3` License. See the `LICENSE` file for more details.
