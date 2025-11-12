package handlers

import (
	"encoding/json"
	"net/http"
	"time"

	dto "hanks-semaphore/db/dto/task" // 匯入我們剛剛建立的 DTO

	"github.com/google/uuid"
	"github.com/gorilla/mux"
)

// CreateTaskHandler 處理 POST /api/tasks
// @Summary      建立一個新任務
// @Description  接收 JSON body 來建立一個新的待處理任務
// @Tags         Tasks
// @Accept       json
// @Produce      json
// @Param        task  body      dto.TaskDTO  true  "要建立的任務資訊 (目前僅為範例，未來會簡化)"
// @Success      201   {object}  dto.TaskDTO  "成功建立的任務"
// @Failure      400   {string}  string       "無效的請求"
// @Router       /tasks [post]
func CreateTaskHandler(w http.ResponseWriter, r *http.Request) {
	// 1. (未來) 解析 request body...
	// ...

	// 2. (暫時) 建立一個「假」的 Task DTO 來回傳
	newTask := dto.TaskDTO{
		ID:        uuid.New().String(),
		Status:    "pending",
		Playbook:  "deploy.yml",
		CreatedAt: time.Now(),
	}

	// 4. 回傳 "201 Created"
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(newTask)
}

// GetTaskHandler 處理 GET /api/tasks/{task_id}
// @Summary      取得一個特定任務
// @Description  根據 task_id 取得單一任務的詳細資訊
// @Tags         Tasks
// @Produce      json
// @Param        task_id   path      string       true  "任務 ID"
// @Success      200       {object}  dto.TaskDTO  "成功取得的任務"
// @Failure      400       {string}  string       "無效的 ID"
// @Failure      404       {string}  string       "找不到任務"
// @Router       /tasks/{task_id} [get]
func GetTaskHandler(w http.ResponseWriter, r *http.Request) {

	// 1. 從 URL 路徑中取得 "task_id"
	vars := mux.Vars(r)
	taskID, ok := vars["task_id"]
	if !ok {
		http.Error(w, "Missing task_id", http.StatusBadRequest)
		return
	}

	// 2. (未來) 呼叫 taskService.GetByID(taskID) ...

	// 3. (暫時) 建立一個「假」的 Task DTO 來回傳
	foundTask := dto.TaskDTO{
		ID:        taskID,
		Status:    "running",
		Playbook:  "deploy.yml",
		CreatedAt: time.Now().Add(-5 * time.Minute),
		StartedAt: func() *time.Time { t := time.Now().Add(-1 * time.Minute); return &t }(),
	}

	// 4. 回傳 "200 OK"
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(foundTask)
}
