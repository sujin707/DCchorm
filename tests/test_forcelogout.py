from http.client import responses

import pytest

from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_getdevices_response, handle_forcelogout_response
from api.service import get_global_token_uid, get_getdevices
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest


@pytest.mark.parametrize('forcelogout',load_yaml_data('forcelogout.yaml'))
def test_forcelogout(forcelogout):
    token ,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)


    method = forcelogout.get('request',{}).get('method')
    url = forcelogout.get('request', {}).get('url')
    testname = forcelogout.get('name')
    testCaseId = forcelogout.get('testCaseId')

    all_online = get_getdevices()
    for item in all_online:
        is_current = item.get('is_current')
        if is_current is False:
            online_id = item.get('online_id')

            body_data = {
                'uid':uid,
                'online_id':online_id,
                'code':token
            }

            # 缺少一个数据则不执行剩下代码
            if not validate_login_data(method, url,testname):
                pytest.skip(f"{testname}用例的数据不完整，跳过该用例的测试")

            test_http = HttpRequest(url,session)
            forcelogoutapi = LoginApi(test_http)
            response = forcelogoutapi.del_equipment_id(method=method,data=body_data,headers=None)

            devices = handle_forcelogout_response(response,testname)
            assert devices,f"{testname}响应结果中不包含devices"

        else:
            online_id = item.get('online_id')
            print(f"获取到的是本机设备ID：{online_id},无非本机设备ID，不走退出其他设备流程")
