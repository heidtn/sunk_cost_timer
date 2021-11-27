import PySide2
from PySide2 import QtCore
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication, QTextEdit, QLabel, QPushButton, QVBoxLayout, QWidget
import os
import argparse
import beepy

"""
TODO:
- QTimer isn't really good for this sort of actual timekeeping.  Just use it as an updater for a better
time source.
"""

class SunkCostTimer:
    TIMER_TICK = 1000  # in ms

    def __init__(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.time_left = float(f.read())
        else:
            self.time_left = float(
                input("Enter max time for project in decimal hours (e.g. 4.5): "))
            with open(filename, 'w') as f:
                f.write(str(self.time_left))

        self.filename = filename
        self.app = QApplication([])
        self.layout = QVBoxLayout()
        self.window = QWidget()

        self.time_label = QLabel(self.hours_to_hour_mins(self.time_left))
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        font = self.time_label.font()
        font.setPointSize(30)
        self.time_label.setFont(font)
        self.play_pause_button = QPushButton("play")
        self.play_pause_button.clicked.connect(self.button_pressed)

        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.play_pause_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick_timer)

        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec_()

    def button_pressed(self):
        if self.play_pause_button.text() == "play":
            self.timer.start(self.TIMER_TICK)
            self.play_pause_button.setText("pause")
        else:
            self.timer.stop()
            self.play_pause_button.setText("play")

    def tick_timer(self):
        self.time_left -= (self.TIMER_TICK / 1000.0)/3600.0
        if self.time_left <= 0:
            self.time_left = 0
            self.timer.stop()
            beepy.beep(sound='error')
        with open(self.filename, 'w') as f:
            f.write(str(self.time_left))
        self.time_label.setText(self.hours_to_hour_mins(self.time_left))

    def hours_to_hour_mins(self, hours):
        total_hours = int(hours)
        minutes = (hours - total_hours) * 60.0
        total_minutes = int(minutes)
        seconds = int((minutes - total_minutes) * 60.0)
        return f"{total_hours}:{total_minutes:02d}:{seconds:02d}"


def main():
    parser = argparse.ArgumentParser(
        description='Sunk cost timer for projects.')
    parser.add_argument('filename', help='filename to create or use for this project',
                        nargs='?', default='sunk_cost_time.txt')
    args = parser.parse_args()
    filename = args.filename
    timer = SunkCostTimer(filename)


if __name__ == "__main__":
    main()
