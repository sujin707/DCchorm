import allure
import pytest
from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_login_response
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

# 存储已处理的 testCaseId
# processed_test_case_ids = set()
# @pytest.fixture(scope="session", autouse=True)
# def clear_processed_test_case_ids():
#     global processed_test_case_ids
#     processed_test_case_ids.clear()

'''
    登录成功的用户
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    # print("Loaded test case:", login)
    # global processed_test_case_ids
    # processed_test_case_ids.clear()
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')
    testCaseId = login.get('testCaseId')


    # 检查 testCaseId 是否唯一
    # if testCaseId in processed_test_case_ids:
    #     pytest.fail(f"测试用例 {testname} 的 testCaseId {testCaseId} 重复，请检查 login.yaml 文件。")
    # processed_test_case_ids.add(testCaseId)
    #
    # allure.dynamic.testcase(testCaseId)

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")

    test_http = HttpRequest(url)
    login_api = LoginApi(test_http)
    response = login_api.login(method=method, data=body_data, headers=None)

    all_tokens, all_uids,_ = handle_login_response(response, testname)
    if response.get('code') == 200:
        assert all_tokens, f'{testname}, 未返回有效 token'
        assert all_uids, f'{testname}, 未返回有效 uid'

'''
    密码错误的用户
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")

    test_http = HttpRequest(url)
    login_api = LoginApi(test_http)
    response = login_api.login(method=method, data=body_data, headers=None)

    all_tokens, all_uids, msg = handle_login_response(response, testname)
    if response.get('code') == 400:
        assert not all_tokens and not all_uids, f'{testname}, 密码错误但仍返回了无效的token或uid'
        assert msg, f'{testname}, 登录出错'

'''
    方法为空的接口
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")
    else:
        test_http = HttpRequest(url)
        login_api = LoginApi(test_http)
        response = login_api.login(method=method, data=body_data, headers=None)

'''
    uuid 为空
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")
    else:
        test_http = HttpRequest(url)
        login_api = LoginApi(test_http)
        response = login_api.login(method=method, data=body_data, headers=None)

        if response.get('code') == 400:
            _,_,msg = handle_login_response(response,testname)
            assert msg , f'{testname}用例返回的信息不是“请求错误”的信息'

'''
    账号密码为空
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")
    else:
        test_http = HttpRequest(url)
        login_api = LoginApi(test_http)
        response = login_api.login(method=method, data=body_data, headers=None)

        if response.get('code') == 400:
            _,_,msg = handle_login_response(response,testname)
            assert msg , f'{testname}用例返回的信息不是“请求错误”的信息'

'''
    密码为空
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")
    else:
        test_http = HttpRequest(url)
        login_api = LoginApi(test_http)
        response = login_api.login(method=method, data=body_data, headers=None)

        if response.get('code') == 400:
            _,_,msg = handle_login_response(response,testname)
            assert msg , f'{testname}用例返回的信息不是“请求错误”的信息'


'''
    账号为空
'''
@pytest.mark.parametrize('login', load_yaml_data('login.yaml'))
def test_login(login):
    method = login.get('request', {}).get('method')
    url = login.get('request', {}).get('url')
    body_data = login.get('request', {}).get('data')
    testname = login.get('name')

    if not validate_login_data(method, url, testname):
        pytest.skip(f"{testname} 用例的数据不完整，跳过该用例的测试")
    else:
        test_http = HttpRequest(url)
        login_api = LoginApi(test_http)
        response = login_api.login(method=method, data=body_data, headers=None)

        if response.get('code') == 400:
            _,_,msg = handle_login_response(response,testname)
            assert msg , f'{testname}用例返回的信息不是“请求错误”的信息'
