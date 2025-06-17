import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import WORKING_DIRECTORY, SYSTEM_PROMPT, AVAILABLE_FUNCTIONS

def main():
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    if not args:
        print("error: no prompt given")
        print('Example usage: python3 main.py "your prompt here" [--verbose]')
        sys.exit(1)
    user_prompt = " ".join(args)
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[AVAILABLE_FUNCTIONS],
            )
        )
    if verbose:
        print_verbose(user_prompt, response, model)
    if response.text:
        print(response.text)
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")


def print_verbose(user_prompt, response, model):
    print("\n#############################################################################")
    print(f"User prompt: {user_prompt}")
    print("\n#############################################################################")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") # type: ignore
    print("\n#############################################################################")
    print(f"Given answer by {model}:")


if __name__ == "__main__":
    main()
    