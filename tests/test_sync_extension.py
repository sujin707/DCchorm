from urllib.parse import urlencode

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_extension_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('extension',load_yaml_data('sync_extension.yaml'))
@pytest.mark.order(4)
def test_extensions(extension):
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)


    method = extension.get('request',{}).get('method')
    url = extension.get('request', {}).get('url')
    data = extension.get('request', {}).get('data')
    name = extension.get('name')
    testCaseId = extension.get('testCaseId')
    query_data = data
    body_data ={
        'uid':uid,
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
    setversionapi = LoginApi(test_http)
    responses= setversionapi.get_settingsversions(method=method,data= body_data,headers=None,form_data=True)

    # extensions = handle_extension_response(responses,name)
    # print(testCaseId)
    # assert extensions,f'{name}用例未返回有效数据'