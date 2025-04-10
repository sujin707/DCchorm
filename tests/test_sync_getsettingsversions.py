from http.client import responses

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_setversion_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

'''
    获取各大配置版本
    {
    "status":1,
    "info":{
        "bookmarks":4585,
        "mouse_gestures":41,
        "normal":261,
        "note":15,
        "ntp":50,
        "passwords":46,
        "theme":163
    }
}
'''


@pytest.mark.parametrize('setversion',load_yaml_data('sync_setversion.yaml'))
@pytest.mark.order(6)
def test_getsettingsversion(setversion):
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    method = setversion.get('request',{}).get('method')
    url = setversion.get('request', {}).get('url')
    name = setversion.get('name')
    testCaseId = setversion.get('testCaseId')
    body_data ={
        'uid':uid,
        'code':token
    }

    if not validate_login_data(method,url,name):
        pytest.skip(f"{name}用例缺少数据")

    test_http = HttpRequest(url,session)
    setversionapi = LoginApi(test_http)
    responses= setversionapi.get_settingsversions(method=method,data= body_data,headers=None,form_data=True)


    infos = handle_setversion_response(responses,name)
    assert infos,f'{name}用例未返回有效数据'


