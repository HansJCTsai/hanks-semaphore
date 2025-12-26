# [修正] 將模組匯入為 user，這樣可以用 crud.user.func() 呼叫
from . import crud_user as user
