package dto

import "time"

// TaskDTO 是 API 和 服務 之間傳遞的資料結構
type TaskDTO struct {
	ID         string     `json:"id"`
	Status     string     `json:"status"`
	Playbook   string     `json:"playbook"` // 例如 "deploy.yml"
	CreatedAt  time.Time  `json:"created_at"`
	StartedAt  *time.Time `json:"started_at,omitempty"` // 使用指標(pointer)來允許 null
	FinishedAt *time.Time `json:"finished_at,omitempty"`
}
