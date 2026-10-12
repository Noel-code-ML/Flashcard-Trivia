
import streamlit as st
import pandas as pd
import random
import time
from pathlib import Path

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="Trivia Flashcards",
    page_icon="🧠",
    layout="centered"
)

BACKGROUND_COLOR = "#B1DDC6"

# Use the folder containing app.py
BASE_DIR = Path(__file__).resolve().parent
original_file = BASE_DIR / "data" / "new_questions.csv"

# ---------------------------------
# LOAD TRIVIA QUESTIONS
# ---------------------------------

@st.cache_data
def load_questions(file_path, modified_time):
    try:
        data = pd.read_csv(
            file_path,
            encoding="cp1252"
        )
    except UnicodeDecodeError:
        data = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

    data.columns = data.columns.str.strip()

    if not {"Question", "Answer"}.issubset(data.columns):
        raise ValueError(
            "CSV must contain Question and Answer columns."
        )

    data = data.dropna(
        subset=["Question", "Answer"]
    )

    data = data[["Question", "Answer"]].copy()

    data["Question"] = data["Question"].astype(str).str.strip()
    data["Answer"] = data["Answer"].astype(str).str.strip()

    data = data[
        (data["Question"] != "") &
        (data["Answer"] != "")
    ]

    data = data.drop_duplicates()

    return data.to_dict(orient="records")


if not original_file.exists():
    st.error(
        "Could not find data/new_questions.csv. "
        "Check that the file is in your project."
    )
    st.stop()

try:
    all_questions = load_questions(
        str(original_file),
        original_file.stat().st_mtime_ns
    )
except Exception as error:
    st.error(f"Could not load questions: {error}")
    st.stop()

if not all_questions:
    st.warning("Your trivia CSV contains no valid questions.")
    st.stop()

# ---------------------------------
# SESSION STATE
# ---------------------------------

# Create a unique identifier for each question/answer pair
def question_id(card):
    return (card["Question"], card["Answer"])


if "learned_ids" not in st.session_state:
    st.session_state.learned_ids = set()

if "current_card" not in st.session_state:
    st.session_state.current_card = None

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "card_started" not in st.session_state:
    st.session_state.card_started = time.time()

if "auto_reveal" not in st.session_state:
    st.session_state.auto_reveal = True


def get_remaining():
    return [
        card for card in all_questions
        if question_id(card)
        not in st.session_state.learned_ids
    ]


def next_card():
    remaining = get_remaining()

    if not remaining:
        st.session_state.current_card = None
    else:
        # Avoid immediately repeating the same card
        previous = st.session_state.current_card

        choices = [
            card for card in remaining
            if card != previous
        ]

        if not choices:
            choices = remaining

        st.session_state.current_card = random.choice(choices)

    st.session_state.show_answer = False
    st.session_state.card_started = time.time()


def mark_known():
    card = st.session_state.current_card

    if card is not None:
        st.session_state.learned_ids.add(
            question_id(card)
        )

    next_card()


def reset_progress():
    st.session_state.learned_ids = set()
    st.session_state.current_card = None
    next_card()


if st.session_state.current_card is None and get_remaining():
    next_card()

# ---------------------------------
# APPLICATION STYLING
# ---------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #B1DDC6;
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    .flashcard {
        background: white;
        border-radius: 22px;
        padding: 45px 30px;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        margin: 20px 0;
    }

    .flashcard.answer {
        background: #245A52;
        color: white;
    }

    .card-label {
        font-size: 22px;
        font-weight: 500;
        margin-bottom: 20px;
    }

    .card-text {
        font-size: clamp(24px, 4vw, 38px);
        font-weight: 700;
        line-height: 1.4;
        overflow-wrap: anywhere;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 55px;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# HEADER
# ---------------------------------

st.title("🧠 Trivia Flashcards")

st.write(
    "Test your knowledge with interactive trivia questions. "
    "Mark questions you know and keep practicing the rest!"
)

total = len(all_questions)
remaining = get_remaining()
completed = total - len(remaining)

col1, col2, col3 = st.columns(3)

col1.metric("Total Questions", total)
col2.metric("Learned", completed)
col3.metric("Remaining", len(remaining))

st.progress(completed / total)

st.divider()

# ---------------------------------
# SETTINGS
# ---------------------------------

st.toggle(
    "Automatically reveal answer after 3 seconds",
    key="auto_reveal"
)

# ---------------------------------
# FLASHCARD DISPLAY
# ---------------------------------

if not remaining:

    st.success("🎉 Congratulations! All trivia questions completed!")

    st.balloons()

    if st.button("🔄 Start Over"):
        reset_progress()
        st.rerun()

else:

    card = st.session_state.current_card

    if st.session_state.show_answer:
        label = "Answer"
        content = card["Answer"]
        card_class = "flashcard answer"
    else:
        label = "Question"
        content = card["Question"]
        card_class = "flashcard"

    # Escape user-supplied CSV content before inserting into HTML
    from html import escape

    st.markdown(
        f"""
        <div class="{card_class}">
            <div class="card-label">{label}</div>
            <div class="card-text">{escape(content)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------------
    # ANSWER REVEAL
    # ---------------------------------

    if not st.session_state.show_answer:

        if st.button("👁️ Reveal Answer"):
            st.session_state.show_answer = True
            st.rerun()

        if st.session_state.auto_reveal:
            elapsed = time.time() - st.session_state.card_started

            if elapsed < 3:
                time.sleep(3 - elapsed)

            st.session_state.show_answer = True
            st.rerun()

    # ---------------------------------
    # ANSWER BUTTONS
    # ---------------------------------

    col_left, col_right = st.columns(2)

    with col_left:
        if st.button(
            "❌ Don't Know",
            use_container_width=True
        ):
            next_card()
            st.rerun()

    with col_right:
        if st.button(
            "✅ I Know This",
            use_container_width=True
        ):
            mark_known()
            st.rerun()

    st.divider()

    if st.button("🔄 Restart All Questions"):
        reset_progress()
        st.rerun()

# ---------------------------------
# FOOTER
# ---------------------------------

st.caption(
    "Built with Python, Streamlit, and Pandas. "
    "Progress is saved for the current browser session."
)
