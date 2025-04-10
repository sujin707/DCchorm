'''
    用于返回数据给其他方法调用

'''
import json
import random
import uuid
from urllib.parse import urlencode
import pytest
import requests
from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import (
    handle_login_response,
    handle_getdevices_response,
    handle_getconfigs_response,
    handle_setversion_response,
    handle_extension_response, handle_bookmarklist_response, handle_syncpull_response, handle_getinfo_response
)
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

# 全局变量用于存储 token、uid 和 session
GLOBAL_TOKEN = None
GLOBAL_UID = None
GLOBAL_SESSION = None


def get_global_token_uid():
    global GLOBAL_TOKEN, GLOBAL_UID, GLOBAL_SESSION
    if GLOBAL_TOKEN is None or GLOBAL_UID is None or GLOBAL_SESSION is None:
        session = requests.Session()
        login_data = load_yaml_data('login.yaml')
        if not login_data:
            return None, None, None

        for item in login_data:
            request_data = item.get('request', {})
            method = request_data.get('method')
            url = request_data.get('url')
            body_data = request_data.get('data')
            testname = item.get('name')

            if not validate_login_data(method, url, testname):
                continue

            test_http = HttpRequest(url, session)
            login_api = LoginApi(test_http)
            response = login_api.login(data=body_data, method=method, headers=None)
            all_tokens, all_uids ,_= handle_login_response(response, testname)
            if all_tokens and all_uids:
                GLOBAL_TOKEN, GLOBAL_UID, GLOBAL_SESSION = all_tokens[0], all_uids[0], session
                break
    return GLOBAL_TOKEN, GLOBAL_UID, GLOBAL_SESSION


# 登录设备信息
def get_getdevices():
    uuiddata = load_yaml_data('login.yaml')
    first_case_data = uuiddata[0]
    uuid = first_case_data.get('request', {}).get('data', {}).get('uuid')

    token, uid, session = get_global_token_uid()
    if not all([token, uid, session]):
        return None

    getdevice = load_yaml_data('getdevices.yaml')
    for item in getdevice:
        request_data = item.get('request', {})
        method = request_data.get('method')
        url = request_data.get('url')
        testname = item.get('name')

        query_data = {
            'uid': str(uid),
            'code': token,
            'uuid': uuid
        }
        query_str = urlencode(query_data)
        if '?' in url:
            url = f"{url}&{query_str}"
        else:
            url = f"{url}?{query_str}"

        if not validate_login_data(method, url, testname):
            continue

        test_http = HttpRequest(url, session)
        getdevicesapi = LoginApi(test_http)
        response = getdevicesapi.get_equipment_id(method=method, params=query_data, headers=None, form_data=True)
        online_ids = handle_getdevices_response(response, testname)
        if online_ids:
            return online_ids
    return None


# 云同步版本信息
def get_sync_getconfig():
    token, uid, session = get_global_token_uid()
    if not all([token, uid, session]):
        return None

    sync_config = load_yaml_data('sync_configs.yaml')
    for item in sync_config:
        method = item.get('request', {}).get('method')
        url = item.get('request', {}).get('url')
        name = item.get('name')

        if not validate_login_data(method, url, name):
            pytest.skip(f'{name}数据缺失')

        body_data = {
            'uid': uid,
            'code': token
        }

        test_http = HttpRequest(url, session)
        getconfigapi = LoginApi(test_http)
        response = getconfigapi.get_config_id(method=method, data=body_data, headers=None, form_data=True)
        versions = handle_getconfigs_response(response, name)
        if versions:
            return versions
    return None


# 获取各大配置版本
def get_settingsversion():
    token, uid, session = get_global_token_uid()
    if not all([token, uid, session]):
        return None

    setversion = load_yaml_data('sync_setversion.yaml')
    for item in setversion:
        method = item.get('request', {}).get('method')
        url = item.get('request', {}).get('url')
        name = item.get('name')
        body_data = {
            'uid': uid,
            'code': token
        }

        if not validate_login_data(method, url, name):
            pytest.skip(f"{name}用例缺少数据")

        test_http = HttpRequest(url, session)
        setversionapi = LoginApi(test_http)
        responses = setversionapi.get_settingsversions(method=method, data=body_data, headers=None, form_data=True)

        infos = handle_setversion_response(responses, name)
        if infos:
            return infos
    return None


# 插件版本
def get_extensions():
    token, uid, session = get_global_token_uid()
    if not all([token, uid, session]):
        return None

    extension = load_yaml_data('sync_extension.yaml')
    for item in extension:
        method = item.get('request', {}).get('method')
        url = item.get('request', {}).get('url')
        data = item.get('request', {}).get('data')
        name = item.get('name')
        query_data = data
        body_data = {
            'uid': uid,
            'code': token
        }

        if not validate_login_data(method, url, name):
            pytest.skip(f"{name}用例缺少数据")

        query_str = urlencode(query_data)
        if '?' in url:
            url = f"{url}&{query_str}"
        else:
            url = f"{url}?{query_str}"

        test_http = HttpRequest(url, session)
        setversionapi = LoginApi(test_http)
        responses = setversionapi.get_settingsversions(method=method, data=body_data, headers=None, form_data=True)

        extensions = handle_extension_response(responses, name)
        if extensions:
            return extensions
    return None

# 拉取上传的数据
def get_sync_pull():
    pull = load_yaml_data('sync_pull.yaml')
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    for item in pull:
        method = item.get('request',{}).get('method')
        url = item.get('request', {}).get('url')
        data = item.get('request', {}).get('data')
        name = item.get('name')
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
        info = handle_syncpull_response(responses,name)
        if info:
            return info
        else:
            return None


# 上传书签数据
def post_sync_push():
    push = load_yaml_data('sync_push.yaml')
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    for item in push:
        method = item.get('request',{}).get('method')
        url = item.get('request', {}).get('url')
        name = item.get('name')
        data = item.get('request', {}).get('data')

        if not validate_login_data(method,url,name):
            pytest.skip(f"{name}用例缺少数据")

        infodata = get_sync_pull()
        bookmarks = infodata.get('settings',{}).get('bookmarks',{})

        # guid  id确保唯一就行，可随意更改,生成一个随机的GUID（版本4）
        random_guid = uuid.uuid4()
        uuid_str = str(random_guid)
        random_part = random.randint(100, 999)  # 生成一个6位数的随机数

        # 新增数据上传更新
        new_children = {
            'date_added': '13387363431517499',
            'guid': uuid_str,
            'id': random_part,
            'name': '炸弹猫',
            'type': url,
            'url': 'http://www.163.com'
        }

        childer = bookmarks.get('roots',{}).get('bookmark_bar',{}).get('children')
        if childer is not None:
            if isinstance(childer,list):
                childer.append(new_children)
            else:
                childer = [new_children]



        versions = infodata.get('versions',{}) # 各类版本，没有云同步的版本号
        if 'bookmarks' in versions and 'passwords' in versions:
            versions['bookmarks']+=1
            versions['passwords'] += 1
        result = {
            'settings':{
                'bookmarks':bookmarks
            },
            'versions':{
                **versions,
                'extension':0
            }
        }
        book_data = json.dumps(result,ensure_ascii=False)

        query_data = data
        query_str = urlencode(query_data)
        if '?' in url:
            url = f"{url}&{query_str}"
        else:
            url = f"{url}?{query_str}"

        version = get_sync_getconfig()
        body_data ={
            'uid':uid,
            'config_version':version,
            'spversion':2,
            'types':63,
            'code':token,
            'data':book_data
        }

        test_http = HttpRequest(url,session)
        syncpullapi = LoginApi(test_http)
        responses= syncpullapi.push(method=method,data= body_data,headers=None,form_data=True)

        info = get_sync_pull()
        book_datapull = info.get('settings',{}).get('bookmarks',{})
        push_book_dict = json.loads(book_data)
        push = push_book_dict.get('settings',{}).get('bookmarks',{})

        if push == book_datapull:
            print('上传的数据与拉下来数据一致，上传成功')
        else:
            print('上传失败')


# 获取恢复管理页面版本信息
def get_bookmarkslist():
    bookmarkslist = load_yaml_data('sync_bookmarkslist.yaml')
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    for item in bookmarkslist:
        method = item.get('request',{}).get('method')
        url = item.get('request', {}).get('url')
        data = item.get('request', {}).get('data')
        name = item.get('name')
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
        archivelist = handle_bookmarklist_response(responses,name)
        if archivelist:
            return archivelist
        else:
            return None


# 获取用户信息，数据可用于如：新人特惠
def get_userinfos():
    userinfo = load_yaml_data('userinfo.yaml')
    token ,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    for item in userinfo:
        method = item.get('request',{}).get('method')
        url = item.get('request', {}).get('url')
        testname = item.get('name')
        testCaseId = item.get('testCaseId')
        data = item.get('request', {}).get('data')

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
        userinfo = handle_getinfo_response(response,testname)
        if userinfo:
            return userinfo
        else:
            return None
