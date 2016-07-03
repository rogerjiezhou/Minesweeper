__author__ = 'Jie'

from tkinter import *
from tkinter.messagebox import *
import random


class main_window:
    """
    Main window class, there are two frames in the window.
    Top one consist of main button and the bottom one consist of
    button grid
    """
    def __init__(self):
        self.window = Tk()
        self.window.title("Zhoujie 968212")
        self.top_frame = Frame(self.window)
        self.bottom_frame = Frame(self.window)
        self.top_frame.pack(side=TOP)
        self.bottom_frame.pack(side=BOTTOM)

        #import all the images
        self.photo_new = PhotoImage(file="c:\\temp\\new_game_button.png")
        self.photo_won = PhotoImage(file="c:\\temp\\won.png")
        self.photo_button = PhotoImage(file="c:\\temp\\button.png")
        self.photo_mine = PhotoImage(file="c:\\temp\\mine.png")
        self.photo_flag = PhotoImage(file="c:\\temp\\flag.png")
        self.photo_lost = PhotoImage(file="c:\\temp\\lost.png")
        self.photo_hit = PhotoImage(file="c:\\temp\\hit.png")

        #create buttons and information lists
        self.main_button = Button(self.top_frame, image=self.photo_new)
        self.main_button.bind("<ButtonPress-1>", self.restart)
        self.main_button.pack()
        self.button_list = []
        self.mine_list = []
        self.flag_list = []
        self.win = True
        self.window.resizable(width=FALSE, height=FALSE)

        #create the map
        self.create_buttons()
        self.create_maps()

    def create_buttons(self):
        """
        create a one dimensional button list,
        bind event handler to left and right click
        """
        for i in range(81):
            self.new_button = my_button(self.bottom_frame,i)
            self.new_button.config(image=self.photo_button)
            self.new_button.config(bg="#bdbdbd")
            self.button_list.append(self.new_button)
            self.new_button.grid(row=i%9, column=i//9)
            self.new_button.bind("<ButtonRelease-1>", lambda event, j=i: self.left_click(j))
            self.new_button.bind("<Button-3>", lambda event, j=i: self.right_click(j))


    def create_maps(self):
        """
        create map of button store information
        (mine button, number button, empt button
        """
        self.mine_list.clear()
        self.flag_list.clear()

        #create a mine list with ten non-repeatitve number
        self.mine_list = random.sample(range(0,81),10)
        self.mine_list.sort()
        for i in range(10):
            self.button_list[self.mine_list[i]].set_mine()

        #create number button based on their number of neighbor mines
        for i in range(81):
            count = 0
            if i%9 > 0:
                if self.button_list[i-1].isMine:
                    count += 1
            if i > 8:
                if self.button_list[i-9].isMine:
                    count += 1
            if i%9 < 8:
                if self.button_list[i+1].isMine:
                    count += 1
            if i < 72:
                if self.button_list[i+9].isMine:
                    count += 1
            if i%9 > 0 and i > 8:
                if self.button_list[i-10].isMine:
                    count += 1
            if i > 8 and i%9 < 8:
                if self.button_list[i-8].isMine:
                    count += 1
            if i%9 < 8 and i < 72:
                if self.button_list[i+10].isMine:
                    count += 1
            if i < 72 and i%9 > 0:
                if self.button_list[i+8].isMine:
                    count += 1
            if count > 0 and not self.button_list[i].isMine:
                self.button_list[i].isNumber = True
            self.button_list[i].set_number(count)

    def recusive_check(self,order):
        """
        Recusive method to check the neighbor status
        until the neighbor is the boundary or number button
        """
        if self.button_list[order].isNumber:
            self.button_list[order].set_pass()
            self.button_list[order].show_number()
            return
        if self.button_list[order].isPass:
            return
        else:
            #if the button is on the boundary
            if order%9 == 0 or order%9 == 8 or order < 9 or order > 71:
                self.button_list[order].set_pass()
            #check left button
            if order%9 > 0:
                self.button_list[order].set_pass()
                self.recusive_check(order-1)
            #check left-up button
            if order%9 > 0 and order > 8:
                self.button_list[order].set_pass()
                self.recusive_check(order-10)
            #check up button
            if order > 8:
                self.button_list[order].set_pass()
                self.recusive_check(order-9)
            #check right-up button
            if order > 8 and order%9 < 8:
                self.button_list[order].set_pass()
                self.recusive_check(order-8)
            #check right button
            if order%9 < 8:
                self.button_list[order].set_pass()
                self.recusive_check(order+1)
            #check right-down button
            if order%9 < 8 and order < 72:
                self.button_list[order].set_pass()
                self.recusive_check(order+10)
            #check down button
            if order < 72:
                self.button_list[order].set_pass()
                self.recusive_check(order+9)
            #check left-down button
            if order < 72 and order%9 > 0:
                self.button_list[order].set_pass()
                self.recusive_check(order+8)

    def check_win(self):
        """
        Checking winning or not and show dialog
        """
        self.flag_list.sort()
        self.win = True
        for i in range(10):
            if self.flag_list[i] != self.mine_list[i]:
                self.win = False
        if self.win == True:
            self.main_button.config(image=self.photo_won)
            showinfo("You win!", "Congratulations!")

    def restart(self,event):
        """
        Restart the game
        """
        self.main_button.config(image=self.photo_new)
        for i in range(81):
            self.button_list[i].reset()
        self.create_maps()

    def left_click(self,order):
        """
        Left click handler using recursive method if not mine
        """
        #If hit the mine then show losing dialog
        if self.button_list[order].isMine:
            for i in range(10):
                self.button_list[self.mine_list[i]].config(image=self.photo_mine)
            self.button_list[order].config(image=self.photo_hit)
            self.main_button.config(image=self.photo_lost)
            showinfo("You Lose!", "Sorry! Try again")
        else:
            self.recusive_check(order)

    def right_click(self,order):
        """
        Right click handler, if number of flag mine
         is TEN then check winning or not
        """
        if self.button_list[order].isPass:
            return
        else:
            if not self.button_list[order].isFlag:
                 if len(self.flag_list) == 10:
                     return
                 self.button_list[order].config(image=self.photo_flag)
                 self.flag_list.append(order)
                 self.button_list[order].isFlag = True
                 if len(self.flag_list) == 10:
                     self.check_win()
            else:
                 self.button_list[order].config(image=self.photo_button)
                 self.flag_list.remove(order)
                 self.button_list[order].isFlag = False


class my_button(Button):
    """
    My own button class inherit from Button class
    """
    def __init__(self,master,order):
        """
        Pass the order of button to itself, store necessary information
        """
        Button.__init__(self,master)
        self.order = order
        self.isFlag = False
        self.isMine = False
        self.isNumber = False
        self.isPass = False
        self.number = 0

        #Import all the images
        self.photo_new = PhotoImage(file="c:\\temp\\new_game_button.png")
        self.photo_won = PhotoImage(file="c:\\temp\\won.png")
        self.photo_button = PhotoImage(file="c:\\temp\\button.png")
        self.photo_mine = PhotoImage(file="c:\\temp\\mine.png")
        self.photo_flag = PhotoImage(file="c:\\temp\\flag.png")
        self.photo_lost = PhotoImage(file="c:\\temp\\lost.png")
        self.photo_hit = PhotoImage(file="c:\\temp\\hit.png")
        self.photo_one = PhotoImage(file="c:\\temp\\one.png")
        self.photo_two = PhotoImage(file="c:\\temp\\two.png")
        self.photo_three = PhotoImage(file="c:\\temp\\three.png")
        self.photo_four = PhotoImage(file="c:\\temp\\four.png")
        self.photo_five = PhotoImage(file="c:\\temp\\five.png")

    def set_mine(self):
        """
        Set mine flag
        """
        self.isMine = True

    def set_pass(self):
        """
        Set pass flag
        """
        self.isPass = True
        self.config(relief=RIDGE)

    def set_number(self, number):
        """
        Set number if number button
        """
        self.number = number

    def show_number(self):
        """
        Show number image
        """
        if self.number == 1:
            self.config(image=self.photo_one)
        elif self.number == 2:
            self.config(image=self.photo_two)
        elif self.number == 3:
            self.config(image=self.photo_three)
        elif self.number == 4:
            self.config(image=self.photo_four)
        else:
            self.config(image=self.photo_five)

    def reset(self):
        """
        Reset all information if game restart
        """
        self.isFlag = False
        self.isMine = False
        self.isNumber = False
        self.isPass = False
        self.number = 0
        self.config(image=self.photo_button)
        self.config(relief=RAISED)

main = main_window()
mainloop()

