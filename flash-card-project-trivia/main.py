
from tkinter import *
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"

original_file = "data/new_questions.csv"
learning_file = "data/words_to_learn.csv"
learned_file = "data/learned_questions.csv"

current_card = {}
flip_timer = None

# Load the latest Questions
original_data = pandas.read_csv(
    original_file,
    encoding="cp1252"
)

# Clean column names and remove empty rows
original_data.columns = original_data.columns.str.strip()
original_data = original_data.dropna(subset=["Question", "Answer"])

all_words = original_data.to_dict(orient="records")

# Load previously learned words
if os.path.exists(learned_file):
    learned_data = pandas.read_csv(
        learned_file,
        encoding="utf-8"
    )
    learned_words = learned_data.to_dict(orient="records")
else:
    learned_words = []

# Include new words and exclude previously learned words
to_learn = [
    word for word in all_words
    if word not in learned_words
]


def next_card():
    global current_card, flip_timer

    # Cancel the previous flip timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
        flip_timer = None

    # Stop when all words have been learned
    if not to_learn:
        canvas.itemconfig(
            card_title,
            text="Complete!",
            fill="black"
        )
        canvas.itemconfig(
            card_word,
            text="All words learned!",
            fill="black"
        )
        canvas.itemconfig(
            card_background,
            image=card_front_img
        )
        return

    current_card = random.choice(to_learn)

    canvas.itemconfig(
        card_title,
        text="Question",
        fill="black"
    )

    canvas.itemconfig(
        card_word,
        text=current_card["Question"],
        fill="black"
    )

    canvas.itemconfig(
        card_background,
        image=card_front_img
    )

    # Start a new 3-second timer
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global flip_timer
    flip_timer = None

    canvas.itemconfig(
        card_title,
        text="Answer",
        fill="white"
    )

    canvas.itemconfig(
        card_word,
        text=current_card["Answer"],
        fill="white"
    )

    canvas.itemconfig(
        card_background,
        image=card_back_img
    )


def is_known():
    global to_learn, learned_words

    if not to_learn or not current_card:
        return

    # Remove the current card from the learning list
    to_learn.remove(current_card)

    # Save the card as learned
    if current_card not in learned_words:
        learned_words.append(current_card)

    learned_data = pandas.DataFrame(
        learned_words,
        columns=["Question", "Answer"]
    )

    learned_data.to_csv(
        learned_file,
        index=False,
        encoding="utf-8"
    )

    # Save remaining words
    remaining_data = pandas.DataFrame(
        to_learn,
        columns=["Question", "Answer"]
    )

    remaining_data.to_csv(
        learning_file,
        index=False,
        encoding="utf-8"
    )

    next_card()


# -----------------------------
# USER INTERFACE
# -----------------------------

window = Tk()
window.title("Flashy")
window.configure(
    padx=50,
    pady=50,
    background=BACKGROUND_COLOR
)

canvas = Canvas(
    width=800,
    height=526,
    bg=BACKGROUND_COLOR,
    highlightthickness=0
)

card_front_img = PhotoImage(
    file="images/card_front.png"
)

card_back_img = PhotoImage(
    file="images/card_back.png"
)

card_background = canvas.create_image(
    400,
    263,
    image=card_front_img
)

card_title = canvas.create_text(
    400,
    150,
    text="",
    font=("Arial", 40, "italic")
)

card_word = canvas.create_text(
    400,
    263,
    text="",
    font=("Arial", 40, "bold"),
    width=700,
    justify="center"
)

canvas.grid(
    row=0,
    column=0,
    columnspan=2
)

# Wrong answer button
cross_image = PhotoImage(
    file="images/wrong.png"
)

unknown_button = Button(
    image=cross_image,
    highlightthickness=0,
    command=next_card
)

unknown_button.grid(
    row=1,
    column=0
)

# Correct answer button
check_image = PhotoImage(
    file="images/right.png"
)

known_button = Button(
    image=check_image,
    highlightthickness=0,
    command=is_known
)

known_button.grid(
    row=1,
    column=1
)

# Start flashcards
next_card()

window.mainloop()
