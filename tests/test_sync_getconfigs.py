from http.client import responses

import pytest
from requests import session

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_getconfigs_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

'''
    获取同步设置里面的配置信息，比如设置了书签和密码的同步，取消勾选扩展同步 ，这个页面的设置数据
    {
    "status":1,
    "info":{
        "version":105,             ----版本
        "sync_settable_types":31   ----31表示权限的组合
    }
}

    代码权限配置：【从右往左看二进制，10111表示扩展没开】
    enum·SettableType·{
    SETTABLE_TYPE_NONE   =·0，
    SETTABLE_TYPE_BOOKMARKS =.1·<<·0,
    SETTABLE_TYPE_NORMAL    =·1·<く.1,
    SETTABLE_TYPE_PASSWORDSS    =·1·<く.2,
    SETTABLE_TYPE_EXTENSION =·1·<<·3,
    SETTABLE_TYPE_NOTE  =·1.<く·4,

'''


@pytest.mark.parametrize('configs',load_yaml_data('sync_configs.yaml'))
@pytest.mark.order(5)
def test_sync_getconfig(configs):
    token,uid,session = get_global_token_uid()
    token, uid = effective_token_uid(token,uid)

    method = configs.get('request',{}).get('method')
    url = configs.get('request',{}).get('url')
    name = configs.get('name')
    testCaseId = configs.get('testCaseId')

    if not validate_login_data(method,url,name):
        pytest.skip(f'{name}缺少某些数据，跳过后续代码')

    body_data = {
        'uid':uid,
        'code':token
    }

    test_http = HttpRequest(url,session)
    getconfigapi = LoginApi(test_http)
    responses= getconfigapi.get_config_id(method=method,data = body_data,headers=None,form_data=True)

    # 断言
    versions = handle_getconfigs_response(responses,name)
    print(testCaseId)
    assert versions,f'{versions}未返回有效值'
