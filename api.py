import os

import requests

import config
from reg_password import rsa_decrypt

requests.packages.urllib3.disable_warnings()


class Api:

    def __init__(self):
        if os.path.exists("userconfig.txt"):
            with open("userconfig.txt", 'r', encoding='gbk') as fp:
                r_list = fp.readlines()
                config.app_key = rsa_decrypt(r_list[0].strip())
                config.app_secret = rsa_decrypt(r_list[1].strip())

    @staticmethod
    def get_file_content(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()

    def _request(self, url, file_path):
        headers = {
            "app-key": config.app_key,
            "app-secret": config.app_secret,
        }
        data = self.get_file_content(file_path)
        resp = requests.post(url, headers=headers, data=data, verify=False)
        return resp.json()

    def table(self, file_path):
        url = "https://ocr-api.ccint.com/cci_ai/service/v1/table_recog"
        return self._request(url, file_path)

    def common_text(self, file_path):
        url = "https://ocr-api.ccint.com/cci_ai/service/v1/common_text"
        return self._request(url, file_path)


if __name__ == '__main__':
    api = Api()
    resp = api.table("C:\\Users\\admin\\Desktop\\a.jpg")
    print(resp)
