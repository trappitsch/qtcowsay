# SPDX-FileCopyrightText: 2024-present Reto Trappitsch <reto@galactic-forensics.space>
#
# SPDX-License-Identifier: MIT

import sys

import cowsay
from PyQt6 import QtGui, QtWidgets


# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QtCowSay")

        # description label
        desc = QtWidgets.QLabel("Enter text to be said and select character")

        # entry for what to say
        self.entry = QtWidgets.QLineEdit()

        # select character
        self.character = QtWidgets.QComboBox()
        self.character.setToolTip("Select the character to say something")
        self.character.addItems(cowsay.char_names)
        self.character.setCurrentText("cow")

        # label to print
        self.print_area = QtWidgets.QLabel("")
        self.print_area.setToolTip("The cow says...")

        # buttons
        button_print = QtWidgets.QPushButton("Say...")
        button_print.clicked.connect(self.cowsay)

        button_exit = QtWidgets.QPushButton("Exit")
        button_exit.clicked.connect(self.close)

        # Set the central widget of the Window.
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(button_print)
        button_layout.addWidget(button_exit)

        layout.addWidget(desc)
        layout.addWidget(self.entry)
        layout.addWidget(self.character)
        layout.addWidget(self.print_area)
        layout.addLayout(button_layout)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def cowsay(self):
        """Print what the cow says in the label."""
        text = self.entry.text()

        # set font of label
        font = QtGui.QFont("Monospace", 12)
        font.setStyleHint(QtGui.QFont.StyleHint.TypeWriter)
        self.print_area.setFont(font)

        # character
        character = self.character.currentText()

        # set output to label
        try:
            out = cowsay.get_output_string(character, text)
        except cowsay.CowsayError as e:
            QtWidgets.QMessageBox.warning(self, "Input error", str(e))
            return

        self.print_area.setText(out)


def run():
    """Main function to run the app."""
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    run()
