# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:15:51 2020

@author: jujuc
"""

import requests

URL_API_BASE = "https://api.deezer.com/album/302127"

req = requests.get(URL_API_BASE)
print(req.text)