from __future__ import annotations

from collections import defaultdict
from itertools import chain
from urllib.parse import urlencode
from json import loads

from aiohttp import ClientSession
import xmltodict

from typing import Any, Tuple, Dict, Union
from types import NoneType

# TODO: CHANGE EVERYTHING, I FOUND THE DUMB SETTING TO MAKE RESPONSES FROM THE API JSON FORMATTED
# Also found one to do images! (https://products.wolframalpha.com/api/documentation/#formatting-output)

_attr_types = defaultdict(
  lambda: (lambda x: x),
  height=int,
  width=int,
  numsubpods=int,
  position=float,
  primary=xmlbool,
  success=xmlbool
)

def xmlbool(s):
  return bool(loads(s))

def postprocessor(_, key: str, value: Union[str, Dict[str, Any]]):
  value = Model.find_cls(key)(value)
  value = _attr_types[key.lstrip("@")](value)
  return key, value



class Client:
  URL = "https://api.wolframalpha.com/v2/query?"

  def __init__(self, app_id: str):
    self.app_id = app_id

  async def query(self, input: str, param=(), **kwargs) -> Result:
    data = dict(
      input=input,
      appid=self.app_id
    )
    data = chain(params, data.items(), kwargs.items())

    query = urlencode(tuple(data))
    url = self.URL + query
    async with ClientSession() as session:
      async with session.get(url) as resp:
        assert resp.headers["Content-Type"] == "text/xml;charset=utf-8"
        doc = xmltodict.parse(await resp.text(), postprocessor=postprocessor)
        return doc["queryresult"]



class Model:
  children: Tuple[str, ...] = ()
  key: str = ""

  def __init__(self, value: Dict[str, Any]):
    self._dict = value

  @classmethod
  def find_cls(cls, key: str) -> Model:
    """Find a possible Model to wrap an item by key"""
    match = (
      sub
      for sub in cls.__subclasses__()
      if key == getattr(sub, "key", sub.__name__.lower())
    )
    return next(match, lambda x: x)

  def __getitem__(self, item: str):
    return self._dict[item] if item in self._dict else self._dict["@"+item]

  def __getattr__(self, attr: str):
    return self._getchildren(attr) or self._getattr(attr)

  def _getattr(self, attr: str):
    try:
      return self[attr]
    except KeyError:
      return AttributeError(attr)

  def _getchildren(self, name: str):
    if name not in self.__class__.children:
      return
    sub = self.__class__.find_cls(name)
    attr = sub.key or sub.__name__.lower()
    try:
      val: Model = self._getattr(attr)
    except AttributeError:
      val = ()
    return val
    
class Assupmtions(Model):
  """Not to be confused with Assumption,
  this class is basically a list of assumptions.

  This is used to solve the issue since assumptions are stored in a dictionary of its own.
  This basically means I'm too lazy to implement a proper solution
  """

  children = "assumption"

  def __iter__(self):
    return (a for a in self["assumption"]).__iter__()

class Assumption(Model):
  @property
  def text(self):
    text = self.template.replace('${desc1}', self.description)
    with contextlib.suppress(Exception):
      text = text.replace('${word}', self.word)
    return text[: text.index('. ') + 1]

class Warning(Model):
  # I've rarely ever seen this but whatever

class Image(Model):
  """Holds info about an image included with an answer"""
  key = "img"

class Subpod(Model):
  """Holds a specific answer or additional information relevant to said answer"""

class Pod(Model):
  """
  Groups answers and information contextualizing those answers.
  """

  children = ('subpods',)

  @property
  def primary(self):
    return self.get('@primary', False)

  @property
  def texts(self):
    """
    The text from each subpod in this pod as a list.
    """
    return [subpod.plaintext for subpod in self.subpods]

  @property
  def text(self):
    return next(iter(self.subpods)).plaintext

class Result(Model):
  """Handles processing the response for the programmer"""

  key = 'queryresult'
  children = 'pods', 'assumptions', 'warnings'

  @property
  def info(self):
    """
    The pods, assumptions, and warnings of this result.
    """
    return itertools.chain(self.pods, self.assumptions, self.warnings)

  def __iter__(self):
    return self.info

  def __len__(self):
    return sum(1 for _ in self)

  def __bool__(self):
    return bool(len(self))

  @property
  def results(self):
    """
    The pods that hold the response to a simple, discrete query.
    """
    return (pod for pod in self.pods if pod.primary or pod.title == 'Result')

  @property
  def details(self):
    """
    A simplified set of answer text by title.
    """
    return {pod.title: pod.text for pod in self.pods}