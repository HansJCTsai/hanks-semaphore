package main

import (
	// 匯入我們定義的 CLI 內部套件
	// "hanks-semaphore" 是我們在 go.mod 中定義的模組名稱
	"hanks-semaphore/internal/cli/cmd"
)

// main 函式是 Go 應用程式的唯一進入點
func main() {
	// 執行 internal/cli/cmd/root.go 中定義的 Execute() 函式
	cmd.Execute()
}
