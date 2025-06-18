import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.internal import generate_content
from config import MAX_ITERATIONS

def main():
    # initialize
    verbose = "--verbose" in sys.argv
    interactive = "--interactive" in sys.argv
    supress = "--supress" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if not args:
        print("Error: no prompt given")
        print('Example usage: python3 main.py "your prompt here" [--verbose][--interactive][--supress]')
        sys.exit(1)
    user_prompt = " ".join(args)
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if not supress:
        print("\n#############################################################################")
        print(f'User: "{user_prompt}"\n')
    
    # start LLM loop
    for i in range(MAX_ITERATIONS):
        response, messages= generate_content(client, messages, verbose, supress)
        if not response.function_calls:
            if response.text:
                print(f'\nModel: "{response.text}"')
                break
            else:
                print(f'System: "No response from Model - exit"')
                break
        elif i == MAX_ITERATIONS:
            print(f"\nSystem: Feedback Loop aborted because max_iterations={MAX_ITERATIONS} reached")
        if interactive:
            user_prompt = input()
            if len(user_prompt) > 0:
                messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))
                if verbose:
                    print("User injection: " + user_prompt + "\n")
        


if __name__ == "__main__":
    main()
    