

def is_valid_token(token):
    return token is not None and token.strip()!=''

def is_valid_uid(uid):
    if isinstance(uid, int):
        # 如果 uid 是整数类型，直接判断是否为 None
        return uid is not None
    elif isinstance(uid, str):
        # 如果 uid 是字符串类型，判断是否为空字符串
        return uid is not None and uid.strip() != ""
    return False

def is_valid_uuid(uuid):
    return uuid is not None and uuid.strip() != ''

# 处理多个
def filter_valid_tokens_and_uids(tokens, uids):
    valid_tokens = [token for token in tokens if is_valid_token(token)]
    valid_uids = [uid for uid in uids if is_valid_uid(uid)]
    return valid_tokens, valid_uids

# 处理单个
def effective_token_uid(token, uid):
    # 只进行验证，不修改 token 和 uid
    if token and uid:
        return token, uid
    return None, None
