from __future__ import annotations

from wolfram.models import ConversationalResults, FullResults, Model, SimpleImage

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
  from requests import Response
  from aiohttp import ClientResponse

class API:
  VERSION: int
  ENDPOINT: str

  def format_results(resp: Response):
    raise NotImplementedError

  async def async_format_results(resp: ClientResponse):
    raise NotImplementedError



class FullResultsAPI(API):
  VERSION = 2
  ENDPOINT = "query"

  def format_results(resp: Response) -> FullResults:
    raw = resp.json()
    return FullResults.from_dict(raw["queryresult"])

  async def async_format_results(resp: ClientResponse) -> FullResults:
    raw = await resp.json()
    return FullResults.from_dict(raw["queryresult"])



class SimpleAPI(API):
  VERSION = 1
  ENDPOINT = "simple"

  def format_results(resp: Response) -> SimpleImage:
    return SimpleImage(resp.content)

  async def async_format_results(resp: ClientResponse) -> SimpleImage:
    return SimpleImage(await resp.read())



class ShortAPI(API):
  VERSION = 1
  ENDPOINT = "result"

  def format_results(resp: Response) -> str:
    return resp.text

  async def async_format_results(resp: ClientResponse) -> str:
    return await resp.text()



class SpokenAPI(API):
  VERSION = 1
  ENDPOINT = "spoken"

  def format_results(resp: Response) -> str:
    return resp.text

  async def async_format_results(resp: ClientResponse) -> str:
    return await resp.text()



class ConversationalAPI(API):
  VERSION = 1
  ENDPOINT = "conversation.jsp"

  def format_results(resp: Response) -> ConversationalResults:
    raw = resp.json()
    return ConversationalResults.from_dict(raw)

  async def async_format_results(resp: ClientResponse) -> ConversationalResults:
    raw = await resp.json()
    return ConversationalResults.from_dict(raw)