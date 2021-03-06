from Controller import core
from Views import tkinterView
import settings as s

def main():
    
    c = core.Core(s)
    print(c.init_game(3))
    view = tkinterView.GameGrid(c,s)

main()
