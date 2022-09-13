
class API:
  VERSION: int
  ENDPOINT: str

  def format_results(self, raw: dict):
    raise NotImplementedError()

class FullResultsAPI(API):
  VERSION = 2
  ENDPOINT = "query"

class SimpleAPI(API):
  VERSION = 1
  ENDPOINT = "simple"

class ShortAPI(API):
  VERSION = 1
  ENDPOINT = "result"

class SpokenAPI(API):
  VERSION = 1
  ENDPOINT = "spoken"

class ConversationalAPI(API):
  VERSION = 1
  ENDPOINT = "conversation.jsp"
