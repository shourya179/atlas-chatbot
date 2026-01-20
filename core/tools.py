import os 
import requests

# NOTE: Tool execution is experimental and intentionally limited


WORKSPACE_DIR  ="workspace"

os.makedirs(WORKSPACE_DIR,exist_ok=True)


def write_file(filename: str, content: str) -> str:
    try:
        os.makedirs(WORKSPACE_DIR, exist_ok=True)  # 🔥 THIS LINE FIXES IT

        path = os.path.join(WORKSPACE_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File '{filename}' created successfully in workspace."
    except  Exception as e :
        return f"⚠️ File write failed: {str(e)}"  

def web_search(query : str) ->str:
    """
    simple web search using DuckDuckGo (no API key required)
    """     

    try:
        url= "https://google.com/html/"
        params = {"q":query}
        responce = requests.get(url,params=params,timeout=120)

        if responce.status_code != 200:
            return "web search failed."
        
        return f"search results fetched for:{query}"
    except Exception as e:
        return f"web search error:{e}"
    
def generate_code(prompt: str) -> str:
    """
    Dummy code generator (LLM will refine later)
    """
    return (
        "# Generated code\n"
        f"# Prompt: {prompt}\n\n"
        "def main():\n"
        "    print('Hello from generated code')\n\n"
        "if __name__ == '__main__':\n"
        "    main()\n"
    )


def summarize(text: str) -> str:
    """
    Simple summarizer (placeholder)
    """
    sentences = text.split(".")
    return ".".join(sentences[:3]) + "."

def list_tools():
    """
    Returns metadata about available tools.
    used by the tool selector (LLM or rule based). 
    """
    return {
        "web_search":{
            "description":"search the web for recent or factual information."
        },
        "generate_code": {
            "description": "Generate example code or project templates."
        },
        "write_file": {
            "description": "Write content to a file in the workspace."
        },
        "summarize": {
            "description": "Summarize long text into key points."
        }
    }
    