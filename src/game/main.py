#to publish on windows 10, enter terminal and enter this directory and type:
#pyinstaller -F --icon=..\\assets\images\icon.ico --add-data "..\\assets;..\\assets" main.py
"""
TODO:basic ai https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/23853848#23853848
"""
import tkinter as tk
from src.game.game import Game


class Wrapper():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('2048')
        self.root.iconbitmap(default='..\\assets\\images\\icon.ico')

        self.bg = tk.Frame(self.root, bg='white', width=400, height=400)
        self.game=Game(self.bg)
        self.bg.bind('<Up>', lambda e,dir='up':self.game.step_wrapper(dir))
        self.bg.bind('<Down>', lambda e,dir='down':self.game.step_wrapper(dir))
        self.bg.bind('<Left>', lambda e,dir='left':self.game.step_wrapper(dir))
        self.bg.bind('<Right>', lambda e,dir='right':self.game.step_wrapper(dir))
        self.bg.pack(side=tk.BOTTOM)
        self.bg.focus_set()

        menubar=tk.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label='reset', command=self.game.reset)
        menubar.add_command(label='high scores', command=self.game.high_score)
        menubar.add_command(label='about', command=self.about_game)

        self.root.mainloop()

    def about_game(self):
        about = tk.Toplevel(self.root)
        about.geometry("%dx%d%+d%+d" % (200, 30, 0, 0))
        about.title('about')
        about_text=tk.Label(about,text="made by mikey2520 on 5.24.2020")
        about_text.pack()

if __name__ == '__main__':
    wrapper = Wrapper()
