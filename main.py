import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # Create the main window
    main_window = MainWindow()

    # Show the main window
    main_window.show()

    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
