import json
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic_settings import BaseSettings

# 設定 config.json 的路徑
# 假設 config.json 位於 backend/ 根目錄 (即執行指令的目錄)
CONFIG_JSON_PATH = Path("config.json")


def load_json_config() -> Dict[str, Any]:
    """讀取 config.json 並轉換為 Settings 需要的格式"""
    if not CONFIG_JSON_PATH.exists():
        print(
            f"Warning: {CONFIG_JSON_PATH} not found, relying on environment variables."
        )
        return {}

    with open(CONFIG_JSON_PATH, encoding="utf-8") as f:
        try:
            data = json.load(f)
            postgres = data.get("postgres", {})

            # 回傳一個字典，對應 Settings 裡面的變數名稱
            return {
                "POSTGRES_SERVER": postgres.get("host"),
                "POSTGRES_USER": postgres.get("user"),
                "POSTGRES_PASSWORD": postgres.get("pass"),
                "POSTGRES_DB": postgres.get("name"),
                "POSTGRES_PORT": str(
                    postgres.get("port", 5432)
                ),  # 轉成字串以防 JSON 寫成數字
            }
        except json.JSONDecodeError:
            print("Error: Failed to decode config.json")
            return {}


class Settings(BaseSettings):
    PROJECT_NAME: str = "Hanks Semaphore API"
    API_V1_STR: str = "/api/v1"

    # 這裡給預設值 None，強迫一定要從 JSON 或環境變數讀取到，否則會報錯 (Optional 可選)
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: str = "5432"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # 確保所有必要參數都有值
        if not all(
            [
                self.POSTGRES_SERVER,
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_DB,
            ]
        ):
            raise ValueError(
                "Database configuration is missing. Please check config.json or environment variables."
            )

        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        # Pydantic 允許同時讀取 .env，如果找不到 JSON 會嘗試讀 .env
        env_file = ".env"


# 初始化時，將 JSON 的內容傳入 (**json_config 會把字典解包成參數)
json_config = load_json_config()
settings = Settings(**json_config)
