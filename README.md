# CSV Agent

A simple AI agent built with LangChain and Google's Gemini API that manipulates CSV data through natural language instructions.

## Features

- Add/remove rows or columns
- Set cell values
- Natural language interface

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Example commands:
   - "Add a column named Salary with default value 0"
   - "Remove the Age column"
   - "Add a new row with Name as Alice, Age as 29"
   - "Remove row 2"
   - "Set the City value for row 1 to San Francisco"

3. Type 'exit' to quit

## Requirements

- Python 3.9+
- LangChain
- Google Generative AI package
- pandas 