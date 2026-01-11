import asyncio

import typer
from rich.console import Console

from backend.app.crud.crud_user import daoUser_instan

# 動態匯入 app 模組 (因為 main.py 已經修正路徑，這裡可以直接 import app)
from backend.app.db.session import AsyncSessionLocal
from backend.app.schemas.user import UserCreate

console = Console()


def interactive_setup():
    """
    執行互動式安裝流程：詢問使用者並建立管理員
    """
    console.print("\n[bold cyan]👤 Admin User Setup[/bold cyan]")

    # 1. 問是否要建立使用者 (Typer Confirm)
    if not typer.confirm("❓ Do you want to create an Admin user?", default=True):
        return

    # 2. 收集資訊 (Typer Prompt)
    username = typer.prompt("Enter Username", default="admin")
    email = typer.prompt("Enter Email", default="admin@example.com")
    password = typer.prompt("Enter Password", hide_input=True, confirmation_prompt=True)
    name = typer.prompt("Enter Full Name", default="Admin")

    # 3. 執行建立 (Rich Status 轉圈圈)
    # 使用 try-except 確保 async 錯誤也能被捕獲
    try:
        with console.status(
            "[bold green]Creating admin user...[/bold green]", spinner="dots"
        ):
            asyncio.run(_create_admin_logic(username, email, password, name))
    except Exception as e:
        console.print(f"❌ [bold red]Error creating user:[/bold red] {e}")


async def _create_admin_logic(username, email, password, name):
    async with AsyncSessionLocal() as session:
        # 檢查是否已存在
        existing = await daoUser_instan.get_by_email(session, email=email)
        if existing:
            console.print(
                f"⚠️  [yellow]User {email} already exists. Skipping creation.[/yellow]"
            )
            return

        user_in = UserCreate(
            username=username, email=email, password=password, name=name, admin=True
        )
        await daoUser_instan.create(session, obj_in=user_in)

        console.print(
            f"✅ [bold green]Admin user '{username}' created successfully![/bold green]"
        )
