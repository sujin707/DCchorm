from urllib.parse import urlencode

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_extension_response, handle_bookmarklist_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

'''
{
    "status":1,
    "info":{
        "archivelist":[
            {
                "add_time":"2025-04-01 16:31:15",
                "device_name":"",
                "id":"2323603_20250401163115",
                "pcnum":2,
                "appnum":0
            }
        ],
        "today":[
            {
                "add_time":"2025-04-02 15:13:20",
                "device_name":"DESKTOP-47E8L17",
                "id":"2323603_20250402151320",
                "pcnum":3,
                "appnum":0
            }
        ],
        "deltime":""
    }
}
'''

@pytest.mark.parametrize('bookmarkslist',load_yaml_data('sync_bookmarkslist.yaml'))
def test_bookmarkslist(bookmarkslist):
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    method = bookmarkslist.get('request',{}).get('method')
    url = bookmarkslist.get('request', {}).get('url')
    data = bookmarkslist.get('request', {}).get('data')
    name = bookmarkslist.get('name')
    testCaseId = bookmarkslist.get('testCaseId')
    query_data = data
    body_data ={
        'uid':uid,
        'types':1,
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



    # 断言
    bookmarklists = handle_bookmarklist_response(responses,name)
    assert bookmarklists,f'{name}用例未返回有效数据'