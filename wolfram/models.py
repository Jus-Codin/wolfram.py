"""
Practically all WolframAlpha API models as well as internally used
data classes are here
"""

# TODO: Implement API models

from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Mapping, Optional, TypeVar, Generic, TypedDict

from wolfram.types import WolframDict

@dataclass
class WolframRequest:
  """Contains data about the request that is to be sent to the API.
  This is not meant to be used directly"""
  base_url: str = "https://api.wolframalpha.com/"
  version: int
  endpoint: str
  params: Mapping[str, str]



ModT = TypeVar("ModT", bound=WolframDict) # This will have to do for now

@dataclass
class Model(Generic[ModT]):
  """The base class of all Wolfram|Alpha models"""
  _raw: Optional[ModT] = None
  _raw_type: ClassVar[Callable]

  @classmethod
  def from_dict(cls, raw: ModT):
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
    return {
      k: getattr(self, k)
      for k in self.__dataclass_fields__.keys()
      if not k.startswith("_")
    }

  @property
  def raw(self) -> ModT:
    """Returns the raw dictionary of the model"""
    return self._raw if self._raw is not None else self._to_dict

class Error(Model):
  _raw_type = ErrorDict
  msg: str
  code = field(default_factory=int)

