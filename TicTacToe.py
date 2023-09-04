"""
Tic tac toe using python's tkinter (not the best approach by any means, I did it this way mostly as a 1 day, short code challange).
The user will play with "X", while the computer will play with "0".
Still need to implement a hard difficulty.
"""

import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
import random
from tkinter import messagebox
import os


class Tic_Tac_Toe_Game:
    def __init__(self, computer_starts = False, difficulty = "easy"):
        self.__create_interface(computer_starts, difficulty)

    def __create_interface(self, computer_starts, difficulty):
        self.__root = tk.Tk()
        self.__root.geometry("610x600")
        self.__root.title("Tic and toe")

        self.__widgets_grid = {}
        self.__free = list(range(1,10)) # The places on the grid where a move can be done
        self.computer_starts = computer_starts
        self.difficulty = difficulty

        for row in range(3):
            for column in range(3):
                grid_element = empty(self.__root, (row,column)) # Assign empty objects to the grid
                grid_element.label.bind("<Button-1>",self.__player_input)
                self.__widgets_grid[(row,column)] = grid_element

        self.__first_value = self.__get_first_label_number() # Will be used to keep track of the labels created by tkinter each time, so multiple plays are allowed.
        # It is a result of a tkinter restriction in designing games
        if self.computer_starts:
            self.__computer_move(self.difficulty)


    def start(self):
        self.__root.mainloop()

    def __player_input(self, event):
        selected = self.__get_element_from_event(event)

        self.__free.remove(selected)

        row = (selected-1) // 3 
        column = (selected-1) % 3 

        self.__widgets_grid[(row,column)] = x(self.__root,(row,column))
        
        winner = self.__evaluate_grid()

        if not self.__decide_outcome(winner):
            self.__computer_move(self.difficulty)


    def __computer_move(self, difficulty):
            if difficulty == "hard":
                move = self.__get_optimal_move()
            elif difficulty == "medium":
                move = self.__get_good_move()
            else:
                move = random.choice(self.__free)

            print(self.__free)
            self.__free.remove(move) 
            row = (move-1) // 3 
            column = (move-1) % 3 
            self.__widgets_grid[(row,column)] = o(self.__root,(row,column))

            winner = self.__evaluate_grid()
            self.__decide_outcome(winner)

    def __get_good_move(self):
        """
        Returns a good move by the computer, but not the best. Checks if the computer would win by making a specific move and makes it if so.
        Then checks if the player would win by making a specific move and blocks that move instead. Called if the difficulty is "medium"
        """
        test_grid = {}
        for i in range(3):
            for j in range(3):
                if isinstance(self.__widgets_grid[(i,j)], x):
                    test_grid[(i,j)] = "x"
                elif isinstance(self.__widgets_grid[(i,j)], o):
                    test_grid[(i,j)] = "o"
                else:
                    test_grid[(i,j)] = "empty"

        for move in self.__free:
            row = (move-1) // 3 
            column = (move-1) % 3 
            test_grid[(row,column)] = "o"
            result = self.__evaluate_grid(test_grid)
            test_grid[(row,column)] = "empty"
            if result == "o":
                return move

        for move in self.__free:
            row = (move-1) // 3 
            column = (move-1) % 3 
            test_grid[(row,column)] = "x"
            result = self.__evaluate_grid(test_grid)
            test_grid[(row,column)] = "empty"
            if result == "x":
                return move   
    
        return random.choice(self.__free)

    def __decide_outcome(self, winner):
        if winner == "x":
            self.__unbind_all()
            answer = messagebox.askokcancel("Game over!","You won! Want to play again?")
            if answer:
                self.__play_again()
            return 1
        
        elif winner == "o":
            self.__unbind_all()
            answer = messagebox.askokcancel("Game over!","You lost! Want to play again?")
            if answer:
                self.__play_again()
            return 1
        
        elif winner is None and len(self.__free) != 0:
            return 0
        else:
            answer = messagebox.askokcancel("Game over!","Draw! Want to play again?")
            if answer:
                self.__play_again()
            return 1

    def __evaluate_grid(self, grid = None):
        """
        Evaluates "grid" to check if either the player or the computer has won. If called without the argument "grid" it will evaluate the playing grid, and update it marking
        who has won. It can also be called with another grid, in which it will evaluate that board. Usefull when making better moves by the computer, to not mess up the default grid.
        """
        x_wins = 0
        o_wins = 0

        if grid == None:
            test_grid = {}
            for i in range(3):
                for j in range(3):
                    if isinstance(self.__widgets_grid[(i,j)], x):
                        test_grid[(i,j)] = "x"
                    elif isinstance(self.__widgets_grid[(i,j)], o):
                        test_grid[(i,j)] = "o"
                    else:
                        test_grid[(i,j)] = "empty"
        else:
            test_grid = grid

        for i in range(3):
            for j in range(3):
                if test_grid[(i,j)] == "x":
                    x_wins += 1

                if test_grid[(i,j)] == "o":
                    o_wins += 1

            if o_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(i,index)] = o_red(self.__root, (i,index))
                return "o"
            
            if x_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(i,index)] = x_red(self.__root, (i,index))
                return "x"
            o_wins = 0
            x_wins = 0

        for i in range(3):
            for j in range(3):
                if test_grid[(j,i)] == "x":
                    x_wins += 1

                if test_grid[(j,i)] == "o":
                    o_wins += 1

            if o_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,i)] = o_red(self.__root, (index,i))
                return "o"
            
            if x_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,i)] = x_red(self.__root, (index,i))
                return "x"
            o_wins = 0
            x_wins = 0

        for i in range(3):
            if test_grid[(i,i)] == "x":
                x_wins += 1
            if test_grid[(i,i)] == "o":
                o_wins += 1
            
            if o_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,index)] = o_red(self.__root, (index,index))
                return "o"
            
            if x_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,index)] = x_red(self.__root, (index,index))
                return "x"
            
        o_wins = 0
        x_wins = 0

        for i in range(3):
            if test_grid[(i,2-i)] == "x":
                x_wins += 1
            if test_grid[(i,2-i)] == "o":
                o_wins += 1
            
            if o_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,2-index)] = o_red(self.__root, (index,2-index))
                return "o"
            
            if x_wins == 3:
                if grid == None:
                    for index in range(3):
                        self.__widgets_grid[(index,2-index)] = x_red(self.__root, (index,2-index))
                return "x"

        return None
        
    def __unbind_all(self):
        for item in self.__widgets_grid.values():
            item.label.unbind("<Button-1>")
    
    def __play_again(self):
        self.__free = list(range(1,10))

        for row in range(3):
            for column in range(3):
                self.__widgets_grid[(row,column)] = empty(self.__root, (row,column))
                self.__widgets_grid[(row,column)].label.bind("<Button-1>",self.__player_input)

        self.__first_value = self.__get_first_label_number() # Gets a new value for the first element, as tkinter has assign it another one on each change

        if self.computer_starts:
            self.__computer_move()
        
              
    def __get_element_from_event(self,event):
        number = Tic_Tac_Toe_Game.get_digits_from(event.widget)
        print(number, self.__first_value)
        number = number + 1 - self.__first_value
        return number 

    def __get_first_label_number(self):
        sequence = Tic_Tac_Toe_Game.get_digits_from(self.__widgets_grid[(0,0)].label)
        return sequence
    
    @staticmethod
    def get_digits_from(sequence):
    """Method used to get the numbers from a sequence, for example, a label's name. Probably could have been avoided given more time."""
        last = [letter for letter in str(sequence) if letter.isdigit()]
        if len(last) == 0:
            last = "1"
        else:
            l = ""
            for item in last:
                l+=item
            last = l
        last = int(last)
        return last

        
class grid_object():
    """Default parent class for any item that will be placed somewhere on the grid"""

    current_path = os.path.dirname(__file__) 
    specific_path = None # Will be over-written by the children classes

    def __init__(self, root, position):
        self.image_path = None
        pil_image = Image.open(self.__get_image_path()).resize((200,200))
        tk_image = ImageTk.PhotoImage(pil_image)

        self.label = tk.Label(root, text=None, image=tk_image)
        self.label.configure(width=200, height=200)
        self.label.image = tk_image

        self.label.bind("<Button-1>")

        self.__place(position)

    def __place(self, position):
        self.label.grid(row=position[0], column=position[1], sticky="nsew")

    @classmethod
    def __get_image_path(cls):
        image_path = grid_object.current_path + cls.specific_path
        return image_path

class x(grid_object): # Over-write the specific_path class attribute in the children of the parent class
    specific_path = "\\images\\x.png"

class o(grid_object):
    specific_path = "\\images\\o.png"
    
class x_red(grid_object):
    specific_path = "\\images\\xred.png"
    
class o_red(grid_object):
    specific_path = "\\images\\ored.png"
  
class empty(grid_object):
    specific_path = "\\images\\empty.jpg"

    
def main():
    game = Tic_Tac_Toe_Game(computer_starts = False, difficulty = "medium")
    game.start()

if __name__ == "__main__":
    main()
