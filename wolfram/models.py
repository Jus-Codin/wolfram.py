"""
Practically all WolframAlpha API models as well as internally used
data classes are here
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import (
  Any,
  Callable,
  ClassVar,
  Generic,
  Iterable,
  List,
  Literal,
  Mapping,
  Optional,
  Sequence,
  TypeVar,
  Union
)

from wolfram.types import *
from wolfram.utils import optional_factory, list_map_factory, always_list_factory

DictT = TypeVar("DictT", bound=WolframDict)



@dataclass
class WolframRequest:
  """Contains data about the request that is to be sent to the API.
  This is not meant to be used directly"""
  base_url: str = "https://api.wolframalpha.com/"
  version: int
  endpoint: str
  params: Mapping[str, str]



class WolframURL:
  def __init__(self, url: str):
    url, self._query = url.split("?")
    self._path = url.replace("\/", "/")

  @property
  def path(self) -> str:
    return self._path

  @property
  def query(self) -> str:
    return self._query

  @property
  def params(self) -> Mapping[str, str]:
    return {
      v[0]: v[1]
      for v in map(
        str.split, self.query.split("&")
      )
    }

  @property
  def url(self) -> str:
    return self.path + self.query



@dataclass
class Model(Generic[DictT]):
  """The base class of all Wolfram|Alpha models"""
  _raw: DictT = None

  @classmethod
  def from_dict(cls, raw: DictT):
    """Constructs the model from a mapping"""
    return cls(
      _raw = raw,
      **{
        k: v
        for k, v in raw.items()
        if k in self.__dataclass_fields__.keys()
      }
    )

  @property
  def _to_dict(self) -> DictT:
    """Returns the model with it's values in a dictionary excluding private variables,
    not to be called directly"""
    return {
      k: getattr(self, k)
      for k in self.__dataclass_fields__.keys()
      if not k.startswith("_")
    }

  @property
  def raw(self) -> DictT:
    """Returns the raw dictionary of the model"""
    return self._raw if self._raw is not None else self._to_dict



# Subpod models

@dataclass
class Image(Model[ImageDict]):
  title: str
  width: int
  height: int
  themes = field(
    default_factory=lambda seq: [
      int(ele) for ele in seq.split(",")
    ]
  )

@dataclass
class Audio(Model[AudioDict]):
  type: str
  url = field(default_factory=WolframURL)



# Assumptions

@dataclass
class Assumption(Model[AssumptionDict]):
  name: str
  desc: str
  input: str
  
@dataclass
class AssumptionsCollection(Model[AssumptionsDict]):
  type: str
  word: str
  template: str
  count: int
  values = field(
    default_factory=list_map_factory(
      Assumption.from_dict
    )
  )



# Warnings

@dataclass
class Warning(Model[WarningDict], Generic[DictT]):
  text: str

  @classmethod
  def _find_cls(cls, warning: DictT):
    for sub in cls.__subclasses__():
      if all(
        k in warning.keys() or k == "text"
        for k in sub.__dataclass_fields__.keys()
      ):
        return sub
    return cls

  @classmethod
  def to_subclass(cls, warning: DictT):
    cls = cls._find_cls(warning)
    return cls.from_dict(warning)

@dataclass
class SpellCheckWarning(Warning[SpellCheckWarningDict]):
  word: str
  suggestion: str

@dataclass
class DelimiterWarning(Warning[DelimiterWarningDict]):
  pass

@dataclass
class TranslationWarning(Warning[TranslationWarningDict]):
  phrase: str
  trans: str
  lang: str

@dataclass
class Alternative(Model[AlternativeDict]):
  level: str
  val: str
  score = field(default_factory=float)

@dataclass
class ReinterpretWarning(Model[ReinterpretWarningDict]):
  new: str
  level: str
  score = field(default_factory=float)
  alternative = field(
    default_factory=_always_list_factory(
      Alternative.from_dict
    )
  )



# Queries that are not understood

@dataclass
class DidYouMean(Model[DidYouMeanDict]):
  level: str
  val: str
  score = field(default_factory=float)

@dataclass
class LanguageMsg(Model[LanguageMsgDict]):
  english: str
  other: str

@dataclass
class FutureTopic(Model[FutureTopicDict]):
  topic: str
  msg: str

@dataclass
class ExamplePage(Model[ExamplePageDict]):
  category: str
  url = field(default_factory=WolframURL)

@dataclass
class Tip(Model[TipsDict]):
  text: str

@dataclass
class Generalization(Model[GeneralizationDict]):
  topic: str
  desc: str
  url = field(default_factory=WolframURL)



# Errors usually caused by bad app ids

@dataclass
class Error(Model[ErrorDict]):
  msg: str
  code = field(default_factory=int)



# Sources

@dataclass
class Source(Model[SourceDict]):
  text: str
  url = field(default_factory=WolframURL)



@dataclass
class SubPod(Model[SubPodDict]):
  title: str
  plaintext: Optional[str]
  img: Optional[Image] = field(
    default_factory=optional_factory(
      Image.from_dict
    )
  )



@dataclass
class Pod(Model[PodDict]):
  title: str
  position: int
  id: str
  numsubpods: int
  primary: Optional[Literal[True]] = None
  error: Optional[Error] = field(
    default_factory=optional_factory(
      Error.from_dict,
      match=False
    )
  )
  subpods = field(
    default_factory=list_map_factory(
      SubPod.from_dict
    )
  )



@dataclass
class FullResults(Model[FullResultsDict]):
  success: bool
  numpods: int
  timing: float

  id: str
  host: str

  tips = field(
    default_factory=always_list_factory(
      Tip.from_dict
    )
  )

  recalculate: Optional[WolframURL] = field(
    default_factory=optional_factory(
      WolframURL,
      match=""
    )
  )
  pods = field(
    default_factory=list_map_factory(
      Pod.from_dict
    )
  )
  assumptions: Optional[AssumptionsCollection] = None
  warnings: Optional[Warning] = field(
    default_factory=Warning.to_subclass
  )
  sources = field(
    default_factory=always_list_factory(
      Source.from_dict
    )
  )

  languagemsg: Optional[LanguageMsg] = field(
    default_factory=LanguageMsg.from_dict
  )
  futuretopic: Optional[FutureTopic] = field(
    default_factory=FutureTopic.from_dict
  )
  examplepage: Optional[ExamplePage] = field(
    default_factory=ExamplePage.from_dict
  )
  generalization: Optional[Generalization] = field(
    default_factory=Generalization.from_dict
  )
  didyoumeans = field(
    default_factory=always_list_factory(
      DidYouMean.from_dict
    )
  )



@dataclass
class ConversationalResults(Model[ConversationalResultsDict]):
  result: str
  conversationID: str
  host: str
  s: Optional[int] = int