"""
Practically all WolframAlpha API models as well as internally used
data classes are here
"""

# TODO: Implement API models

from dataclasses import dataclass, field
from typing import (
  TYPE_CHECKING,
  Any,
  Callable,
  Mapping,
  Optional,
  Sequence,
  Union
)

@dataclass
class WolframRequest:
  """Contains data about the request that is to be sent to the API.
  This is not meant to be used directly"""
  base_url: str = "https://api.wolframalpha.com/"
  version: int
  endpoint: str
  params: Mapping[str, str]



@dataclass
class Model:
  """The base class of all Wolfram|Alpha models"""
  _raw: dict = None

  @classmethod
  def from_dict(cls, raw: Mapping[str, Any]):
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
  def _to_dict(self):
    """Returns the model with it's values in a dictionary excluding private variables,
    not to be called directly"""
    return self._raw_type(**{
      k: getattr(self, k)
      for k in self.__dataclass_fields__.keys()
      if not k.startswith("_")
    })

  @property
  def raw(self) -> Mapping[str, Any]:
    """Returns the raw dictionary of the model"""
    return self._raw if self._raw is not None else self._to_dict



@dataclass
class FullResults(Model):
  ...



@dataclass
class ConversationalResults(Model):
  result: str
  conversationID: str
  host: str
  s: Optional[int] = int



@dataclass
class Pod(Model):
  ...



@dataclass
class SubPod(Model):
  ...



# Subpod models

@dataclass
class Image(Model):
  ...

@dataclass
class Audio(Model):
  ...



# Assumptions

@dataclass
class AssumptionsCollection(Model):
  ...

@dataclass
class Assumption(Model):
  ...



# Warnings

@dataclass
class Warning(Model):
  text: str

@dataclass
class SpellCheckWarning(Warning):
  ...

@dataclass
class DelimiterWarning(Warning):
  ...

@dataclass
class TranslationWarning(Warning):
  ...

@dataclass
class Alternative(Model):
  score: str
  level: str
  val: str

@dataclass
class ReinterpretWarning(Model):
  new: str
  level: str
  score = field(default_factory=float)
  alternative: Optional[
    Union[
      Sequence[
        Alternative, ...
      ],
      Alternative
    ]
  ]



# Queries that are not understood

@dataclass
class DidYouMean(Model):
  ...

@dataclass
class LanguageMsg(Model):
  ...

@dataclass
class FutureTopic(Model):
  ...

@dataclass
class ExamplePage(Model):
  ...

@dataclass
class Tip(Model):
  ...

@dataclass
class Generalization(Model):
  ...



# Errors usually caused by bad app ids

@dataclass
class Error(Model):
  msg: str
  code = field(default_factory=int)



# Sources

class Source(Model):
  ...