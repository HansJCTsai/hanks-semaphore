package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	// 匯入我們即將建立的 server 邏輯套件
	webAPI "hanks-semaphore/internal/server"
)

// 1. init() 函式：自動註冊此命令
func init() {
	// 將 serverCmd 作為一個子命令，加到 rootCmd (定義在 root.go) 上
	rootCmd.AddCommand(serverCmd)

	// 這裡我們可以為 'server' 命令添加本地的 flags --port 9000 or -p 9000
	serverCmd.Flags().StringP("port", "p", "8080", "伺服器監聽的埠號")
}

// 2. serverCmd 變數：定義 'server' 子命令
var serverCmd = &cobra.Command{
	Use:     "server",
	Short:   "以伺服器模式啟動 Hanks_Semaphore 後端",
	Aliases: []string{"S", "s"}, // 仿效 semaphore，'S' 也可以用
	Long:    `啟動後端 API 伺服器、WebSocket 服務以及任務排程器。`,

	// 3. Run 函式：當 'hanks-semaphore server' 被執行時的動作
	Run: func(cmd *cobra.Command, args []string) {

		fmt.Println("正在啟動後端伺服器 (Backend Server)...")

		// 4. (修改) 從旗標中「讀取」port 的值
		// "port" 必須和 .Flags().StringP(...) 中的名稱 "port" 一致
		port, err := cmd.Flags().GetString("port")
		if err != nil {
			fmt.Printf("讀取 port 旗標失敗: %v\n", err)
			return // 發生錯誤時退出
		}
		// 我們呼叫 internal/server 套件中的 StartServer() 函式
		// (我們將在下一步建立這個函式)
		if err := webAPI.StartServer(port); err != nil {
			fmt.Printf("啟動伺服器失敗: %v\n", err)
		}
	},
}
