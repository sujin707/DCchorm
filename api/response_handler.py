
'''
    用于接收数据，对响应的数据做处理，主要用于断言操作

'''
import json


def handle_login_response(response,testname):
    all_tokens = []
    all_uids = []
    msg = ''
    if response.get('code') == 200:
        token = response.get('data',{}).get('code')
        uid = response.get('data',{}).get('uid')
        all_tokens.append(token)
        all_uids.append(uid)
        print(f'{testname},获取到的uid：{uid}，鉴定码：{token}')
    elif response.get('code') == 400:
        msg = response.get('msg')
        print(f'{testname},错误信息:{msg}')
    else:
        print(f'{testname},响应数据:{response}')

    return all_tokens,all_uids,msg


# 获取用户信息
def handle_getinfo_response(response,testname):
    userinfo=[]
    if response.get('code') ==200:
        data = response.get('data',{})
        userinfo.append(data)
        print(f"{testname}获取到的用户信息{data}")
    else:
        print(f"{testname},获取设备列表失败，响应数据：{response}")

    # print(online_ids)
    return userinfo

# 获取登录设备的设备信息
def handle_getdevices_response(response,testname):
    all_online = []
    online_ids=[]
    if response:
        for item in response:
            online_ids.append(item)
        all_online.extend(online_ids)
        print(f"{testname}，返回的设备ID是{all_online}")
    else:
        print(f"{testname},获取设备列表失败，响应数据：{response}")


    return online_ids

# 删除为否的设备ID
def handle_forcelogout_response(response,testname):
    devices=[]
    if response.get('deleted') is True:
        device = response.get('devices',{})
        devices.append(device)
    else:
        print(f"{testname},获取设备列表失败，响应数据：{response}")
    print(devices)

    return devices


# 获取云同步的版本配置
def handle_getconfigs_response(response,name):
    versions = []
    if response.get('status') == 1:
        version = response.get('info',{}).get('version')
        versions.append(version)
        print(f'{name}获取云同步版本、配置成功，版本号：{version}')
    else:
        print(f'{name}获取云同步版本、配置失败，响应数据是{response}')

    return versions

# 更新云同步的版本配置
def handle_updateconfigs_response(response,name):
    info =[]
    if response.get('status') == 1:
        info = response.get('info')
        print(f'{name}获取云同步版本、配置成功，版本号：{info}')
    else:
        print(f'{name}获取云同步版本、配置失败，响应数据是{response}')
    return info

# 获取各大版本
def handle_setversion_response(response,name):
    infos = []
    if response.get('status') == 1:
        info = response.get('info',{})
        infos.append(info)
        print(f'{name}获取云同步版本、配置成功，版本号：{info}')
    else:
        print(f'{name}获取云同步版本、配置失败，响应数据是{response}')

    return infos

# 获取插件版本
def handle_extension_response(response,name):
    extensions = []
    if response.get('msg') == 'success':
        extension = response.get('data',{})
        extensions.append(extension)
        print(f'{name}获取插件成功，版本号：{extension}')
    else:
        print(f'{name}获取插件失败，响应数据是{response}')

    return extensions

# 获取恢复页面的书签历史版本
def handle_bookmarklist_response(response,name):
    json_response = json.dumps(response)
    data = json.loads(json_response)
    bookmarklists = []
    if data.get('status') == 1:
        bookmarklist = data.get('info',{})
        bookmarklists.append(bookmarklist)
        print(f'{name}用例获取书签历史版本成功，版本号：{bookmarklist}')
    else:
        print(f'{name}用例获取书签历史版本失败，响应数据是{response}')

    return bookmarklists

# 拉取云端的最新数据
def handle_syncpull_response(response,name):
    pulldata = []
    if response.get('status') == 1:
        info = response.get('info',{})
        pulldata.append(info)
        print(f'{name}用例拉取云端数据成功，版本号：{json.dumps(info,indent=4)}')
    else:
        print(f'{name}用例拉取云端数据失败，响应数据是{response}')

    return pulldata

# 上传云端更新数据
def handle_syncpush_response(response,name):
    pushdata = []
    if response.get('status') == 1:
        info = response.get('info',{})
        pushdata.append(info)
        print(f'{name}用例上传云端成功，响应数据：{json.dumps(info,indent=4)}')
    else:
        print(f'{name}用例上传云端失败，响应数据是{response}')

    return pushdata

# 恢复最新的书签数据
def handle_recoverbookmark_response(response,name):
    recoverbookmark = []
    if response.get('status') == 1:
        data = response.get('data',{})
        recoverbookmark.append(data)
        print(f'{name}用例恢复书签数据成功，响应：{data}')
    else:
        print(f'{name}用例恢复书签数据失败，响应数据是{response}')

    return recoverbookmark

# 查看书签数据
def handle_recover_bookmarkpull_response(response,name):
    info = []
    if response.get('message') == 'success':
        data = response.get('info',{})
        info.append(data)
        print(f'{name}用例查看书签数据成功，响应：{data}')
    else:
        print(f'{name}用例查看书签数据失败，响应数据是{response}')

    return info

# 删除书签数据
def handle_recover_bookmarkremove_response(response,name):
    info = []
    if response.get('info') == 'success':
        data = response.get('info',{})
        info.append(data)
        print(f'{name}用例删除书签数据成功，响应：{data}')
    else:
        print(f'{name}用例删除书签数据失败，响应数据是{response}')

    return info

# 上传密码数据
def handle_sync_push_pwd_response(response,name):
    info = []
    if response.get('info') == 'yes':
        data = response.get('info',{})
        info.append(data)
        print(f'{name}用例上传密码数据成功，响应：{data}')
    else:
        print(f'{name}用例上传密码数据失败，响应数据是{response}')

    return info