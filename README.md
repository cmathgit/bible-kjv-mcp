# [Bible-kjv-mcp](https://github.com/cmathgit/bible-kjv-mcp)

## MCP Server: Local KJV JSON (FastMCP)

This repository also contains a Model Context Protocol (MCP) server that serves the local JSON bible files verbatim. The server exposes simple tools to list available books and return a specific book’s JSON as-is from disk. This is a fork of the original repository [Bible-kjv](https://github.com/aruljohn/Bible-kjv) with the addition of a MCP server.

### Requirements
- Python 3.10+ (recommended 3.11 or newer)
- `uv` package manager (see `https://docs.astral.sh/uv/getting-started/installation/`)


#### Clone repositories and enter the project directory.
   ```
   git clone https://github.com/aruljohn/Bible-kjv
   git clone https://github.com/cmathgit/bible-kjv-mcp
   cd bible-kjv-mcp
   ```
Copy files from the original repository by aruljohn to the new one.
   ```
   cp -r ../Bible-kjv/*.json .
   ```

### Installation with uv
1. Initialize project:
   ```
   uv init
   ```
2. Pin Python (optional):
   ```
   uv python pin 3.13
   ```
3. Create and activate a virtual environment with uv.
   - Windows (PowerShell or CMD):
     ```
     uv venv
     .venv\Scripts\activate
     ```
   - Linux/macOS (bash/zsh):
     ```
     uv venv
     source .venv/bin/activate
     ```
4. Add dependency:
   ```
   uv add mcp[cli]
   ```
5. Minimal pyproject.toml:
   ```toml
   [project]
   name = "bible-kjv-mcp"
   version = "0.1.0"
   description = "MCP server that serves KJV Bible JSON files verbatim."
   readme = "README.md"
   requires-python = ">=3.13"
   dependencies = ["mcp[cli]>=1.12.4"]

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```
6. Check versions:
   ```
   uv --version
   python --version
   ```
7. Run:
   ```
   uv run server.py
   ```

The server runs over stdio and is intended to be launched by an MCP-compatible client (Roo Code, Cline, Cursor, Claude Desktop). Running it manually is optional.

### Configure in Roo Code, Cline, or Cursor
Add or update your MCP configuration (often `mcp.json`) to include this server. Replace paths with your absolute locations.

```json
{
  "mcpServers": {
    "bible-kjv-1611": {
      "command": "/ABSOLUTE/PATH/TO/uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/bible-kjv-1611-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

## Using the MCP Server in Cursor

Once the MCP server is configured in your Cursor `mcp.json` as described above, you can interact with it directly through Cursor's Agent mode:

1.  **Activate Agent Mode:** In your Cursor IDE, ensure you are in Agent Mode. This is typically activated through a specific UI element or command, allowing you to converse with the AI.
2.  **Select Model:** Choose the appropriate language model that supports tool calling and MCP integration.
3.  **Formulate Queries:** You can now pose natural language queries to retrieve information from the KJV 1611 Bible. The agent will automatically invoke the corresponding MCP tools (`list_books`, `get_book_json`, `get_books_chapter_count`).

    **Examples of queries:**
    *   "List the books of the kjv bible"
    *   "How many chapters are in John?"
    *   "John 8:58."
    *   "Show me John 1:1-15."

Notes:
- Some IDEs limit the combined length of the server name and tool name. If you encounter truncation issues, shorten the server key (e.g., `kjv-json`).
- The server name within the code is `kjv-1611-local-json` and the tools exposed are concise to fit common limits.

### Tools exposed by this server
- `list_books()`
  - Returns the contents of `Books.json` (array of 80 book names).
- `get_book_json(book: str)`
  - Returns the verbatim JSON for the specified book. Accepts either a title (e.g., `"Genesis"`) or a filename (e.g., `"Genesis.json"`), case-insensitive.
- `get_books_chapter_count()`
  - Returns the contents of `Books_chapter_count.json`.

### Example requests you can make to your MCP client
- “List the KJV 1611 book names.” → invokes `list_books`.
- “Return the JSON for Psalms.” → invokes `get_book_json` with `book = "Psalms"`.
- “Give me the book/chapter counts for all KJV 1611 books.” → invokes `get_books_chapter_count`.

### Data location
- The server reads JSON files from the current working directory first and falls back to the directory containing `server.py`. Keep the provided JSON files together with `server.py` (the project root) for reliable operation.

# [Bible-kjv](https://github.com/aruljohn/Bible-kjv)

+ Contains all the 66 books of the Old Testament and New Testament
+ Each book is in a separate JSON file as a JSON object
+ `Books.json` contains all 66 book names as a JSON array

> Note on numbered book filenames
> Some JSON filenames for numbered books omit spaces (e.g., `1John.json`, `2Peter.json`). The MCP server automatically resolves inputs with or without spaces or underscores (e.g., “1 John”, “1John”, “1_John”, “2 Peter”). No action or renaming is required.