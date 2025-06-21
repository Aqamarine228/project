import sys
from PyQt5.QtWidgets import QApplication

from view.main_view import MainView


def main():
    # Start the Qt app
    app = QApplication(sys.argv)
    window = MainView()  # Create main window
    window.show()        # Show the window
    sys.exit(app.exec_())  # Run app loop

if __name__ == '__main__':
    main()