# import the needed modules
from base64 import b64encode
import json
import requests

# this will get an initial access token
def get_access_headers(client_key, client_secret, base_url):
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
      # TODO: return something more meaningful ...
      # print('connection error: {}'.format(e))
      return(
        -1
      )
      return 0

  if r.status_code != 200:
      print(r.status_code)
      return(
        -1
      )

  access_token = r.json()['access_token']

  # set our headers to use the access token
  headers['authorization'] = 'bearer ' + access_token

  # Note: depending on the Sierra REST API request endpoint,
  # you may need to change the types below to fit the request,
  # but these are pretty standard
  headers['content-type'] = 'application/json'
  headers['accept'] = 'application/json'

  return headers


def get_api_access_header_info(access_headers, base_url):
  """
  try to authorize the client_key + client_secret and return some data
  """

  try:
    r = requests.get(base_url + 'info/token', headers=access_headers, verify=True)
  except:
    return(
      # TODO 
      # {'error': r.NameError}
      -1
    )

  return(r.json())


def make_auth_string(client_key, client_secret):
  """
  given client_key, client_secret inputs, produce the auth_string for the sierra rest api
  (or, better yet, store this auth string, and use it as the requested input from the user)
  """
  auth_string = b64encode(
      (client_key + ':' + client_secret).encode('utf-8')
  ).decode('utf-8')

  return(auth_string)


def make_auth_headers(auth_string):
  headers = {}
  headers['authorization'] = 'basic ' + auth_string

  return(headers)


def set_access_headers(base_url, auth_string=None, client_key=None, client_secret=None):
  """
  use this function to set and refresh the access_headers for future
  authorizing API requests

  either use the client_key and client_secret 
  ... or the auth_string (which has been pre-encoded from the key + secret)
  """
  if (auth_string is None and client_key is None and client_key is None):
    # can't work with no input
    return(-1)

  if ( (auth_string is None) and (client_key is not None and client_key is not None) ):
    auth_string = make_auth_string(client_key, client_secret)
  
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