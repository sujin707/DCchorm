from http.client import responses

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_getdevices_response
from api.service import get_global_token_uid
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('getdevice',load_yaml_data('getdevices.yaml'))
@pytest.mark.order(2)
def test_getdevices(getdevice):
    token ,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)


    method = getdevice.get('request',{}).get('method')
    url = getdevice.get('request', {}).get('url')
    testname = getdevice.get('name')
    testCaseId = getdevice.get('testCaseId')

    uuids = load_yaml_data('login.yaml')
    uuid = uuids[0].get('request',{}).get('data', {}).get('uuid')

    body_data = {
        'uid':uid,
        'code':token,
        'uuid':uuid
    }

    # 缺少一个数据则不执行剩下代码
    if not validate_login_data(method, url,testname):
        pytest.skip(f"{testname}用例的数据不完整，跳过该用例的测试")

    test_http = HttpRequest(url,session)
    getdevicesapi = LoginApi(test_http)
    response = getdevicesapi.get_equipment_id(method=method,params=body_data,headers=None,form_data = True)

    online_ids = handle_getdevices_response(response,testname)
    assert online_ids,f"{testname}响应结果中包含online_id"

