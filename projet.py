# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:15:51 2020

@author: jujuc
"""

import requests

URL_API_BASE = "https://api.deezer.com/version/service/id/method/?parameters"

def get_author_info_from_wikipedia(author_name):
    '''
        Get author detailed info from wikipedia API

        :param author_name:
        :type: author_name: string
        :return: json_response: response of wikipedia API
        :rtype: dict
    '''
    S = requests.Session()
    
    params = {
        'titles': author_name,
        'prop': 'extracts',
        'explaintext': True,
        "action": "paraminfo",
        "format": "json",
        "modules": "parse|query+info|query"

    }

    # TODO : Request Wikipedia API using params and return json_response

    R = S.get(url=URL_API_BASE, params=params)
    json_response = R.json()
    return json_response
