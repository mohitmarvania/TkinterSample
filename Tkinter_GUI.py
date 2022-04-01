"""
Mohit Marvania
github : https://github.com/mohitmarvania/
Project Name :  SAMPLE TKINTER GUI.
"""
from datetime import datetime
from tkinter import *

import cv2
import pyttsx3

engine = pyttsx3.init()
LIGHT_GREY = "#F5F5F5"
LABEL_COLOR = "#25265E"
DEFAULT_FONT = ("Arial", 20)
DIGIT_FONT = ("Arial", 30, "bold")
SMALL_FONT = ("Arial", 16)
LARGE_FONT = ("Arial", 40, "bold")


# Function to open the camera.
def camera():
    live = cv2.VideoCapture(0)
    while True:
        # start_time = time.time()

        check, frame = live.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('CAMERA', frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            # end_time = time.time()
            break
    print("The camera was on at {}".format(datetime.today()))
    live.release()
    cv2.destroyAllWindows()


# Class calculator which contains all the functions of calculator.
class Calculator:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("CALCULATOR")

        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_expression = ""
        self.current_expression = ""
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), ".": (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    # Binding keys to return the answer when 'Enter'/'Return' is pressed.
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    # Function which creates special buttons for clear, equals, etc..
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        # self.create_squareRoot_button()
        self.clear_digit()

    # Function to display the labels on the screen above the buttons.
    def create_display_labels(self):
        total_label = Label(self.display_frame, text=self.total_expression, anchor=E, bg=LIGHT_GREY, fg=LABEL_COLOR,
                            padx=24, font=SMALL_FONT)
        total_label.pack(expand=True, fill="both")

        label = Label(self.display_frame, text=self.current_expression, anchor=E, bg=LIGHT_GREY, fg=LABEL_COLOR,
                      padx=24, font=LARGE_FONT)
        label.pack(expand=True, fill="both")

        return total_label, label

    # Function to add expression and displaying it at the top.
    def add_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    # Creates a grid that displays the digit buttons.
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = Button(self.buttons_frame, text=str(digit), bg="white", fg=LABEL_COLOR, font=DIGIT_FONT,
                            borderwidth=0, command=lambda x=digit: self.add_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=NSEW)

    # Function to append and update the expression.
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # Function that will create a operation buttons in the GUI.
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = Button(self.buttons_frame, text=symbol, bg="#F8FAFF", fg=LABEL_COLOR, font=DEFAULT_FONT,
                            borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=NSEW)
            i += 1

    # Clear function to remove all the entered value.
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    # Clear button function.
    def create_clear_button(self):
        button = Button(self.buttons_frame, text="AC", bg="#F8FAFF", fg=LABEL_COLOR, font=DEFAULT_FONT,
                        borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=NSEW)

    # AC function.
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    # AC function button.
    def create_square_button(self):
        button = Button(self.buttons_frame, text="x\u00b2", bg="#F8FAFF", fg=LABEL_COLOR, font=DEFAULT_FONT,
                        borderwidth=0, command=self.square)
        button.grid(row=0, column=3, sticky=NSEW)

    # Function to clear single digit with backspace.
    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    # Function to clear all digit.
    def clear_digit(self):
        button = Button(self.buttons_frame, text="C", bg="#F8FAFF", fg=LABEL_COLOR, font=DEFAULT_FONT,
                        borderwidth=0, command=self.backspace)
        button.grid(row=0, column=2, sticky=NSEW)

    # Main function that evaluates the operation.
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = Button(self.buttons_frame, text="=", bg="#CCEDFF", fg=LABEL_COLOR, font=DEFAULT_FONT,
                        borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=NSEW)

    def create_display_frame(self):
        frame = Frame(self.window, height=221, bg=LIGHT_GREY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:12])

    def run(self):
        self.window.mainloop()


# Creating a function to call the calculator.
def callCalculator():
    obj = Calculator()
    obj.run()


# Creating a GUI.
window = Tk()
window.title("TKINTER GUI")
window.geometry('500x700')


# Most Main function that will create the outer/main GUI.
def MAIN():
    frame = Frame(window, bg="black")
    heading = Label(window, text="WELCOME")
    heading.grid(row=1, column=2, sticky=NSEW)
    camera_btn = Button(window, text="Camera", command=camera, fg="red", bg="red", padx=50, pady=50)
    camera_btn.grid(row=2, column=2)
    calculator_btn = Button(window, text="Calculator", command=callCalculator, fg="blue", bg="red", padx=50, pady=50)
    calculator_btn.grid(row=2, column=3)

    # Defining audioBook that will be opened on the same GUI.
    def audiobook():
        heading.destroy()
        camera_btn.destroy()
        calculator_btn.destroy()
        audioBook_button.destroy()

        lab1 = Label(window, text="Welcome to audioBook\n Starting Soon!!", font=("Sans serif", 20, "italic"))
        lab1.grid(row=1, column=6)

        def back():
            lab1.destroy()
            but1.destroy()
            MAIN()

        but1 = Button(window, text="Back", command=lambda: back(), fg="black", padx=15, pady=15)
        but1.grid(row=3, column=2)

    audio_text = StringVar()
    audioBook_button = Button(window, textvariable=audio_text, command=lambda: audiobook(), fg="green", bg="red",
                              padx=50, pady=50)
    audio_text.set("AudioBook")
    audioBook_button.grid(row=2, column=4)

    frame.grid()


# Calling the main Function to run the program.
MAIN()
window.mainloop()
