from collections.abc import Awaitable, Callable
from typing import TypeAlias

from discord import Interaction, Member, Role, User
from discord.app_commands import AppCommandChannel, AppCommandThread

InteractionCallback: TypeAlias = Callable[[Interaction], Awaitable[None]]

# SelectCallback
SelectCallback: TypeAlias = Callable[[Interaction, list[str]], Awaitable[None]]
ChannelSelectCallback: TypeAlias = Callable[[Interaction, list[AppCommandChannel | AppCommandThread]], Awaitable[None]]
RoleSelectCallback: TypeAlias = Callable[
    [Interaction, list[Role]],
    Awaitable[None],
]
MentionableSelectCallback: TypeAlias = Callable[[Interaction, list[Role | Member | User]], Awaitable[None]]
UserSelectCallback: TypeAlias = Callable[[Interaction, list[User | Member]], Awaitable[None]]
