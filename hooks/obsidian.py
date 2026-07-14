"""
MkDocs hook — convert Obsidian-flavoured markdown to standard markdown.

Handles:
  - ![[image.png]]  / ![[file.pdf|size]]  → stripped entirely
  - [[Page|Display]]                      → Display (plain text)
  - [[Page]]                              → Page   (plain text)
  - ```dataviewjs ... ```                 → stripped entirely
  - > [!TYPE] callouts                    → MkDocs admonitions
"""

import re


# ── Obsidian image / file embeds ────────────────────────────────────
_RE_EMBED = re.compile(
    r"!\[\[.+?\]\]",
    re.DOTALL,
)

# ── Wiki-links ──────────────────────────────────────────────────────
_RE_WIKILINK = re.compile(
    r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]"
)

# ── Dataviewjs / dataview code blocks ───────────────────────────────
_RE_DATAVIEW = re.compile(
    r"```dataviewjs?\s*\n.*?```",
    re.DOTALL,
)

# ── Obsidian callouts → MkDocs admonitions ──────────────────────────
_RE_CALLOUT_START = re.compile(
    r"^> \[!(\w+)\]\s*(.*)",
    re.MULTILINE,
)

# Map Obsidian callout types to MkDocs admonition types
_CALLOUT_MAP = {
    "NOTE": "note",
    "TIP": "tip",
    "IMPORTANT": "important",
    "WARNING": "warning",
    "CAUTION": "danger",
    "INFO": "info",
    "ABSTRACT": "abstract",
    "TODO": "todo",
    "SUCCESS": "success",
    "QUESTION": "question",
    "FAILURE": "failure",
    "DANGER": "danger",
    "BUG": "bug",
    "EXAMPLE": "example",
    "QUOTE": "quote",
    "UPDATING": "warning",
}


def _convert_callouts(md: str) -> str:
    """Convert Obsidian callout syntax to MkDocs admonition syntax."""
    lines = md.split("\n")
    result = []
    i = 0
    while i < len(lines):
        match = _RE_CALLOUT_START.match(lines[i])
        if match:
            callout_type = match.group(1).upper()
            title = match.group(2).strip()
            admonition_type = _CALLOUT_MAP.get(callout_type, "note")

            if title:
                result.append(f'!!! {admonition_type} "{title}"')
            else:
                result.append(f"!!! {admonition_type}")

            i += 1
            # Collect continuation lines (lines starting with "> ")
            while i < len(lines) and lines[i].startswith("> "):
                content = lines[i][2:]  # strip "> "
                result.append(f"    {content}")
                i += 1
        else:
            result.append(lines[i])
            i += 1
    return "\n".join(result)


def on_page_markdown(markdown: str, **kwargs) -> str:
    """Process each page's markdown before rendering."""
    # 1. Strip dataviewjs / dataview blocks
    markdown = _RE_DATAVIEW.sub("", markdown)

    # 2. Strip Obsidian image / file embeds
    markdown = _RE_EMBED.sub("", markdown)

    # 3. Convert wiki-links to plain text
    markdown = _RE_WIKILINK.sub(r"\1", markdown)

    # 4. Convert callouts to admonitions
    markdown = _convert_callouts(markdown)

    return markdown
