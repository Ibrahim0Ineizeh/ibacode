import argparse
import os
import json
import sys
from collections.abc import Iterable

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion_message import ChatCompletionMessage
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_system_message_param import ChatCompletionSystemMessageParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from prompts import system_prompt
from call_function import available_functions
from call_function import call_function

def main():

    # Create a parser object and add an argument then get all arguments
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args: argparse.Namespace = parser.parse_args()

    # Load dotenv objects then get the API key for the open ai API
    load_dotenv()
    api_key: str | None  = os.environ.get("OPENROUTER_API_KEY")

    # Check if it does exist
    if api_key == None:
        raise RuntimeError("The API key for the LLM was not found!")

    # Create a client using the API key
    client: OpenAI | None = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Creat a message log for providing the agent with history
    messages: list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        # Get a response for the user prompt from the agent
        response: ChatCompletion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        response_message: ChatCompletionMessage = response.choices[0].message
        # Check if a response was provided
        if response.usage is not None:
            prompt_tokens: int = response.usage.prompt_tokens
            response_tokens: int = response.usage.completion_tokens
        else:
            raise RuntimeError("Failed API request!")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        messages.append(response_message)

        if response_message.tool_calls != None:
            for tool_call in response_message.tool_calls:
                if tool_call.type == "function":
                    result = call_function(tool_call=tool_call, verbose=args.verbose)
                    if result['content'] != "":
                        if args.verbose:
                            print(f"-> {result['content']}")

                        messages.append(result)
                    else:
                        raise RuntimeError("Error: no function is returned.")
        else:
            print(f"Response:\n{response.choices[0].message.content}")
            break
    else:
        print("Error: the agent couldn't get a final solution")
        sys.exit(1)

if __name__ == "__main__":
    main()
