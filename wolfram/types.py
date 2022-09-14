"""
Typed dictionary of every single model in the API
"""

from __future__ import annotations

from typing import Literal, Mapping, Optional, Sequence, TypedDict, Union

class WolframDict(TypedDict):
  pass

class FullResultsDict(WolframDict):
  success: bool
  error: Union[ErrorDict, Literal[False]]

  numpods: int
  timing: float

  tips: TipsDict

  recalculate: Optional[str]

  id: str
  host: str

  pods: Sequence[PodDict, ...]

  assumptions: AssumptionsDict

  warnings: Union[
    Sequence[
      Union[SpellCheckWarningDict, DelimiterWarningDict, TranslationWarningDict], ...
    ],
    SpellCheckWarningDict, DelimiterWarningDict, TranslationWarningDict
  ]

  sources: Union[
    Sequence[
      SourceDict
    ],
    SourceDict
  ]

  # When queries don't return pods
  languagemsg: LanguageMsgDict
  futuretopic: FutureTopicDict
  examplepage: ExamplePageDict
  generalization: GeneralizationDict
  didyoumeans: Union[
    Sequence[DidYouMeanDict, ...],
    DidYouMeanDict
  ]

  
class ConversationalResultsDict(WolframDict):
  """The response when using the Conversational API"""
  result: str
  conversationID: str
  host: str
  s: Optional[int]



class PodDict(WolframDict):
  title: str
  primary: Optional[Literal[True]]
  error: Union[ErrorDict, Literal[False]]
  position: int
  id: str
  numsubpods: int
  subpods: Sequence[SubPodDict, ...]



class SubPodDict(WolframDict):
  title: Optional[str]
  img: Optional[ImageDict]
  plaintext: Optional[str]



# Subpod data types

class ImageDict(WolframDict):
  src: str
  alt: str
  title: str
  width: int
  height: int
  themes: str
  contenttype: str

class AudioDict(WolframDict):
  url: str
  type: str



# Assumptions

class AssumptionsDict(WolframDict):
  type: str
  word: str
  template: str
  count: int
  values: Sequence[AssumptionDict, ...]

class AssumptionDict(WolframDict):
  name: str
  desc: str
  input: str



# Warnings

class WarningDict(WolframDict):
  text: str

class SpellCheckWarningDict(WarningDict):
  word: str
  suggestion: str

class DelimiterWarningDict(WarningDict):
  pass

class TranslationWarningDict(WarningDict):
  phrase: str
  trans: str
  lang: str

class AlternativeDict(WolframDict):
  score: str
  level: str
  val: str

class ReinterpretWarningDict(WarningDict):
  new: str
  score: str
  level: str
  alternative: Optional[
    Union[
      Sequence[
        AlternativeDict, ...
      ],
      AlternativeDict
    ]
  ]



# Queries that are not understood

class DidYouMeanDict(WolframDict):
  score: str # Another example of a wrong data type used by the API...
  level: str
  val: str

class LanguageMsgDict(WolframDict):
  english: str
  other: str

class FutureTopicDict(WolframDict):
  topic: str
  msg: str

class ExamplePageDict(WolframDict):
  category: str
  url: str

class TipsDict(WolframDict):
  text: str

class GeneralizationDict(WolframDict):
  topic: str
  desc: str
  url: str



# Errors usually caused by appids

class ErrorDict(WolframDict):
  code: str # In the API specification it claims that this is an integer, however it is a string
  msg: str



# Sources

class SourceDict(WolframDict):
  url: str
  text: str