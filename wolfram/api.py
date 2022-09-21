from wolfram.models import ConversationalResults, FullResults, Model

from typing import Any, Optional

class API:
  VERSION: int
  ENDPOINT: str

  def format_results(self, resp: Response):
    raise NotImplementedError

  async def async_format_results(self, resp: ClientResponse):
    raise NotImplementedError



class FullResultsAPI(API):
  VERSION = 2
  ENDPOINT = "query"

  def format_results(self, resp: Response) -> FullResults:
    raw = resp.json()
    return FullResults.from_dict(raw)

  async def async_format_results(self, resp: ClientResponse) -> FullResults:
    raw = await resp.json()
    return FullResults.from_dict(raw)



class SimpleAPI(API):
  VERSION = 1
  ENDPOINT = "simple"

  def format_results(self, resp: Response) -> bytes:
    return resp.content

  async def async_format_results(self, resp: ClientResponse) -> bytes:
    return await resp.read()



class ShortAPI(API):
  VERSION = 1
  ENDPOINT = "result"

  def format_results(self, resp: Response) -> str:
    return resp.text

  async def async_format_results(self, resp: ClientResponse) -> str:
    return await resp.text()



class SpokenAPI(API):
  VERSION = 1
  ENDPOINT = "spoken"

  def format_results(self, resp: Response) -> str:
    return resp.text

  async def async_format_results(self, resp: ClientResponse) -> str:
    return await resp.text()



class ConversationalAPI(API):
  VERSION = 1
  ENDPOINT = "conversation.jsp"

  def format_results(self, resp: Response) -> ConversationalResults:
    raw = resp.json()
    return ConversationalResults.from_dict(raw)

  async def async_format_results(self, resp: ClientResponse) -> ConversationalResults:
    raw = await resp.json()
    return ConversationalResults.from_dict(raw)