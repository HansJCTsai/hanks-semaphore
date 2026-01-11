import typer
import uvicorn
from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(help="Server management", rich_markup_mode="rich")
console = Console()


@app.command(
    "start",
    help="Start the [bold green]FastAPI[/bold green] Server (Uvicorn)",
    epilog="[dim]Example:[/dim]\n  [green]python cli/main.py server start --reload[/green]",
)
def start(
    host: str = typer.Option("0.0.0.0", help="Host to bind"),
    port: int = typer.Option(8000, help="Port to listen"),
    reload: bool = typer.Option(False, help="Enable auto-reload (Dev mode)"),
):
    """Start the HTTP API server"""

    # 1. 系統初始化橫線
    console.rule("[bold cyan]System Initialization[/bold cyan]")

    # 2. 產生 ASCII Art
    f = Figlet(font="slant")
    big_text = f.renderText("Semaphore")

    # 3. 準備詳細資訊
    info_msg = (
        f"\n"
        f"📡 Host:   [bold cyan]{host}[/bold cyan]\n"
        f"🔌 Port:   [bold cyan]{port}[/bold cyan]\n"
        f"🔄 Reload: [bold {'green' if reload else 'yellow'}]{'Enabled' if reload else 'Disabled'}[/bold {'green' if reload else 'yellow'}]"
    )

    # 4. 組合面板內容
    panel_content = Text(big_text, style="bold magenta") + Text(info_msg)

    # 5. 顯示面板
    console.print(
        Panel(
            panel_content,
            title="[bold green]🚀 Server Running[/bold green]",
            border_style="green",
            expand=False,
        )
    )

    console.print("\n[dim]Press Ctrl+C to stop[/dim]\n")

    # 6. 啟動 Uvicorn
    uvicorn.run("app.main:app", host=host, port=port, reload=reload)
