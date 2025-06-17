import os
from google import genai
from google.genai import types
from functions.llm_callables import get_file_content, get_files_info, run_python_file, write_file
from config import WORKING_DIRECTORY, MODEL, SYSTEM_PROMPT, AVAILABLE_FUNCTIONS

# calls a function with the function_call from the LLM
def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_directory"] = WORKING_DIRECTORY
    if verbose:
        print(f"Calling function: {function_name}({' '.join(function_args)})")
    else:
        print(f" - Calling function: {function_name}")
    
    match function_name:
        case "get_file_content":
            function_result = get_file_content(**function_args)
        case "get_files_info":
            function_result = get_files_info(**function_args)
        case "write_file":
            function_result = write_file(**function_args)
        case "run_python_file":
            function_result = run_python_file(**function_args)
        case _:
            print(f"Error: Unknown function: {function_name}")
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"Error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

# give the LLM a prompt and generate the content
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[AVAILABLE_FUNCTIONS],
            )
        )
    if verbose:
        print("\n#############################################################################")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}") # type: ignore
        print("\n#############################################################################")
        print(f"Returned result by {MODEL}:")
    if response.text:
        print(response.text)
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if function_call_result.parts[0].function_response.response: # type: ignore
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}") # type: ignore
            else:
                raise Exception("Unexpected error: function call without response")

