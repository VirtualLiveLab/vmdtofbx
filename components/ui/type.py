from collections.abc import Awaitable, Callable
from typing import TypeAlias

from discord import Interaction

InteractionCallback: TypeAlias = Callable[[Interaction], None | Awaitable[None]]
