# Wordle Guesser

## Overview

The Wordle Guesser project is a Python implementation of a Wordle guessing game. The game is facilitated by three main files:

1. **guesser.py**: This file contains the core function responsible for guessing the target word. It utilizes two datasets, one with fewer words and another with more words. The guesser searches firstly in the shorter dataset and then in the longer one.

2. **game.py**: This file provides general instructions and orchestrates the game. It sets the rules, generates random words using the `wordle.py` file, and utilizes the guesser from `guesser.py` to make guesses. If the maximum number of trials (6 by default) is exceeded, the game moves on to the next word.

3. **wordle.py**: This file generates a specified number of random words (n) and uses the guesser from `guesser.py` to attempt to guess each word. At the end of the game, it returns the accuracy and the average number of trials.

## File Structure

```
wordle-guesser/
│
├── data/
│   ├── unigram_final.csv (shorter one)
│   ├── entirewordlist.csv (longer one)
│   └── wordlist.yaml (the game randomly pick words from this list)
│
├── guesser.py
├── game.py
├── wordle.py
│
├── README.md
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.9 installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Riclaw/wordle-guesser.git
   cd wordle-guesser
   ```

## Usage

1. Run the game:
   ```bash
   python game.py --r <number_of_runs>
   ```

2. The game will utilize the guesser to attempt to guess random words, providing accuracy and average trial information at the end.

## Customization

- You can customize the datasets in the `data/` folder to include your own word lists.
- Adjust the maximum number of trials in `game.py` if needed.


Feel free to customize the content further based on your project's specifics and any additional information you'd like to include.
