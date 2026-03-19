# Document Summarizer + Action Extractor

## What This Is
A CLI tool that takes any business document (PDF, Word, or plain text)
and returns a structured analysis: plain-English summary, action items
with owners, key decisions made, and open questions flagged.

Built as a demo project for Antoine Tabet's AI consulting practice.
Target audience: 10–200 person SMBs in non-risk-averse industries
(manufacturing, operations, sales teams).

## Tech Stack
- Python 3.11+
- Claude API (claude-sonnet-4-5) via the `anthropic` Python SDK
- `pypdf` for PDF parsing
- `python-docx` for Word document parsing
- `rich` for clean terminal output
- `typer` for the CLI interface

## Project Structure
```
doc-summarizer/
├── CLAUDE.md
├── main.py          # CLI entry point
├── parser.py        # Document parsing (PDF, DOCX, TXT)
├── analyzer.py      # Claude API calls and prompt logic
├── output.py        # Formatting and displaying results
├── requirements.txt
└── samples/         # Sample documents for testing
```

## Input / Output Spec

**Input:** Any of:
- A PDF file path
- A .docx Word file path
- A .txt plain text file path

**Output (printed to terminal, clean formatted):**
1. **Summary** — 3–5 sentence plain-English overview
2. **Action Items** — bulleted list, each with: task, owner (if
   mentioned), deadline (if mentioned)
3. **Key Decisions** — what was decided or concluded in the document
4. **Open Questions** — things flagged as unresolved or needing
   follow-up

## How to Run
```bash
pip install -r requirements.txt
python main.py path/to/document.pdf
python main.py path/to/report.docx
```

## Git Conventions — STRICT

**Identity:** All commits must be made as `tabetant`. Before any
commit, verify with:
```bash
git config user.name "tabetant"
git config user.email "antoine.tabet@mail.utoronto.ca"
```
Never commit as "Claude" or any other author. Never use
`--author` flags to override this.

**Branches:**
- Create a new branch for each feature or component
- Use meaningful names with standard prefixes:
  - `feat/pdf-parser` — new feature
  - `feat/cli-interface` — new feature
  - `fix/encoding-error` — bug fix
  - `refactor/prompt-logic` — refactor
- Never name branches after Claude, sessions, or timestamps
- Work directly in the root project folder on the branch —
  no subdirectories per branch, no `claude/` folders

**Commits and merges:**
- Only commit when something works and is tested
- Only merge to main when the feature is complete and verified
- Write commit messages that describe what changed and why,
  not who made them

## API Usage — Important
- During development, mock Claude API responses with static test
  output instead of making real API calls. Only use real API calls
  for final integration testing.
- Never run the tool in an automated loop or batch test without
  asking me first.
- When testing is needed, use the shortest possible input document.
- Use claude-haiku-4-5 for development/testing. Switch to
  claude-sonnet-4-5 only for the final demo version.