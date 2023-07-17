import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QMainWindow, QAction, QFileDialog
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import Qt
import configparser
import requests
import json
import re

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.config['App']['Title'])
        self.setGeometry(300, 150, 500, 800)

        widget = QWidget()
        self.setCentralWidget(widget)

        # Create layout and add widgets
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        self.add_menu()

        # Send Log button
        button = QPushButton('Send Log')
        button.clicked.connect(self.send_log_to_discord)
        layout.addWidget(button)

        # Clear Console Log button
        clear_button = QPushButton('Clear Log')
        clear_button.clicked.connect(self.clear_console)
        layout.addWidget(clear_button)

    def add_menu(self):
        menu = self.menuBar()
        for section in self.config.sections():
            if section != 'App' and section != 'Patterns' and section != 'Discord':
                menu_section = menu.addMenu(section)
                for key in self.config[section]:
                    action = QAction(key, self)
                    action.triggered.connect(lambda checked, s=self.config[section][key]: self.run_command(s))
                    menu_section.addAction(action)

    def run_command(self, command):
        if "powershell.exe" in command:
            # Extract the relative path from the command string
            relative_path = re.search(r'-File ./?(.*?)$', command).group(1)

            # Generate the absolute path to the file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_path = os.path.join(base_dir, relative_path)

            # Print for debugging
            print(f"base_dir = {base_dir}")
            print(f"relative_path = {relative_path}")
            print(f"absolute_path = {absolute_path}")

            # Replace the relative path in the command string with the absolute path
            command = command.replace('./' + relative_path, absolute_path)

            # Print the final command for debugging
            print(f"final command = {command}")

        elif "./" in command:
            # Extract the relative path from the command string
            relative_path = re.search(r'\./?(.*?)$', command).group(1)

            # Generate the absolute path to the file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            absolute_path = os.path.join(base_dir, relative_path)

            # Print for debugging
            print(f"base_dir = {base_dir}")
            print(f"relative_path = {relative_path}")
            print(f"absolute_path = {absolute_path}")

            # Replace the relative path in the command string with the absolute path
            command = command.replace('./' + relative_path, absolute_path)

            # Print the final command for debugging
            print(f"final command = {command}")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.add_to_console(output.decode('utf-8'))
        if error:
            self.add_to_console(error.decode('utf-8'), 'red')


    def add_to_console(self, text, color=None):
        self.console.moveCursor(QTextCursor.End)
        for line in text.splitlines():
            line_color = color
            if line_color is None:
                for pattern, pattern_color in self.config['Patterns'].items():
                    if re.search(pattern, line):
                        line_color = pattern_color
                        break
            if line_color:
                self.console.setTextColor(QColor(line_color))
            self.console.append(line)
            self.console.setTextColor(QColor('black'))

    def clear_console(self):
        self.console.clear()

    def send_log_to_discord(self):
        # Get all the text from the console
        log = self.console.toPlainText()

        # Save the log to a text file
        with open('log.txt', 'w') as f:
            f.write(log)

        # Define the webhook URL from the config file
        webhook_url = self.config['Discord']['WebhookURL']

        # Create the data to send
        data = {
            'content': 'Log file from TechToolkit'
        }

        # Send the log file to the webhook
        result = requests.post(webhook_url, data=data, files={'file': open('log.txt', 'rb')})

        # If the post request was not successful, print the error
        if result.status_code != 204:
            print(f'Error sending message to Discord: {result.status_code}, {result.text}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
