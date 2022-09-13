from json import JSONDecodeError
from urllib.parse import urlencode
from typing import Dict, Tuple, overload

from .api import API
from .models import WolframRequest

import requests

class ClientABC:
  """The abstract base class of Clients"""

  API_VERSION = {
    1: "v1/",
    2: "v2/"
  }

  def __init__(self, appid: str, api: API, base_url: str = None):
    self._api = api
    self._appid = appid

  @property
  def api(self) -> API:
    """The API that this client is using"""
    return self._api

  @property
  def appid(self) -> str:
    """The App ID in use by the client"""
    return self._appid

  def _check_request(self, request: WolframRequest):
    if request.version not in self.API_VERSION.keys():
      raise ValueError(f"Unknown API version '{request.version}'.")

  def _send_request(self, request: WolframRequest):
    raise NotImplementedError

  def _create_request(self, **params) -> WolframRequest:
    return WolframRequest(version=self.api.VERSION, endpoint=self.api.ENDPOINT, params=params)

  def query(self): # TODO
    raise NotImplementedError



class Client(ClientABC):
  """Client to interact with the APIs"""

  def _send_request(self, request: WolframRequest) -> dict:
    self._check_request(request)
    api_version = self.API_VERSION[request.version]

    params = "?" + urlencode(
      tuple(
        dict(appid=self.appid, **request.params).items()
      )
    )
    url = request.base_url + api_version + endpoint + params
    resp = requests.get(url)
    try: 
      data = resp.json()
    except JSONDecodeError:
      raise Exception() # TODO: Change to custom exception
    return data



class AsyncClient(ClientABC):
  ...