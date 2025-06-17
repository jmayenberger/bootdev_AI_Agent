from google.genai import types

MAX_CHARS = 1e4

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

functions =  []


SCHEMA_GET_FILES_INFO = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
functions.append(SCHEMA_GET_FILES_INFO)


SCHEMA_GET_FILE_CONTENT = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns file contents at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to get the content from, relative to the working directory.",
            ),
        },
    ),
)
functions.append(SCHEMA_GET_FILE_CONTENT)


SCHEMA_RUN_PYTHON_FILE = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file at the specified file path with the given input arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(
                        type=types.Type.STRING,
                        description="An argument to pass to the file. If no arguemtn is given, file will be executed without arguments."
                    ),
                    description="List of additional arguments for file execution. If not provided, file will be executed without additional arguments.",
                ),
        },
    ),
)
functions.append(SCHEMA_RUN_PYTHON_FILE)


SCHEMA_WRITE_FILE = types.FunctionDeclaration(
    name="write_file",
    description="Writes input content to a file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to write to, relative to the working directory. If file or directories do not exist, they will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into file.",
            ),
        },
    ),
)
functions.append(SCHEMA_WRITE_FILE)


AVAILABLE_FUNCTIONS = types.Tool(function_declarations=functions)