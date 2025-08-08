from typing import Any, List, Optional
from pathlib import Path
import json

from mcp.server.fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("kjv-local-json")


# Filenames in the working directory
BOOKS_INDEX_FILENAME = "Books.json"
BOOKS_CHAPTER_COUNT_FILENAME = "bible_book_chapters.json"


def _resolve_workspace_path(filename: str) -> Path:
    """Resolve a filename within the workspace.

    Prefer the current working directory; fall back to the directory of this file.
    """
    cwd_path = Path.cwd() / filename
    if cwd_path.exists():
        return cwd_path
    here_path = Path(__file__).resolve().parent / filename
    return here_path


def _load_json_file(filename: str) -> Any:
    """Load and return JSON from a file in the workspace (verbatim)."""
    path = _resolve_workspace_path(filename)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_book_name(book: str) -> str:
    """Normalize a provided book spec to the canonical JSON filename.

    Accepts inputs like "Genesis", "Genesis.json", "1 John", "1John", or "1_John"
    (case-insensitive) and returns an existing filename (e.g., "1John.json") when possible.
    Uses `Books.json` to align casing and tries several filename variants.
    """
    raw = book.strip()
    base = raw[:-5] if raw.lower().endswith(".json") else raw

    def _variants_for(title: str) -> List[str]:
        # Try canonical, no-spaces, and underscores variants
        names = [title, title.replace(" ", ""), title.replace(" ", "_")]
        return [f"{n}.json" for n in names]

    # Try to align with Books.json for canonical casing, then probe variants that exist on disk
    try:
        books: List[str] = _load_json_file(BOOKS_INDEX_FILENAME)
        for b in books:
            if b.lower().replace(" ", "") == base.lower().replace(" ", ""):
                for filename in _variants_for(b):
                    if _resolve_workspace_path(filename).exists():
                        return filename
                # If none of the variants exist, still return canonical to surface a clear error
                return f"{b}.json"
    except Exception:
        pass  # Fall through to input-based variants

    # If not found via index, try variants derived from the input itself
    for filename in _variants_for(base):
        if _resolve_workspace_path(filename).exists():
            return filename

    # Fallback: trust provided name as-is
    return f"{base}.json"


@mcp.tool()
def list_books() -> List[str]:
    """Return the list of available book names from `Books.json`."""
    books: List[str] = _load_json_file(BOOKS_INDEX_FILENAME)
    return books


@mcp.tool()
def get_book_json(book: str) -> Any:
    """Return the verbatim JSON content for the specified book.

    - Input may be the book title (e.g., "Genesis") or a filename (e.g., "Genesis.json").
    - Output is the parsed JSON content exactly as stored on disk.
    """
    filename = _normalize_book_name(book)
    return _load_json_file(filename)


@mcp.tool()
def get_books_chapter_count() -> Any:
    """Return the verbatim JSON content of `Books_chapter_count.json`."""
    return _load_json_file(BOOKS_CHAPTER_COUNT_FILENAME)


if __name__ == "__main__":
    # Run the MCP server over stdio
    mcp.run(transport="stdio")