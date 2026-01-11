import typer

from backend.cli.cmd import migrate, server, setup

# [關鍵] 啟用 rich 模式，讓 help 支援顏色
app = typer.Typer(help="Semaphore Backend CLI Manager", rich_markup_mode="rich")

# ---------------------------------------------------------
# 使用 add_typer 時，加上 rich_help_panel 進行分組
# ---------------------------------------------------------

# 1. Setup 指令 -> 分類到 "Initialization"
app.add_typer(setup.app, name="setup", rich_help_panel="🚀 Initialization")

# 2. Migrate 指令 -> 分類到 "Database Management"
app.add_typer(migrate.app, name="migrate", rich_help_panel="📦 Database Management")

# 3. Server 指令 -> 分類到 "System Operations"
app.add_typer(server.app, name="server", rich_help_panel="⚙️ System Operations")
