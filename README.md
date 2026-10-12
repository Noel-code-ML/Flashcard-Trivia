# Flashcard-Trivia
Trivia game for holiday groups.

# Trivia Flashcard Learning App

### Python | Tkinter | Pandas | CSV Data Management

## Project Overview

An interactive, desktop-based trivia flashcard application developed using Python, Tkinter, and Pandas. The application helps users expand their general knowledge by presenting trivia questions, facts, and answers through randomized flashcards, automatic card flipping, and progress tracking.

The application dynamically loads trivia content from a CSV dataset, tracks completed questions, and automatically incorporates new trivia questions when the dataset is updated.

## Key Features

- **Interactive Trivia Flashcards:** Displays trivia questions, terms, or facts with corresponding answers.
- **Automatic Card Flipping:** Reveals the answer after three seconds.
- **Randomized Questions:** Randomly selects trivia flashcards to create varied learning sessions.
- **Progress Tracking:** Saves completed trivia questions and excludes them from future sessions.
- **Dynamic Trivia Updates:** Automatically recognizes newly added questions from the master CSV file.
- **Persistent Learning Data:** Maintains progress between application sessions using CSV files.
- **User-Friendly Interface:** Provides an intuitive graphical interface with interactive buttons.
- **Long-Question Support:** Wraps longer trivia questions and answers for improved readability.
- **Completion Detection:** Displays a completion message when all trivia flashcards have been completed.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Graphical user interface |
| Pandas | CSV processing and data management |
| Random | Randomized trivia selection |
| OS | File existence checks |
| CSV | Trivia question storage and progress tracking |

## How the Application Works

**1. Trivia Data Loading**

The application loads trivia questions and answers from a CSV dataset using Pandas. Each row represents a trivia question, fact, or term and its corresponding answer.

**2. Flashcard Presentation**

A randomly selected trivia question appears on the front of a flashcard. After three seconds, the card automatically flips to reveal the answer.

**3. User Interaction**

Users select one of two buttons:

- **Known (✓):** Marks the trivia question as completed, removes it from the active learning list, and saves progress.
- **Unknown (✗):** Advances to another flashcard while keeping the question available for future review.

**4. Progress Persistence**

The application automatically saves completed questions and remaining trivia in separate CSV files, allowing progress to continue across sessions.

**5. Dynamic Trivia Management**

Users can add, modify, or remove trivia questions in the master CSV file. The application loads the updated dataset each time it starts.

## Project Structure

```text
trivia-flashcard-app/
│
├── main.py
│
├── data/
│   ├── trivia_words.csv
│   ├── words_to_learn.csv
│   └── learned_words.csv
│
├── images/
│   ├── card_front.png
│   ├── card_back.png
│   ├── right.png
│   └── wrong.png
│
├── requirements.txt
└── README.md
```

*Note: `words_to_learn.csv` and `learned_words.csv` are generated during use and may not exist in a fresh installation. File names can be customized to reflect trivia terminology.*

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/trivia-flashcard-app.git
```

**2. Navigate to the project directory**

```bash
cd trivia-flashcard-app
```

**3. Install dependencies**

```bash
pip install pandas
```

Tkinter is included with most standard Python installations.

**4. Run the application**

```bash
python main.py
```

A desktop window will open displaying the trivia flashcard application.

## Customizing Trivia Questions

Users can replace or expand the trivia dataset by editing `data/trivia_words.csv`.

Example:

```csv
Question,Answer
"What is the capital of Australia?","Canberra"
"Which planet is known as the Red Planet?","Mars"
"What is the chemical symbol for gold?","Au"
"Who painted the Mona Lisa?","Leonardo da Vinci"
"What is the largest ocean on Earth?","Pacific Ocean"
```

The application reads the updated trivia questions when restarted.

**Important:** The CSV column names must match the keys used in the Python code. For example, if the dataset uses `Question` and `Answer`, the flashcard display logic must reference those column names rather than `French` and `English`.

## Technical Implementation

The application demonstrates several fundamental software development concepts:

- **Event-Driven Programming:** Tkinter callbacks manage user interactions and flashcard transitions.
- **Data Processing:** Pandas converts CSV datasets into Python dictionaries for application use.
- **State Management:** Maintains the current trivia question, active question list, and completed questions.
- **File Persistence:** Stores learning progress locally without requiring a database.
- **Randomized Algorithms:** Uses random selection to vary the order of trivia questions.
- **Timer Management:** Uses Tkinter's `after()` scheduling mechanism for automatic card flipping.
- **Dynamic Data Loading:** Reconciles the current trivia dataset with previously completed questions.
- **Error Handling:** Handles empty learning lists and missing progress files.

## Potential Future Enhancements

- Add multiple trivia categories, such as history, science, geography, sports, and entertainment.
- Introduce difficulty levels and timed trivia challenges.
- Implement a scoring system and performance analytics.
- Add multiple-choice questions and answer validation.
- Create a dashboard showing accuracy, completion rates, and learning progress.
- Add user profiles and leaderboards.
- Introduce AI-generated trivia questions using an LLM API.
- Deploy a browser-accessible version using Streamlit.

## Skills Demonstrated

Python Development • GUI Development • Data Processing • Pandas • Event-Driven Programming • File I/O • Data Persistence • Application State Management • CSV Processing • Randomization • User Experience Design

## License

This project is available for educational and portfolio purposes. See the repository's license file for applicable usage permissions, if provided.
