import os

import typer
from alembic import command
from alembic.config import Config
from rich.console import Console

app = typer.Typer(help="Database migration commands", rich_markup_mode="rich")
console = Console()


def get_alembic_config():
    # 取得 backend 根目錄
    # logic: cli/cmd/migrate.py -> cli/cmd -> cli -> backend
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    ini_path = os.path.join(base_dir, "alembic.ini")
    script_location = os.path.join(base_dir, "alembic")

    if not os.path.exists(ini_path):
        raise FileNotFoundError(f"alembic.ini not found at {ini_path}")

    alembic_cfg = Config(ini_path)
    alembic_cfg.set_main_option("script_location", script_location)
    return alembic_cfg


# ==========================================
# 🧠 純邏輯層 (Logic Layer) - 給 setup.py 用的
# ==========================================
def apply_migrations_logic():
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


def create_revision_logic(message: str):
    alembic_cfg = get_alembic_config()
    command.revision(alembic_cfg, message=message, autogenerate=True)


# ==========================================
# 🎨 介面層 (CLI Layer)
# ==========================================


@app.command(
    "up",
    help="Apply all pending migrations ([bold green]Upgrade Head[/bold green])",
    epilog="[dim]Example:[/dim]\n  [green]python cli/main.py migrate up[/green]",
)
def upgrade():
    """Apply all pending migrations"""
    try:
        with console.status(
            "[bold blue]🔄 Running Database Migrations...[/bold blue]", spinner="dots"
        ):
            apply_migrations_logic()
        console.print("✅ [bold green]Database is up to date.[/bold green]")
    except Exception as e:
        console.print(f"❌ [bold red]Migration failed:[/bold red] {e}")
        raise typer.Exit(1)


@app.command(
    "make",
    help="Generate a new migration script based on [bold yellow]SQLAlchemy Models[/bold yellow]",
    epilog='[dim]Example:[/dim]\n  [green]python cli/main.py migrate make -m "add_user_table"[/green]',
)
def makemigrations(
    message: str = typer.Option(..., "-m", "--message", help="Migration description"),
):
    """Generate a new migration file"""
    try:
        with console.status(
            f"[bold blue]📝 Generating migration: {message}...[/bold blue]",
            spinner="dots",
        ):
            create_revision_logic(message)
        console.print("✅ [bold green]Migration script created.[/bold green]")
    except Exception as e:
        console.print(f"❌ [bold red]Failed to generate:[/bold red] {e}")
        raise typer.Exit(1)
