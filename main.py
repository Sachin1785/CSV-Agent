import os
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import colorama
from colorama import Fore, Style, Back
import time
from datetime import datetime
from csvoperations import CSVHandler
from tools import create_tools, SYSTEM_PROMPT

load_dotenv()
colorama.init()

CSV_PATH = "sample.csv"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(f"{Fore.GREEN}{'CSV AGENT CHAT INTERFACE':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📁 Currently working with: {Fore.YELLOW}{CSV_PATH}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type your instructions or 'exit' to quit{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'- ' * 30}{Style.RESET_ALL}")

def print_bot_message(message):
    timestamp = get_timestamp()
    print(f"\n{Fore.GREEN}[{timestamp}] 🤖 Bot: {Style.RESET_ALL}")
    for line in message.split('\n'):
        print(f"{Fore.CYAN}  {line}{Style.RESET_ALL}")

def print_user_message(message):
    timestamp = get_timestamp()
    print(f"\n{Fore.YELLOW}[{timestamp}] 👤 You: {Style.RESET_ALL}")
    print(f"{Fore.WHITE}  {message}{Style.RESET_ALL}")

def print_error(message):
    timestamp = get_timestamp()
    print(f"\n{Fore.RED}[{timestamp}] ❌ Error: {Style.RESET_ALL}")
    print(f"{Fore.RED}  {message}{Style.RESET_ALL}")

def main():
    if not GEMINI_API_KEY:
        print_error("GEMINI_API_KEY environment variable not found. Please set it in .env file.")
        return
        
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GEMINI_API_KEY
    )

    csv_handler = CSVHandler(CSV_PATH)
    
    tools = create_tools(csv_handler)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        agent_kwargs={
            "system_message": SYSTEM_PROMPT,
        }
    )

    print_header()
    
    # chat_history = []
    while True:
        user_input = input(f"\n{Fore.YELLOW}🗨️ You: {Style.RESET_ALL}")
        if user_input.lower() in {"exit", "quit"}:
            print(f"\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
            break
            
        # chat_history.append(("user", user_input))
        
        try:
            print(f"{Fore.GREEN}🤖 Bot: {Fore.CYAN}Thinking...{Style.RESET_ALL}", end="\r")
            response = agent.invoke({"input": user_input})["output"]
            print(" " * 50, end="\r") 
            print_bot_message(response)
            # chat_history.append(("bot", response))
        except Exception as e:
            print_error(str(e))
            # chat_history.append(("error", str(e)))

if __name__ == "__main__":
    main() 