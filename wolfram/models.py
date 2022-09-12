"""
Practically all WolframAlpha API models as well as internally used
data classes are here
"""

# TODO: Implement API models

from dataclasses import dataclass

@dataclass
class WolframRequest:
  """Contains data about the request that is to be sent to the API.
  This is not meant to be used directly"""
  base_url: str = "https://api.wolframalpha.com/"
  version: int
  endpoint: str
  params: Dict[str, str]