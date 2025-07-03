from app.schemas.common import ResponseModel

def success(data=None, msg="成功"):
    return ResponseModel(code=0, msg=msg, data=data)

def fail(msg="失败", code=400, data=None):
    return ResponseModel(code=code, msg=msg, data=data) 