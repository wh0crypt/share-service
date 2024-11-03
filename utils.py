import sys
from typing import Tuple

def check_env(env_vars : Tuple[str]) -> None:
  """
  Checks if the specified environment variables are set.

  This function takes a tuple of environment variable names and checks
  if each one is set (not None). If any variable is not set, it prints
  an error message and terminates the program with an exit code of 1.

  Args:
    env_vars (Tuple[str]): A tuple of environment variable names to check.

  Returns:
    None
  """
  error = False
  
  for env_var in env_vars:
    if env_var is None:
      print(f"{env_var} not set in .env file")
      error = True
  
  if error:
    sys.exit(1)