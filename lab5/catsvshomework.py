"""
Setup script for Cats vs Homework game
Last edited by Geisler 2024
"""

import tkinter as tk
from src.main_menu import MainMenu

def main():
    menu = MainMenu()
    manager = menu.run()
    if manager is not None:
        manager.root().mainloop()

if __name__ == '__main__':
    main()
