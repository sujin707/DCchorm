import pytest
from urllib.parse import urlencode
from api.data_validator import validate_login_data
from api.login_api import LoginApi
from api.response_handler import handle_recoverbookmark_response, handle_recover_bookmarkpull_response
from api.service import get_global_token_uid, get_bookmarkslist
from utils.datas_validator import effective_token_uid
from utils.file_utils import load_yaml_data
from utils.http_utils import HttpRequest

@pytest.mark.parametrize('bookmarkpull',load_yaml_data('recover_bookmarkpull.yaml'))
@pytest.mark.order(11)
def test_recover_bookmarkpull(bookmarkpull):
    token,uid,session = get_global_token_uid()
    token,uid = effective_token_uid(token,uid)

    method = bookmarkpull.get('request',{}).get('method')
    url = bookmarkpull.get('request', {}).get('url')
    data = bookmarkpull.get('request', {}).get('data')
    name = bookmarkpull.get('name')
    testCaseId = bookmarkpull.get('testCaseId')


    if not validate_login_data(method,url,name):
        pytest.skip(f"{name}用例缺少数据")

    all_bid_data =get_bookmarkslist()
    if isinstance(all_bid_data,list):
        first_item = all_bid_data[0]
        today_bid_data = first_item.get('today', {})
        yes_bid_data = first_item.get('archivelist', {})
    else:
        yes_bid_data = []
        today_bid_data = []
    bid = None
    if today_bid_data :
        today_data = today_bid_data[0]
        bid = today_data.get('id')
    elif  yes_bid_data  :
        yes_data = yes_bid_data[0]
        bid = yes_data.get('id')
    else:
        print('取值失败')

    if bid is None or bid == '':
        pytest.skip(f'{name}用例没有历史的书签数据，无法查看数据')

    query_data = data
    body_data ={
        'uid':uid,
        'types':1,
        'bid': bid,
        'code':token
    }
    print(body_data)

    query_str = urlencode(query_data)
    if '?' in url:
        url = f"{url}&{query_str}"
    else:
        url = f"{url}?{query_str}"

    test_http = HttpRequest(url,session)
    recoverbook = LoginApi(test_http)
    responses= recoverbook.get_recoverybookmarks(method=method,data= body_data,headers=None,form_data=True)


    # # 断言
    info = handle_recover_bookmarkpull_response(responses,name)
    print(testCaseId)
    assert info,f'{name}用例未返回有效数据'