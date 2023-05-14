import discord
from discord.ext import commands

APP_COMMAND_LOG_FORMAT = """
[Interaction Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""


def app_command_log(interaction: discord.Interaction) -> str:
    return APP_COMMAND_LOG_FORMAT.format(
        command_name=interaction.command.name if interaction.command else "None",
        guild_id=interaction.guild.id if interaction.guild else "None",
        channel_id=interaction.channel.id if interaction.channel else "None",
        author_id=interaction.user.id,
        author_name=interaction.user.name,
    )


COMMAND_LOG = """
[Command]
Command Name: {command_name}
Guild ID: {guild_id}
Channel ID: {channel_id}
Author ID: {author_id}
Author Name: {author_name}
"""


def command_log(ctx: commands.Context) -> str:  # type: ignore
    return COMMAND_LOG.format(
        command_name=ctx.command.name if ctx.command else "None",
        guild_id=ctx.guild.id if ctx.guild else "None",
        channel_id=ctx.channel.id,
        author_id=ctx.author.id,
        author_name=ctx.author.name,
    )


LOGIN_LOG = """
Logged in as {user} (ID: {id})
Connected to {guilds} guilds
Bot is ready
"""


def login_log(user: discord.ClientUser | None, guild_amount: int):
    return LOGIN_LOG.format(
        user=user,
        id=user.id if user else "None",
        guilds=str(guild_amount),
    )
