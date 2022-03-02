<h2 align="center">Wordle Solver</h2>

![demo gif](https://github.com/nexxeln/wordle-solver/blob/main/images/wordle-solver-demo.gif?raw=true)

## Overview

This is yet another wordle solver. It is built with the word list of the official [wordle](https://www.nytimes.com/games/wordle/index.html) website, but it should also work with most wordle websites. The algorithm is quite efficient, but it is not perfect. On playing 50 games of wordle using the solver, the average number of tries it took to guess the word is **3.86**.

## Prerequisites

- [Python 3.6](https://python.org) or later

## Installation

- Clone the repository: `https://github.com/nexxeln/wordle-solver`
- Create a new virtual environment: `python -m venv venv`
- Activate the virtual environment <br />
  - Windows: `venv/Scripts/activate`
  - Linux: `venv/bin/activate`
  - MacOS: `venv/bin/activate`
- Install the dependencies: `pip install -r requirements.txt`

## Usage

- Go to the [wordle](https://www.nytimes.com/games/wordle/index.html) website
- Run the program: `python wordle.py`
  - The solver will provide you the words to guess
  - To input the colours the convention is:
    - `x` for gray/black (letter is not in the word)
    - `y` for yellow (letter is in the word but in the wrong position)
    - `g` for greeen
  - Enter the words provided in the wordle website
  - You can also see the demo gif above
- Flex your wordle skills and share it with your friends

## Contributing

Contributions are welcome! This algorithm can definitely be even more optimized.
