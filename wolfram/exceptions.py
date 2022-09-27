class WolframException(Exception):
  """The base execution class"""

class ParameterConflict(WolframException):
  """Exception that is raised when a parameter that has been specified by the API was passed in"""
