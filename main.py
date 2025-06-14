import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    verbose = False

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"
    if len(sys.argv) <= 1:
        print("error: no prompt given")
        exit(1)
    if len(sys.argv) > 2:
        if "--verbose" in sys.argv[2:]:
            verbose = True
    user_prompt = sys.argv[1]
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model=model, contents=messages)
    if verbose:
        print_verbose(user_prompt, response, model)
    print(response.text)


def print_verbose(user_prompt, response, model):
    print("\n#############################################################################")
    print(f"User prompt: {user_prompt}")
    print("\n#############################################################################")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") # type: ignore
    print("\n#############################################################################")
    print(f"Given answer by {model}:")


if __name__ == "__main__":
    main()
    