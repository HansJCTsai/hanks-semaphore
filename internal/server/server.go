package server

import (
	"fmt"
	"log"
	"net/http"

	"hanks-semaphore/internal/server/api"
)

// 1. 修改函式簽名 (Signature)，讓它可以「接收」port 參數
func StartServer(port string) error { // <-- 參數從 ( ) 變為 (port string)

	// ... (未來初始化 db) ...

	router := api.NewRouter() // <-- 這會呼叫 router.go

	// 2. 準備監聽地址 (從 "8080" 變為 port 參數)
	//    我們在這裡為埠號加上冒號
	listenAddr := ":" + port

	// 3. 更新提示訊息 (使用 listenAddr)
	fmt.Printf("API 伺服器正在監聽 http://localhost%s\n", listenAddr)
	fmt.Printf("Swagger UI 在 http://localhost%s/swagger/index.html\n", listenAddr)

	// 4. 啟動伺服器 (使用 listenAddr)
	err := http.ListenAndServe(listenAddr, router)
	if err != nil {
		log.Printf("伺服器啟動失敗: %v", err)
		return err
	}

	return nil
}
