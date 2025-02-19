# Virtual Tutor

A conversational math tutoring application that provides step-by-step explanations for mathematical problems.

## Overview

Virtual Tutor is a Streamlit-based chat application that helps users understand mathematical concepts through interactive conversation. The application processes user queries, breaks down mathematical problems into steps, and renders both text explanations and LaTeX formulas for clear understanding.

## Features

- Conversational interface for asking math questions
- Step-by-step problem solving with detailed explanations
- LaTeX rendering for mathematical expressions
- Persistent chat history
- Simple, user-friendly interface

## Installation

### Prerequisites

- Python 3.11+
- Conda package manager

### Setup

1. Clone the repository to your local machine

2. Create and activate the Conda environment:
```
conda env create -f environment.yml
conda activate virtual_tutor
```

3. Launch the application:
```
python -m streamlit run src/main.py
```

## Usage

1. After launching the application, a chat interface will appear in your browser
2. Type your math question in the input field at the bottom
3. The virtual tutor will respond with step-by-step explanations
4. Mathematical formulas will be rendered in LaTeX format for clarity
5. Your chat history is saved automatically between sessions

## Interface Elements

- **Main Chat Window**: Displays conversation history with the tutor
- **Input Field**: Enter your math questions here
- **Sidebar**: Contains utility functions like clearing chat history

## Customization

The application saves chat history to a `chat_history.json` file in the root directory. You can clear the history using the "Clear Chat History" button in the sidebar.

## Troubleshooting

If you encounter issues:
- Verify that you've activated the correct Conda environment
- Ensure all dependencies are properly installed
- Check that the file paths in the application are correct for your system
