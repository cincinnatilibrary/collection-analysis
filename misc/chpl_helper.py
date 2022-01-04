# import the needed modules
from base64 import b64encode
from io import BytesIO
import json
import numpy as np
import pandas as pd
import re
import requests
from sqlalchemy import create_engine

# this will get an initial access token
def set_access_headers(client_key, client_secret, base_url):
  """
  use this function to set and refresh the access_headers for future
  authorizing API requests
  """

  auth_string = b64encode(
    (client_key + ':' + client_secret).encode('utf-8')
  ).decode('utf-8')

  headers = {}
  headers['authorization'] = 'basic ' + auth_string

  try:
      r = requests.post(base_url + 'token', headers=headers, verify=True)

  except requests.ConnectionError as e:
      # print('connection error: {}'.format(e))
      return(
        -1
      )
      return 0

  if r.status_code != 200:
      print(r.status_code)
      return 0

  access_token = r.json()['access_token']

  # set our headers to use the access token
  headers['authorization'] = 'bearer ' + access_token

  # Note: depending on the Sierra REST API request endpoint,
  # you may need to change the types below to fit the request,
  # but these are pretty standard
  headers['content-type'] = 'application/json'
  headers['accept'] = 'application/json'

  return headers


def check_credentials(client_key, client_secret, base_url):
  """
  try to authorize the client_key + client_secret and return some data
  """

  try:
    headers = set_access_headers(client_key, client_secret, base_url)
    r = requests.get(base_url + 'info/token', headers=headers, verify=True)
  except:
    return(
      # TODO 
      # {'error': r.NameError}
      -1
    )

  return(r.json())

#print('access token expires in: {} seconds'.format(r.json()['expiresIn']))