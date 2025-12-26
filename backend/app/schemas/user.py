from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# [基礎模型]：所有 User 相關操作都會有的共用欄位
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    alert: Optional[bool] = False
    admin: Optional[bool] = False


# [建立模型]：註冊時，這些欄位是必填的 (Password 是這時候才傳進來)
class UserCreate(UserBase):
    username: str
    email: EmailStr
    name: str
    password: str


# [更新模型]：更新時，所有欄位都是選填的 (Optional)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    alert: Optional[bool] = None


# [更新模型]：更新時.給管理員用的 (繼承上面，並外加特權欄位)
class UserUpdateAdmin(UserUpdate):
    email: Optional[EmailStr] = None  # 管理員可以改 Email
    username: Optional[str] = None  # 管理員可以改帳號
    admin: Optional[bool] = None  # 管理員可以提拔別人


# [回應模型]：這是回傳給前端看的 (絕對不能包含 Password!)
class UserResponse(BaseModel):
    id: int
    created: datetime
    username: str
    email: EmailStr
    name: str

    # 這是 Pydantic V2 的設定，讓它可以直接讀取 SQLAlchemy 的物件
    mode_config = ConfigDict(from_attributes=True)
