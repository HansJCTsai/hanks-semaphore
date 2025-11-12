package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

func init() {
	// 將 runnerCmd 作為一個子命令，加到 rootCmd (定義在 root.go) 上
	rootCmd.AddCommand(runnerCmd)

	// 這裡我們可以為 'runner' 命令添加本地的 flags --runner 1 or -r 1
	runnerCmd.Flags().StringP("job", "j", "1", "Runner 執行器的識別碼")
}

var runnerCmd = &cobra.Command{
	Use:     "runner",
	Short:   "以執行器模式啟動 Hanks_Semaphore 後端",
	Aliases: []string{"R", "r"},
	Long:    `啟動任務執行器，負責從佇列中取出任務並執行。`,
	Run: func(cmd *cobra.Command, args []string) {
		runnerJobNo, err := cmd.Flags().GetString("job")
		if err != nil {
			fmt.Printf("讀取 runner 旗標失敗: %v\n", err)
			return // 發生錯誤時退出
		}
		fmt.Printf("正在啟動後端伺服器%v\n (Backend Server)...", runnerJobNo)
	},
}
