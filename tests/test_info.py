from http.client import responses

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import  handle_getinfo_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('userinfo',load_yaml_data('userinfo.yaml'))
def test_userinfos(userinfo):
    token ,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)


    method = userinfo.get('request',{}).get('method')
    url = userinfo.get('request', {}).get('url')
    testname = userinfo.get('name')
    testCaseId = userinfo.get('testCaseId')
    data = userinfo.get('request', {}).get('data')

    headers = {
        "Content-Type": "application/json",
        'Authorization': f'Bearer {token}'
    }

    # 缺少一个数据则不执行剩下代码
    if not validate_login_data(method, url,testname):
        pytest.skip(f"{testname}用例的数据不完整，跳过该用例的测试")

    test_http = HttpRequest(url,session)
    userinfo = LoginApi(test_http)
    response = userinfo.get_user_info(method=method,data=data,headers=headers)

    online_ids = handle_getinfo_response(response,testname)
    assert online_ids,f"{testname}响应结果中包含online_id"

