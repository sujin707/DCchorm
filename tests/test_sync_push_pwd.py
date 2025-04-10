# import base64
# import json
# from urllib.parse import urlencode
#
# import pytest
#
# from api.data_validator import validate_login_data
# from api.login_api import LoginApi
# from api.response_handler import   handle_sync_push_pwd_response
# from api.service import get_global_token_uid, get_sync_pull, get_sync_getconfig
# from utils.datas_validator import effective_token_uid
# from utils.file_utils import load_yaml_data
# from utils.http_utils import HttpRequest
#
# '''
#     只操作更新密码数据
# '''
#
# @pytest.mark.parametrize('push',load_yaml_data('sync_push.yaml'))
# def test_sync_push(push):
#     token,uid,session = get_global_token_uid()
#     token,uid = effective_token_uid(token,uid)
#
#     method = push.get('request',{}).get('method')
#     url = push.get('request', {}).get('url')
#     name = push.get('name')
#     testCaseId = push.get('testCaseId')
#     data = push.get('request', {}).get('data')
#
#     if not validate_login_data(method,url,name):
#         pytest.skip(f"{name}用例缺少数据")
#
#
#     infodata = get_sync_pull()
#     passwords = infodata.get('settings',{}).get('passwords',{})
#     new_password ={'content':'WwogICAgewogICAgICAgICJhY3Rpb24iOiJodHRwczovL3d3dy4xNjMuY29tLyIsCiAgICAgICAgImJsb2NrZWRfYnlfdXNlciI6ZmFsc2UsCiAgICAgICAgIm9yaWdpbiI6Imh0dHA6Ly8xMTkuMjMuMjI0LjIwNzo5MDAwL3Ntcy1hZG1pbi9sb2dpbi5odG1sIiwKICAgICAgICAicGFzc3dvcmRfZWxlbWVudCI6InBhc3N3b3JkIiwKICAgICAgICAicGFzc3dvcmRfdmFsdWUiOiJ3YW5neWkiLAogICAgICAgICJzaWdub25fcmVhbG0iOiJodHRwOi8vMTE5LjIzLjIyNC4yMDc6OTAwMC8iLAogICAgICAgICJ1c2VybmFtZV9lbGVtZW50IjoidXNlck5hbWUiLAogICAgICAgICJ1c2VybmFtZV92YWx1ZSI6Im1pbmciCiAgICB9Cl0='}
#     # 解码
#     decoded_passwords = json.loads(base64.b64decode(passwords['content']).decode('utf-8'))
#     decoded_new_password = json.loads(base64.b64decode(new_password['content']).decode('utf-8'))
#     # 合并数据
#     merged_data = decoded_passwords + decoded_new_password
#     # 将合并后的数据编码为 base64
#     merged_data_str = json.dumps(merged_data).encode('utf-8')
#     pwd_64 = base64.b64encode(merged_data_str).decode('utf-8')
#
#     versions = infodata.get('versions',{}) # 各类版本，没有云同步的版本号
#     if 'passwords' in versions:
#         versions['passwords'] += 1
#     result = {
#         'settings':{
#             'passwords':{
#                 'content':pwd_64
#             }
#         },
#         'versions':{
#             **versions,
#             'extension':0
#         }
#     }
#     book_data = json.dumps(result,ensure_ascii=False)
#
#
#     query_data = data
#     query_str = urlencode(query_data)
#     if '?' in url:
#         url = f"{url}&{query_str}"
#     else:
#         url = f"{url}?{query_str}"
#
#     version = get_sync_getconfig()
#     body_data ={
#         'uid':uid,
#         'config_version':version,
#         'spversion':2,
#         'types':63,
#         'code':token,
#         'data':book_data
#     }
#
#     test_http = HttpRequest(url,session)
#     syncpullapi = LoginApi(test_http)
#     responses= syncpullapi.push(method=method,data= body_data,headers=None,form_data=True)
#
#     # # 断言
#     push_pwd = handle_sync_push_pwd_response(responses,name)
#     print(testCaseId)
#     assert push_pwd,f'{name}用例未返回有效数据'