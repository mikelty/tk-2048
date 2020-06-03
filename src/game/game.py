import tkinter as tk
from tkinter import messagebox, simpledialog
import src.game.params as p
from random import sample, choice
from math import log
from src.game.util import move, find_empty_locations

debug=False

class Game():
    def __init__(self, bg):
        self.bg = bg
        self.reset()

    def reset(self):
        self.score=0
        self.won = False
        self.lost = False
        self.matrix=None
        self.tiles=None
        self.init_matrix()
        self.draw()
        self.bg.focus_set()

    def init_matrix(self):
        self.matrix = [[0] * 4 for _ in range(4)]
        a, b = sample(list(range(16)), 2)
        x, y = choice([2,4]), choice([2,4])
#        self.matrix[a // 4][a % 4] = x
#        self.matrix[b // 4][b % 4] = y
#        self.score=x+y
        self.matrix[0][0]=1024
        self.matrix[1][0]=1024
        self.score=2048

    def draw(self):
        score_label=tk.Label(self.bg,text=f'score: {self.score}')
        score_label.grid(row=0,column=0,rowspan=4)
        self.tiles = [[None] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                e=self.matrix[i][j]
                l = tk.Label(self.bg, width=10, height=5, borderwidth=2, relief='groove'\
                             ,text='' if e==0 else str(e)\
                             ,background=p.COLORS[0] if e==0 else p.COLORS[int(log(e)//log(2))])
                l.grid(row=i+1, column=j)
                self.tiles[i][j] = l

    #to be written...
    def step_wrapper(self,dir):
        self.step(dir)

    def step(self, dir):
        if not self.lost:
            self.matrix=move(dir,self.matrix)
            if not self.won and self.check_win():
                self.game_won()
            empty_locations=find_empty_locations(self.matrix)
            if not empty_locations:
                self.game_over()
            else:
                new_tile_location=choice(empty_locations)
                r,c=new_tile_location
                new_value=choice([2,4])
                self.matrix[r][c]=new_value
                self.score+=new_value
            self.draw()
            if debug:
                print('\n'.join(' '.join(str(e) for e in row) for row in self.matrix))

    def check_win(self):
        return max(max(row) for row in self.matrix)>=2048

    def game_won(self):
        self.won=True
        messagebox.showinfo(title='congrats',message='game won.')
        self.record_score(self.score)
        self.bg.focus_set()

    def record_score(self, new_score):
        with open(r'../assets/scores.txt', 'r') as f:
            data=f.readlines()
        records=[]
        for line in data:
            name,score=line.split()
            records.append((name,int(score)))
        records.sort(key=lambda x:-x[1])
        if len(records)<10 or new_score>records[-1][1]:
            name=simpledialog.askstring(title='new high score',prompt='please leave your name to be included in the scoreboard:')
            records.append((name, new_score))
        records.sort(key=lambda x:-x[1])
        records=records[:10]
        with open(r'../assets/scores.txt', 'w') as f:
            for record in records:
                f.write(' '.join(str(e) for e in record)+'\n')

    def game_over(self):
        self.lost = True
        messagebox.showinfo(title='sorry',message='game over.')
        self.record_score(self.score)

    def high_score(self):
        with open(r'../assets/scores.txt', 'r') as f:
            data=f.readlines()
        if not data:
            messagebox.showinfo(title='scoreboard',message='no high scores yet. be the first.')
        else:
            scoreboard=tk.Toplevel(self.bg)
            scoreboard.title('high scores')
            for i,line in enumerate(data):
                name, record=line.split()
                l=tk.Label(scoreboard,text=f'No. {i}. {name} {record}')
                l.pack()

