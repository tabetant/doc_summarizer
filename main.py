from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Analyze business documents with Claude AI.")
console = Console()
err_console = Console(stderr=True, style="bold red")


@app.command()
def analyze(
    file_path: Path = typer.Argument(..., help="Path to the document (PDF, DOCX, or TXT)"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show extracted text length"),
):
    """Analyze a business document and extract summary, action items, decisions, and open questions."""
    if not file_path.exists():
        err_console.print(f"Error: file not found: {file_path}")
        raise typer.Exit(code=1)

    try:
        from parser import ParserError, parse_document
        from analyzer import AnalyzerError, analyze_document
        from output import render_results
    except EnvironmentError as e:
        err_console.print(f"Configuration error: {e}")
        raise typer.Exit(code=1)

    try:
        with console.status("Parsing document..."):
            text = parse_document(str(file_path))

        if verbose:
            Console(stderr=True).print(f"Extracted {len(text):,} characters.", style="dim")

        with console.status("Analyzing with Claude..."):
            results = analyze_document(text)

        render_results(file_path.name, results)

    except ParserError as e:
        err_console.print(f"Parse error: {e}")
        raise typer.Exit(code=1)
    except AnalyzerError as e:
        err_console.print(f"Analysis error: {e}")
        raise typer.Exit(code=1)
    except EnvironmentError as e:
        err_console.print(f"Configuration error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
