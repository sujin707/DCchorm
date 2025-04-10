
import requests


class HttpRequest:

    def __init__(self,base_url,session=None):
        self.base_url = base_url
        if session:
            self.session = session
        else:
            self.session = requests.Session()

    def __repr__(self):
        return f"LoginApi(some_attribute={self.base_url})"

    def send_request(self,method,headers=None,data=None,params=None,timeout=1000,form_data=False):
        url = self.base_url
        if method.lower() == 'post':
            if form_data:
                # print(f"进入 update_config 方法时的 data: {data}")
                response = self.session.post(url, headers=headers, data=data)
            else:
                response = self.session.post(url, headers=headers, json=data)
        elif method.lower() == 'get':
            response = self.session.get(url, headers=headers,params=params)
            # 可以根据需要添加更多的请求方法
        # print(f"服务器响应内容: {response.text}")  # 打印响应内容
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("响应内容不是有效的 JSON 格式。")
            return response.text


