import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.internal import generate_content

def main():
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    client = genai.Client(api_key=api_key)
    if not args:
        print("error: no prompt given")
        print('Example usage: python3 main.py "your prompt here" [--verbose]')
        sys.exit(1)
    user_prompt = " ".join(args)
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print("\n#############################################################################")
        print(f"User prompt: {user_prompt}")
    
    generate_content(client, messages, verbose)


if __name__ == "__main__":
    main()
    