get_current_datetime_schema = {
    "type": "function",
    "function": {
        "name": "get_current_datetime",
        "description": "Get the current date and time",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}

calculate_schema = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluate a mathematical expression and return the result",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A valid Python math expression, e.g. '2 ** 10' or '(3 + 5) * 2'",
                }
            },
            "required": ["expression"],
        },
    },
}

convert_temperature_schema = {
    "type": "function",
    "function": {
        "name": "convert_temperature",
        "description": "Convert a temperature value between Celsius, Fahrenheit, and Kelvin",
        "parameters": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "The temperature value to convert",
                },
                "from_unit": {
                    "type": "string",
                    "description": "The unit to convert from: celsius, fahrenheit, or kelvin",
                },
                "to_unit": {
                    "type": "string",
                    "description": "The unit to convert to: celsius, fahrenheit, or kelvin",
                },
            },
            "required": ["value", "from_unit", "to_unit"],
        },
    },
}

generate_random_number_schema = {
    "type": "function",
    "function": {
        "name": "generate_random_number",
        "description": "Generate a random integer between min_value and max_value (inclusive)",
        "parameters": {
            "type": "object",
            "properties": {
                "min_value": {
                    "type": "integer",
                    "description": "The minimum value (inclusive)",
                },
                "max_value": {
                    "type": "integer",
                    "description": "The maximum value (inclusive)",
                },
            },
            "required": ["min_value", "max_value"],
        },
    },
}

is_palindrome_schema = {
    "type": "function",
    "function": {
        "name": "is_palindrome",
        "description": "Check if a string is a palindrome",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The string to check",
                }
            },
            "required": ["text"],
        },
    },
}

tools = [
    get_current_datetime_schema,
    calculate_schema,
    convert_temperature_schema,
    generate_random_number_schema,
    is_palindrome_schema,
]
