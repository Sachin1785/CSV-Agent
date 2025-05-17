# CSV Agent

A simple AI agent built with LangChain and Google's Gemini API that manipulates CSV data through natural language instructions.

## Features

- Add/remove rows or columns
- Set cell values
- Filter and query data
- Natural language interface

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. Ensure you have a CSV file ready (a sample.csv is included)

## Usage

### CLI Interface

1. Run the command line interface:
   ```
   python main.py
   ```

2. Example commands:
   - "Add a column named Salary with default value 0"
   - "Remove columns: customer id, phone 1, phone 2, email"
   - "Add a new row with Name as Alice, Age as 29"
   - "Remove row 2"
   - "Set the City value for row 1 to San Francisco"

3. Type 'exit' or 'quit' to close the application

## Dependencies

- langchain - Agent framework
- langchain-google-genai - Gemini integration
- pandas - CSV data handling
- colorama - CLI formatting
- python-dotenv - Environment variable management