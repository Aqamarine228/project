import logging
import sys
from logging.handlers import RotatingFileHandler

from PyQt5.QtWidgets import QApplication

from view.main_view import MainView

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(filename)s:%(lineno)d "
           "[%(asctime)s] - %(name)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            filename='logs/all.log',
            maxBytes=1024 * 1024 * 25,
            encoding='UTF-8',
        ),
        RotatingFileHandler(
            filename='logs/errors.log',
            maxBytes=1024 * 1024 * 25,
            encoding='UTF-8',
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger().handlers[1].setLevel(logging.ERROR)


def main():
    # Start the Qt app
    app = QApplication(sys.argv)
    window = MainView()  # Create main window
    window.show()        # Show the window
    sys.exit(app.exec_())  # Run app loop

if __name__ == '__main__':
    main()