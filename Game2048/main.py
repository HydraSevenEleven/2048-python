from Controller import core
from Views.Tkinter import tkinterView

def main():    
    # initialize the Model
    #model = 
    #initialize the View
    view = tkinterView.GameGrid()
     
    # initialise the Controller and inject view and model
    c = core.Core(4, view) 


if __name__ == '__main__':    
    main()   
