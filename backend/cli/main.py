import os
import sys

# ---------------------------------------------------------
# [關鍵] 路徑修正
# 確保 backend 目錄在 sys.path 中，這樣所有檔案都能 import app.*
# ---------------------------------------------------------
cli_dir = os.path.dirname(os.path.abspath(__file__))  # .../backend/cli
backend_dir = os.path.dirname(cli_dir)  # .../backend
sys.path.append(backend_dir)

from backend.cli.cmd.root import app

if __name__ == "__main__":
    app()
