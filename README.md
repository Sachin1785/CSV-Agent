# CSV Agent

A simple AI agent built with LangChain and Google's Gemini API that manipulates CSV data through natural language instructions.

[![CSV Agent Demo](https://img.youtube.com/vi/fflrzwJb-BI/0.jpg)](https://youtu.be/fflrzwJb-BI)

## Demo
Watch the [video demonstration](https://youtu.be/fflrzwJb-BI) to see the CSV Agent in action.

## Features

- Add/remove rows or columns
- Set cell values
- Filter and query data
- Natural language interface
- Web-based Streamlit interface with live data preview
- Command history and chat-like interaction

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

### Web Interface (Recommended)

1. Run the Streamlit web application:
   ```
   cd Streamlit
   streamlit run app.py
   ```

2. Open the provided URL in your browser
3. Enter your Gemini API key in the sidebar
4. Upload a CSV file using the file uploader
5. Use the chat interface to interact with your data
   
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
- streamlit - Web interface and data visualization