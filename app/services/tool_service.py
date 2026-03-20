import json
import random
from datetime import datetime


def get_current_datetime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def convert_temperature(value: float, from_unit: str, to_unit: str) -> str:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    to_celsius = {
        "celsius": lambda v: v,
        "fahrenheit": lambda v: (v - 32) * 5 / 9,
        "kelvin": lambda v: v - 273.15,
    }
    from_celsius = {
        "celsius": lambda v: v,
        "fahrenheit": lambda v: v * 9 / 5 + 32,
        "kelvin": lambda v: v + 273.15,
    }

    if from_unit not in to_celsius or to_unit not in from_celsius:
        return "Error: unsupported unit. Use celsius, fahrenheit, or kelvin."

    celsius = to_celsius[from_unit](value)
    result = from_celsius[to_unit](celsius)
    return f"{result:.2f} {to_unit}"


def generate_random_number(min_value: int, max_value: int) -> str:
    return str(random.randint(min_value, max_value))


def is_palindrome(text: str) -> str:
    cleaned = text.lower().replace(" ", "")
    result = cleaned == cleaned[::-1]
    return f"'{text}' is {'a palindrome' if result else 'not a palindrome'}"


available_functions = {
    "get_current_datetime": get_current_datetime,
    "calculate": calculate,
    "convert_temperature": convert_temperature,
    "generate_random_number": generate_random_number,
    "is_palindrome": is_palindrome,
}


def execute_tool_call(tool_call):
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    return function_to_call(**function_args)
