backend/
├── cli/
│   ├── __init__.py          # 1. 套件識別
│   ├── __main__.py          # 2. 模組執行入口 (python -m cli)
│   ├── main.py              # 3. 腳本執行入口 (python cli/main.py)
│   ├── setup/
│   │   ├── __init__.py      # 4. 空檔案
│   │   └── interactive.py   # 5. [邏輯] 互動式問答與 DB 寫入
│   └── cmd/
│       ├── __init__.py      # 6. 空檔案
│       ├── root.py          # 7. [註冊] 定義 Help Panel 分組
│       ├── migrate.py       # 8. [指令] 資料庫遷移 (邏輯分離)
│       ├── setup.py         # 9. [指令] 串接遷移與互動邏輯
│       └── server.py        # 10. [指令] 啟動伺服器 (大字體面板)