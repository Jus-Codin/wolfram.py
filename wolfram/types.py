"""
Typed dictionary of every single model in the API
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict, Union

class WolframDict(TypedDict):
  pass

class FullResultsDict(WolframDict):
  success: bool

  languagemsg: Optional[str]
  futuretopic: Optional[str] # I'm not too sure what format this is, so I'll assume it's a string
  error: Union[ErrorDict, Literal[False]]

  numpods: int
  timing: float

  recalculate: Optional[str]

  id: str
  host: str

  pods: List[PodDict]

  tips: Dict[str, str] # I would assume so...
  
class ConversationalResultsDict(WolframDict):
  """The response when using the Conversational API"""
  result: str
  conversationID: str
  host: str
  s: Optional[int]



class PodDict(WolframDict):
  title: str
  error: Union[ErrorDict, Literal[False]]
  position: int
  id: str
  numsubpods: int

class SubPodDict(WolframDict):
  title: Optional[str]
  plaintext: str
  img: ImageDict

class ErrorDict(WolframDict):
  # In the API specification it claims that this is an integer, however it is a string
  code: str 
  msg: str

class ImageDict(WolframDict):
  src: str
  alt: str
  title: str
  width: int
  height: int
  themes: str
  contenttype: str