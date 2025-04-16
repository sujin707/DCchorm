import json
from http.client import responses
from urllib.parse import urlencode

import pytest
from requests import session

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import  handle_updateconfigs_response
from api.service import get_sync_getconfig, get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('updateconfigs',load_yaml_data('sync_updateconfigs.yaml'))
@pytest.mark.order(3)
def test_sync_updateconfigs(updateconfigs):
    token, uid, session = get_global_token_uid()

    token, uid = effective_token_uid(token, uid)

    method = updateconfigs.get('request',{}).get('method')
    url = updateconfigs.get('request',{}).get('url')
    name = updateconfigs.get('name')
    testCaseId = updateconfigs.get('testCaseId')

    if not validate_login_data(method, url, name):
        pytest.skip(f"{name}用例缺少数据")

    versions = get_sync_getconfig()
    version = versions[0] + 2
    body_data_data = {
        "sync_settable_types": 17,
        "version": version
    }
    data_str = json.dumps(body_data_data, ensure_ascii=False)

    qdata = updateconfigs.get('request', {}).get('data')
    query_data = qdata
    body_data = {
        'uid': uid,
        'supported_settable_types': '31',
        'code': token,

        'data': data_str
    }
    print(body_data)


    query_str = urlencode(query_data)
    if '?' in url:
        url = f"{url}&{query_str}"
    else:
        url = f"{url}?{query_str}"

    test_http = HttpRequest(url, session)
    updateconfigapi = LoginApi(test_http)
    response= updateconfigapi.update_config(method=method,data=body_data,headers=None,form_data=True)

    # 断言
    info = handle_updateconfigs_response(response,name)
    print(testCaseId)
    assert info,f'{info}未返回有效值'
