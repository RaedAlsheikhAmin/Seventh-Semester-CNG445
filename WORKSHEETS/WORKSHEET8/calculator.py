from tkinter import *

class Calculator(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Calculator")

        self.master.rowconfigure(0,weight=1)#that we make the window expandable
        self.master.columnconfigure(0,weight=1)#for the columns

        for i in range(0,5):
            self.rowconfigure(i, weight=1)#for each row
        for j in range(0,4):
            self.columnconfigure(j,weight=1)#for each column

        self.grid(sticky=W+E+N+S)
        self.mainEntry = Entry(self, justify=RIGHT)
        self.mainEntry.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S)#columnspan that we have 4 buttons in each row

        items = [["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["0", ".", "=", "+"]]
        for i in range(0,4):
            for j in range(0,4):
                if items[i][j]== "=":
                    self.button = Button(self, text=items[i][j], command= self.calculate)
                else:
                    self.button=  Button(self, text=items[i][j])
                    self.button.bind("<Button-1>", self.buttonPressed)#rights button of the mouth, bind functionality gives as another parameter which is event.
                self.button.grid(row=i+1, column=j, sticky=W+E+N+S)#i+1 because the first span will be for the entry
    def buttonPressed(self, event):
        value = event.widget["text"]#access that event and get the text attribute
        self.mainEntry.insert(END, value)#starting position at the end
    def calculate(self):
        expression = self.mainEntry.get()
        result=eval(expression)#to get the value
        self.mainEntry.delete(0,END)# starting from the beginning, delete everything
        self.mainEntry.insert(0, result)#adding the result to the main entry



if __name__ == "__main__":
    cal = Calculator()
    cal.mainloop()

