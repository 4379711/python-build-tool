import requests
from functools import partial
from threading import Thread, Lock
import sys
import tkinter
from datetime import datetime
from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk, filedialog
import winreg
import os
import fitz
import xlwt
import xlrd
from xlutils.copy import copy
from api import Api
from split_pdf import *
from do_work import Work
from reg_password import *
from config import *
import rsa
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from pandas import *
import pandas._libs.tslibs.base
import re
from excel_utils import *
from frame import *
if __name__ == '__main__':
    Application()
