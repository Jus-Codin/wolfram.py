from wolfram.models import ConversationalResults, FullResults, Model

from typing import Generic, Optional, TypeVar

ResT = TypeVar("ResT")

class API(Generic[ResT]):
  VERSION: int
  ENDPOINT: str

  def format_results(self, raw: dict) -> ResT:
    raise NotImplementedError



class FullResultsAPI(API[FullResults]):
  VERSION = 2
  ENDPOINT = "query"

  def format_results(self, raw: dict) -> ResT:
    return FullResults.from_dict(raw)



class SimpleAPI(API):
  VERSION = 1
  ENDPOINT = "simple"

  def format_results(self, raw: dict):
    raise NotImplementedError



class ShortAPI(API):
  VERSION = 1
  ENDPOINT = "result"

  def format_results(self, raw: dict):
    raise NotImplementedError



class SpokenAPI(API):
  VERSION = 1
  ENDPOINT = "spoken"

  def format_results(self, raw: dict):
    raise NotImplementedError



class ConversationalAPI(API[ConversationalResults]):
  VERSION = 1
  ENDPOINT = "conversation.jsp"

  def format_results(self, raw: dict) -> ResT:
    raise NotImplementedError
