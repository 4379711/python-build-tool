import base64
import winreg

import rsa
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

from config import *


def get_value(key_name):
    """
    检查注册表项是否存在,如果存在返回注册表值
    :return:
    """
    try:
        aa = winreg.QueryValueEx(winreg.HKEY_CLASSES_ROOT, key_name)
        return aa[0]
    except Exception:
        return None


def set_value(key_name, _value):
    """
    设置/更新注册表项和值
    """
    winreg.SetValueEx(winreg.HKEY_CLASSES_ROOT, key_name, 0, winreg.REG_SZ, _value)


def make_pem():
    _public_key, _private_key = rsa.newkeys(2048)
    public_key_bytes = _public_key.save_pkcs1()
    private_key_bytes = _private_key.save_pkcs1()
    print(public_key_bytes)
    print(private_key_bytes)


def rsa_encrypt(message):
    """使用公钥进行加密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(public_key))
    cipher_text = base64.b64encode(cipher.encrypt(message.encode())).decode()
    return cipher_text


def rsa_decrypt(text):
    """使用私钥进行解密"""
    cipher = Cipher_pkcs1_v1_5.new(RSA.importKey(private_key))
    retval = cipher.decrypt(base64.b64decode(text), 'ERROR').decode('utf-8')
    return retval
