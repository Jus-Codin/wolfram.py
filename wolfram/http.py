from abc import ABC, abstractmethod
from dataclasses import dataclass
from json import JSONDecodeError
from urllib.parse import urlencode
from typing import Dict, Tuple

from .models import WolframRequest

import requests

class HTTPClientABC(ABC):
  """The abstract base class of HTTPClients"""

  API_VERSION = {
    1: "v1/",
    2: "v2/"
  }
  ENDPOINTS: Dict[int, Tuple[str]] = {
    1: ("simple", "conversation.jsp", "spoken", "result"),
    2: ("query",)
  }

  def __init__(self, appid: str, base_url: str = None):
    self.appid = appid

  def check_request(self, request: WolframRequest):
    if request.version not in self.API_VERSION.keys():
      raise ValueError(f"Unknown API version '{request.version}'.")

    if request.endpoint not in self.ENDPOINTS[request.version]:
      raise ValueError(f"Unknown endpoint '{request.endpoint}'.")

  @abstractmethod
  def send_request(self, request: WolframRequest):
    raise NotImplementedError()

class HTTPClient(HTTPClientABC):
  """Client to interact with the API endpoint and returns raw data"""

  def send_request(self, request: WolframRequest) -> dict:
    self.check_request(request)
    api_version = self.API_VERSION[request.version]

    params = "?" + urlencode(
      tuple(
        dict(appid=self.appid, **request.params).items()
      )
    )
    url = request.base_url + api_version + endpoint + params)
    resp = requests.get(url)
    try: 
      data = resp.json()
    except JSONDecodeError:
      raise Exception() # TODO: Change to custom exception

# TODO
class AioHTTPClient(HTTPClientABC):
  """Asynchronous client to interact with the API endpoint and returns raw data"""