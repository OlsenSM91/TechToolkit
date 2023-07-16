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
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.config['App']['Title'])
        self.setGeometry(300, 300, 300, 200)

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
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        self.add_to_console(output.decode('utf-8'))
        if error:
            self.add_to_console(error.decode('utf-8'), 'red')

    def add_to_console(self, text, color=None):
        self.console.moveCursor(QTextCursor.End)
        if color:
            self.console.setTextColor(QColor(color))
        for line in text.splitlines():
            self.console.append(line)
            for pattern, color in self.config['Patterns'].items():
                if re.search(pattern, line):
                    self.console.setTextColor(QColor(color))
                    self.console.append(line)
        self.console.setTextColor(QColor('black'))

    def send_log_to_discord(self):
        # Get all the text from the console
        log = self.console.toPlainText()

        # Create the message with ``` at the beginning and end
        message = '```\n' + log + '\n```'

        # Define the webhook URL from the config file
        webhook_url = self.config['Discord']['WebhookURL']

        # Create the data to send
        data = {
            'content': message
        }

        # Send the data to the webhook
        result = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})

        # If the post request was not successful, print the error
        if result.status_code != 204:
            print(f'Error sending message to Discord: {result.status_code}, {result.text}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
