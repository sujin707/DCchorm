import requests


class LoginApi:
    def __init__(self, test_http ):
        self.test_http  = test_http

    def login(self,data,method,headers = None):
        # data ={"data":data}
        # headers = {"Content-Type": "application/json"}
        if headers is None:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/32-bit'
            }
        response = self.test_http.send_request(method, headers= headers ,data=data)
        # return response.json()
        return response

    def get_user_info(self,data,method,headers = None):
        # data ={"data":data}
        if headers is None:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/32-bit'
            }
        return self.test_http.send_request(method,headers= headers ,data=data)

    def get_equipment_id(self, method, params, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, params=params, form_data=form_data, headers=headers)

    def del_equipment_id(self, method, data, headers=None):
        if headers is None:
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/32-bit'
            }
        return self.test_http.send_request(method, headers=headers, data=data)



    def get_config_id(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }
        return self.test_http.send_request(method,data =data,form_data=form_data, headers=headers)

    def get_settingsversions(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }
        return self.test_http.send_request(method,data =data,form_data=form_data, headers=headers)

    def get_recoverybookmarks(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }
        return self.test_http.send_request(method,data =data,form_data=form_data, headers=headers)

    def push(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)


    def recover_book_history(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)

    def pull_book(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)

    def look_book(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)

    def remove_book(self, method, data, headers=None,form_data=False):
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)

    def update_config(self, method, data, headers=None,form_data=False):
        # print(f"进入 update_config 方法时的 data: {data}")
        if headers is None:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 SLBrowser/9.0.6.2081 SLBChan/10 SLBVPV/64-bit'
            }

        return   self.test_http.send_request(method, data=data, form_data=form_data, headers=headers)





    def __repr__(self):
        return f"LoginApi(some_attribute={self.test_http})"


