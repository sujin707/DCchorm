
def validate_login_data(method,url,name):
    if not (method and url ):
        print(f"{name},缺少某部分数据")
        return False
    return True