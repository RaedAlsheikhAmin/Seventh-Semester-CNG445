from tkinter import *

class Calculator(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Calculator")

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        for i in range(0,5):
            self.rowconfigure(i, weight=1)

        for j in range(0,4):
            self.columnconfigure(j, weight=1)

        self.grid(sticky=W+E+N+S)
        self.mainEntry = Entry(self, justify=RIGHT)
        self.mainEntry.grid(row=0, column=0, columnspan=4, sticky=W+E+N+S)

        items = [["7", "8", "9", "/"], ["4", "5", "6", "*"], ["1", "2", "3", "-"], ["0", ".", "=", "+"]]
        for i in range(0,4):
            for j in range(0,4):
                if items[i][j] == "=":
                    self.button = Button(self, text=items[i][j], command = self.calculate)
                else:
                    self.button = Button(self, text=items[i][j])
                    self.button.bind("<Button-1>", self.buttonPressed)
                self.button.grid(row=i+1, column=j, sticky=W+E+N+S)

    def buttonPressed(self, event):
        value = event.widget["text"]
        self.mainEntry.insert(END, value)

    def calculate(self):
        expression = self.mainEntry.get()
        result = eval(expression)
        self.mainEntry.delete(0, END)
        self.mainEntry.insert(0, result)

if __name__ == "__main__":
    cal = Calculator()
    cal.mainloop()


