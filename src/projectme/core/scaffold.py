from typing import Literal
from warnings import warn

from projectme.utils import fs
from projectme.stacks import python, react

VALID_STACKS = ("react", "python")
STACK_BUILDERS = {
    "react": react.build,
    "python": python.build,
}

def scaffold(stack: Literal["react", "python"], name: str,
             arguments: list[str] = None,
             flags: list[str] = None,
             path: str = None):

    # Required arguments
    if stack is None and name is None:
        raise TypeError("scaffold.py: scaffold() missing 2 required arguments: 'stack' and 'name'")
    if stack is None:
        raise TypeError("scaffold.py: scaffold() missing required argument: 'stack'")
    if name is None:
        raise TypeError("scaffold.py: scaffold() missing required argument: 'name'")
    if stack not in VALID_STACKS:
        raise ValueError(f"scaffold.py: scaffold() invalid value for 'stack': '{stack}'. Expected one of {VALID_STACKS}")

    # Optional arguments
    if arguments is None and flags is None:
        warn("scaffold.py: scaffold() missing 2 optional arguments: 'arguments' and 'flags'")
    elif arguments is None:
        warn("scaffold.py: scaffold() missing optional argument: 'arguments'")
    elif flags is None:
        warn("scaffold.py: scaffold() missing optional argument: 'flags'")

    arguments = arguments or []
    flags = flags or []
    path = path or fs.cwd()

    # Build
    return STACK_BUILDERS[stack](name, path, arguments, flags)
