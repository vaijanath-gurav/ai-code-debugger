import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from app.executor import run_python_code

load_dotenv()

# Initialize OpenAI client pointing to Google's Free Gemini API endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

EXECUTION_TOOL = {
    "type": "function",
    "function": {
        "name": "run_python_code",
        "description": "Executes Python code and unit tests, returning standard output, errors, and exit codes.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The complete Python script or test case to execute."
                }
            },
            "required": ["code"]
        }
    }
}

SYSTEM_PROMPT = """
You are an expert AI Code Debugging Assistant.
Your workflow:
1. Analyze the user's buggy code and explain the root causes of any errors.
2. Formulate corrected code and unit test cases to verify the fix.
3. CALL the `run_python_code` tool to execute the code and unit tests.
4. If tests pass, present the final explanation, corrected code, and test results to the user.
5. If tests fail, analyze the error output, refactor, and call `run_python_code` again until resolved.
"""

def debug_code(user_code: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Please debug and verify this code:\n\n```python\n{user_code}\n```"}
    ]

    while True:
        # Using Gemini's fast free model (gemini-2.5-flash)
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=messages,
            tools=[EXECUTION_TOOL],
            tool_choice="auto"
        )
        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for tool_call in msg.tool_calls:
            if tool_call.function.name == "run_python_code":
                args = json.loads(tool_call.function.arguments)
                result = run_python_code(args["code"])
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })