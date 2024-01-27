# main.py
from kivy.config import Config

# Set the size to a common Android phone screen size
Config.set('graphics', 'width', '360')  # 1080 / 3
Config.set('graphics', 'height', '640')  # 1920 / 3
Config.write()

from fund_app import MyApp  # Importing the MyApp class from the fund_app module

def main():
    # Create an instance of the MyApp class and start the application
    app = MyApp()
    app.run()

# This ensures that the main function is only called when the script is executed directly, not when it's imported
if __name__ == '__main__':
    main()
