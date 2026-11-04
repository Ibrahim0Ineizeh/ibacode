from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file
from collections.abc import Iterable
import json
from collections.abc import Callable

available_functions: Iterable[ChatCompletionToolUnionParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name: str = tool_call.function.name
    function_args: dict = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if (tool_call.type == "function") and (tool_call.function.name not in function_map):
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown function: {function_name}",
            }
    else:
        function_args["working_directory"] = "./calculator"
        function_to_call = function_map[function_name]
        result = function_to_call(**function_args)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }
