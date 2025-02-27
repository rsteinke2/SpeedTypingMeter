from tkinter import *
import random
from random_texts import random_texts

# ---------------------------- CONSTANTS ------------------------------- #
BROWN = "#964B00"
WHITE = "#FFFFFF"
BLACK = "#000000"
FONT_NAME = "Manrope"
DEFAULT_FONT_SIZE = 30
IMAGE_PATH = None  # To store the path of the uploaded image
original_image = None
watermarked_image = None
time_s = 60  # Timer starts from 60 seconds
timer_started = False  # Flag to check if the timer has started
typed_text = ""  # Variable to store the text typed by the user

# ---------------------------- TIMER FUNCTION ------------------------------- #
def start_timer(label):
    global time_s, typed_text
    if time_s > 0:
        label.config(text=f"Start typing the text below...( {time_s}s remaining)")
        time_s -= 1
        label.after(1000, start_timer, label)
    else:
        label.config(text="Time is up!")
        calculate_wpm(typed_text)

def on_keypress(event, label, text_box):
    global timer_started, typed_text
    if not timer_started:
        timer_started = True
        start_timer(label)
        text_box.delete("1.0", "end")  # Clear the default text when typing starts
    # Update typed_text variable on every key press
    typed_text = text_box.get("1.0", "end-1c")  # Get the text from the text box

def calculate_wpm(text):
    words = text.split()  # Split the text into a list of words
    speed = len(words) / (60 / 60)  # Calculate WPM (total words / time in minutes)

    # Display WPM in a message box
    result_label.config(text=f"Your typing speed is: {speed:.2f} WPM")  # Show the WPM

# ---------------------------- UTILITY FUNCTION FOR JUSTIFYING TEXT ------------------------------- #
def justify_text(text, line_length, max_lines):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
            if len(lines) == max_lines - 1:  # Ensure we don't exceed the max line count
                break
    lines.append(current_line.strip())  # Append the last line

    # Join the lines with newlines to create a justified effect
    justified_text = "\n".join(lines[:max_lines])
    return justified_text

# ---------------------------- RESET FUNCTION ------------------------------- #
def reset_game():
    global time_s, timer_started, typed_text, justified_text
    time_s = 60  # Reset timer
    timer_started = False  # Reset timer flag
    typed_text = ""  # Clear typed text
    text_box.delete("1.0", "end")  # Clear the text box
    countdown_label.config(text=f"Start typing the text below...( {time_s}s remaining)")  # Reset label
    result_label.config(text="")  # Clear result label

    # Get a new random text and format it
    random_text = random.choice(random_texts)
    justified_text = justify_text(random_text, line_length=50, max_lines=10)

    # Update the justified random text label
    random_text_label.config(text=justified_text)

# ---------------------------- MAIN UI SETUP ------------------------------- #
def show_window():
    global time_s, result_label, text_box, countdown_label, random_text_label

    window = Tk()
    window.title("Typing Speed Meter")
    window.config(padx=100, pady=50, bg=BLACK)

    # Configuring grid weights for centering elements
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)

    # Title label
    title_label = Label(text="Typing Speed Meter", fg=WHITE, bg=BLACK, font=(FONT_NAME, 30))
    title_label.grid(column=0, row=0, columnspan=3, sticky="nsew")

    # Adjusting canvas size to match the image size
    canvas = Canvas(width=282, height=274, bg=BLACK, highlightthickness=0)
    speed_typing_img = PhotoImage(file="speed_typing.png")  # Replace with your image path
    canvas.create_image(141, 137, image=speed_typing_img)  # Center the image in the canvas
    canvas.grid(column=0, row=1, columnspan=3, sticky="nsew", padx=60)

    # Countdown label
    countdown_label = Label(text=f"Start typing the text below...( {time_s}s remaining)", fg=WHITE,
                            bg=BLACK, font=(FONT_NAME, 15))
    countdown_label.grid(column=0, row=2, columnspan=3, sticky="nsew", pady=20)

    # Get random text and format it
    random_text = random.choice(random_texts)
    justified_text = justify_text(random_text, line_length=50, max_lines=10)

    # Display justified random text
    random_text_label = Label(text=justified_text, fg=WHITE, bg=BLACK, font=(FONT_NAME, 15),
                              justify=LEFT)
    random_text_label.grid(column=0, row=3, columnspan=3, sticky="nsew", pady=20)

    # Text box for user to type in
    text_box = Text(window, height=10, width=50)
    text_box.insert("1.0", "Start typing here...")  # Insert default text
    text_box.grid(column=0, row=4, columnspan=3, sticky="nsew")

    # Bind keypress event to the text box to start the timer when typing starts
    text_box.bind("<KeyPress>", lambda event: on_keypress(event, countdown_label, text_box))

    # Label to display the result
    result_label = Label(text="", fg=WHITE, bg=BLACK, font=(FONT_NAME, 15))
    result_label.grid(column=0, row=5, columnspan=3, sticky="nsew", pady=20)

    # Reset button
    reset_button = Button(text="Reset", command=reset_game, fg=WHITE, bg=BROWN, font=(FONT_NAME, 15))
    reset_button.grid(column=0, row=6, columnspan=3, sticky="nsew", pady=20)

    window.mainloop()


show_window()
