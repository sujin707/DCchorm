from urllib.parse import urlencode

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_syncpull_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('pull',load_yaml_data('sync_pull.yaml'))
@pytest.mark.order(8)
def test_sync_pull(pull):
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    method = pull.get('request',{}).get('method')
    url = pull.get('request', {}).get('url')
    data = pull.get('request', {}).get('data')
    name = pull.get('name')
    testCaseId = pull.get('testCaseId')
    query_data = data
    body_data ={
        'uid':uid,
        'types':63,
        'code':token
    }

    if not validate_login_data(method,url,name):
        pytest.skip(f"{name}用例缺少数据")

    query_str = urlencode(query_data)
    if '?' in url:
        url = f"{url}&{query_str}"
    else:
        url = f"{url}?{query_str}"

    test_http = HttpRequest(url,session)
    syncpullapi = LoginApi(test_http)
    responses= syncpullapi.pull_book(method=method,data= body_data,headers=None,form_data=True)


    # 断言
    pulldata = handle_syncpull_response(responses,name)
    print(testCaseId)
    assert pulldata,f'{name}用例未返回有效数据'