from core import tools


def execute_tool(tool_name: str, input_data: str) -> str:
    try:
        if tool_name == "web_search":
            return tools.web_search(input_data)

        if tool_name == "write_file":
            return tools.write_file("output.txt", input_data)

        if tool_name == "generate_code":
            return tools.generate_code(input_data)

        if tool_name == "summarize":
            return tools.summarize(input_data)

        return "Unknown tool."
    except Exception as e:
        return f"⚠️ tool error:{str(e)}"