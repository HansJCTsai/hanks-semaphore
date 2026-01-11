import typer
from rich.console import Console

# 引用 Setup 的互動層
from backend.cli.setup.interactive import interactive_setup

# 引用 Migrate 的邏輯層 (注意：是 apply_migrations_logic，不是 upgrade)
from .migrate import apply_migrations_logic

app = typer.Typer(help="Perform interactive setup", rich_markup_mode="rich")
console = Console()


@app.command(
    "run",
    help="Start [bold cyan]Interactive Setup[/bold cyan] (Migrate DB + Create Admin)",
    epilog="[dim]Example:[/dim]\n  [green]python cli/main.py setup run[/green]",
)
def run():
    """Start interactive setup (Migrate DB + Create Admin)"""

    console.rule("[bold cyan]🚀 Semaphore Setup Wizard[/bold cyan]")

    # 1. 執行遷移
    try:
        with console.status(
            "[bold blue]🔄 1/2 Running Migrations...[/bold blue]", spinner="dots"
        ):
            apply_migrations_logic()
        console.print("✅ [bold green]Database migrations applied.[/bold green]")
    except Exception as e:
        console.print(
            f"❌ [bold red]Setup aborted:[/bold red] Migration failed.\n[dim]{e}[/dim]"
        )
        raise typer.Exit(1)

    console.print()  # 空一行

    # 2. 互動式建立使用者 (邏輯在 interactive.py)
    interactive_setup()

    console.rule("[bold green]✨ Setup Complete[/bold green]")
    console.print("\nYou are all set! You can now start the server with:")
    console.print("    [cyan]python cli/main.py server start[/cyan]\n")
