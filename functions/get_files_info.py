import os

from openai.types.chat.chat_completion_tool_union_param import ChatCompletionToolUnionParam

schema_get_files_info: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(work_dir_path, directory))
        valid_target_dir: bool = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}"as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'
        else:

            if os.path.commonpath([work_dir_path, target_dir]) != work_dir_path:
                return f"Error: {target_dir} is not in the working directory"
            elif not os.path.isdir(target_dir):
                return f"Error: {target_dir} is not a directory"
            else:
                targets_items : list[str] = []
                for f in os.listdir(target_dir):
                    targets_items.append(f"- {f}: file_size={os.path.getsize(os.path.join(target_dir, f))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, f))}")
                return "\n".join(targets_items)

    except RuntimeError as e:
        raise RuntimeError(f"Error: {e}")
