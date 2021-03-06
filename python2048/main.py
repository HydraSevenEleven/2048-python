from Controller import core
from Views.Tkinter import tkinterView

def main():
    c = core.Core(4)
    view = tkinterView.GameGrid(c)

main()
