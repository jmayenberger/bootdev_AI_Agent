import os
from google import genai
from google.genai import types
from functions.llm_callables import get_file_content, get_files_info, run_python_file, write_file
from config import WORKING_DIRECTORY, MODEL, SYSTEM_PROMPT, AVAILABLE_FUNCTIONS

# calls a function with the function_call from the LLM
def call_function(function_call_part, verbose, supress):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args["working_directory"] = WORKING_DIRECTORY
    if verbose:
        print_args = ""
        for key in function_args:
            print_args += key + "=" + function_args[key] + ", "
        print(f"System: Calling function: {function_name}({print_args})\n")
    elif not supress:
        print(f"System:  - Calling function: {function_name}\n")
    
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
            if verbose:
                print(f"System: Error: Unknown function: {function_name}\n")
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
def generate_content(client, messages, verbose, supress):
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[AVAILABLE_FUNCTIONS],
            )
        )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}") # type: ignore
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}") # type: ignore
        if response.function_calls:
            text_parts = [part.text for part in response.candidates[0].content.parts if part.text]
            for text in text_parts:
                print(f'Model: "{text}"\n')
    for candidate in response.candidates:
        messages.append(candidate.content)

    function_call_results = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose, supress)
        if function_call_result.parts[0].function_response.response: # type: ignore
            function_call_results.append(function_call_result.parts[0]) #type: ignore
            if not supress:
                print(f'Tool: "Here is the result of of {function_call_part.name}"\n')
            if verbose:
                print(f"System:")
                print(f"{function_call_result.parts[0].function_response.response["result"]}\n") # type: ignore
            
        else:
            raise Exception("Unexpected error: function call without response")
    
    messages.append(types.Content(role="tool", parts=function_call_results))

    return response, messages

