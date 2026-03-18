from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def render_results(filename: str, results: dict) -> None:
    console.print()
    console.print(Panel(f"[bold]{filename}[/bold]", box=box.DOUBLE_EDGE))
    console.print()

    _render_summary(results.get("summary", ""))
    _render_action_items(results.get("action_items", []))
    _render_key_decisions(results.get("key_decisions", []))
    _render_open_questions(results.get("open_questions", []))


def _render_summary(summary: str) -> None:
    if summary:
        content = summary
    else:
        content = Text("None identified.", style="italic dim")
    console.print(Panel(content, title="Summary", box=box.ROUNDED, border_style="cyan"))
    console.print()


def _render_action_items(items: list) -> None:
    if not items:
        inner = Text("None identified.", style="italic dim")
    else:
        inner = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold")
        inner.add_column("Task", ratio=3)
        inner.add_column("Owner", ratio=2)
        inner.add_column("Deadline", ratio=2)
        for item in items:
            task = item.get("task", "") or ""
            owner = item.get("owner") or Text("—", style="dim")
            deadline = item.get("deadline") or Text("—", style="dim")
            inner.add_row(task, owner, deadline)

    console.print(Panel(inner, title="Action Items", box=box.ROUNDED, border_style="yellow"))
    console.print()


def _render_key_decisions(decisions: list) -> None:
    if not decisions:
        content = Text("None identified.", style="italic dim")
    else:
        content = Text()
        for i, decision in enumerate(decisions):
            content.append(f"• {decision}")
            if i < len(decisions) - 1:
                content.append("\n")
    console.print(Panel(content, title="Key Decisions", box=box.ROUNDED, border_style="green"))
    console.print()


def _render_open_questions(questions: list) -> None:
    if not questions:
        content = Text("None identified.", style="italic dim")
    else:
        content = Text()
        for i, question in enumerate(questions):
            content.append(f"• {question}")
            if i < len(questions) - 1:
                content.append("\n")
    console.print(Panel(content, title="Open Questions", box=box.ROUNDED, border_style="magenta"))
    console.print()
