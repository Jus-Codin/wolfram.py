from typing import Optional

class API:
  VERSION: int
  ENDPOINT: str

  def format_results(self, raw: dict):
    raise NotImplementedError

class FullResultsAPI(API):
  VERSION = 2
  ENDPOINT = "query"



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



class ConversationalAPI(API):
  VERSION = 1
  ENDPOINT = "conversation.jsp"

  def format_results(self, raw: dict):
    raise NotImplementedError
