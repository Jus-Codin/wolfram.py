from __future__ import annotations

from json import JSONDecodeError
from urllib.parse import urlencode
from typing import TYPE_CHECKING, Dict, Optional, Sequence, Tuple

from wolfram.api import API, FullResultsAPI, SimpleAPI, ShortAPI, SpokenAPI, ConversationalAPI
from wolfram.models import FullResults

if TYPE_CHECKING:
  from aiohttp import ClientResponse
  from requests import Response

import aiohttp
import requests

class ClientBase:
  """The base class of Clients"""
  BASE_URL = "https://api.wolframalpha.com/"

  API_VERSION = {
    1: "v1/",
    2: "v2/"
  }

  def __init__(self, appid: str):
    self._appid = appid

  @property
  def appid(self) -> str:
    """The App ID in use by the client"""
    return self._appid



class Client(ClientBase):
  """Client to interact with the APIs"""

  def query(self, api: API, **params):
    if not issubclass(api, API):
      raise TypeError("api must be `API` type")


    if api.VERSION not in self.API_VERSION.keys():
      raise ValueError(f"Unknown API version '{request.version}'.")

    api_version = self.API_VERSION[api.VERSION]

    params = "?" + urlencode(
      tuple(
        dict(appid=self.appid, **params).items()
      )
    )
    url = self.BASE_URL + api_version + api.ENDPOINT + params
    resp = requests.get(url)
    return api.format_results(resp)

  def query_full_results(self, input: str, format: Optional[Sequence[str, ...]] = None, **params) -> FullResults:
    if format is not None:
      return self.query(api=FullResultsAPI, input=input, format=",".join(format), **params)
    else:
      return self.query(api=FullResultsAPI, input=input, **params)



class AsyncClient(ClientBase):
  """Async client to interact with the APIs, powered by aiohttp"""

  async def query(self, api: API, **params):
    if not isinstance(api, API):
      raise TypeError("api must be `API` type")


    if api.VERSION not in self.API_VERSION.keys():
      raise ValueError(f"Unknown API version '{request.version}'.")

    api_version = self.API_VERSION[api.VERSION]

    params = "?" + urlencode(
      tuple(
        dict(appid=self.appid, **params).items()
      )
    )
    url = self.BASE_URL + api_version + api.ENDPOINT + params
    async with aiohttp.ClientSession() as client:
      async with client.get(url) as resp:
        result = await api.async_format_results(resp)
    return result

    async def query_full_results(self, input: str, format: Optional[Sequence[str, ...]] = None, **params) -> FullResults:
      if format is not None:
        return await self.query(api=FullResultsAPI, input=input, format=",".join(format), **params)
      else:
        return await self.query(api=FullResultsAPI, input=input, **params)