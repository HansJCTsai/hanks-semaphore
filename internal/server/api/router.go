package api

import (
	"hanks-semaphore/internal/server/handlers" // 匯入我們的 handlers
	"net/http"

	"github.com/gorilla/mux"

	// 1. 匯入 http-swagger
	httpSwagger "github.com/swaggo/http-swagger"
	// 1. (關鍵) 在這裡加入 docs 套件的匯入
	// "hanks-semaphore" 是你的 go.mod 模組名稱
	_ "hanks-semaphore/docs"
)

// NewRouter 建立並回傳一個設定好所有 API 路由的 mux.Router
func NewRouter() *mux.Router {

	r := mux.NewRouter()
	apiRouter := r.PathPrefix("/api").Subrouter()

	// --- 綁定我們的 RESTful API ---

	// 2. 綁定 CreateTask (POST /api/tasks)
	apiRouter.HandleFunc("/tasks", handlers.CreateTaskHandler).Methods("POST")

	// 3. 綁定 GetTask (GET /api/tasks/{task_id})
	apiRouter.HandleFunc("/tasks/{task_id}", handlers.GetTaskHandler).Methods("GET")

	// --- 綁定 Ping ---
	apiRouter.HandleFunc("/ping", pingHandler).Methods("GET")

	// --- 綁定 Swagger UI ---

	// 4. 建立 /swagger/ 路由
	//    我們使用 r (主路由器)，而不是 apiRouter ( /api 子路由器)
	//    這樣 Swagger 的網址就是 http://localhost:8080/swagger/
	r.PathPrefix("/swagger/").Handler(httpSwagger.WrapHandler)

	return r
}

// pingHandler 是一個簡單的 HTTP 處理器 (Handler)
func pingHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("pong"))
}
