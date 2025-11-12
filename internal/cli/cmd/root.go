package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

// rootCmd 代表 'hanks-semaphore' 這個根命令
var rootCmd = &cobra.Command{
	Use:   "hanks-semaphore",
	Short: "一個仿作 Semaphore 的 DevOps 協調器",
	Long: `Hanks_Semaphore 是一個 Go 語言仿作專案，
用於學習 Go 後端、Angular 前端以及 WebSocket 通訊。`,
	// 如果子命令執行出錯，Cobra 會自動顯示錯誤，但不會顯示用法(Usage)
	SilenceUsage: true,
}

// Execute 函式 (由 cmd/hanks-semaphore/main.go 呼叫)
// 這是 Cobra 應用程式的啟動點
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

// init() 函式會在套件被載入時自動執行
// 我們會在未來的步驟中，在這裡註冊 'server' 和 'runner' 子命令
func init() {
	// 範例： cobra.OnInitialize(initConfig)
}
