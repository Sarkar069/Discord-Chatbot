import disnake
from disnake.ext import commands
from utils import dev_guild_only

bot = commands.InteractionBot()
url= "bot's avatar url"
class NoPrivateMessageError(commands.CommandError):
    """Custom error for when a command is used in DMs but is restricted to guilds."""
    pass

class PingCommand(commands.Cog):

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(description="Get the bot's current websocket latency.", guild_ids=dev_guild_only())
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        if inter.guild is None:
         raise NoPrivateMessageError("This command cannot be used in private messages.")
     

        await inter.response.defer(ephemeral=True)
        latency = round(self.bot.latency * 1000)
        embed = disnake.Embed(title=f"Pong..! 🏓 `{latency}` ms", color=disnake.Colour.purple())
        embed.set_author(name="bot's name", icon_url=url)
        await inter.edit_original_response(embed=embed)
  
    @ping.error
    async def ping_error(self, inter: disnake.AppCommandInteraction, error: commands.CommandError):
        if isinstance(error, NoPrivateMessageError):
            await inter.response.send_message(str(error), ephemeral=True)
        else:
            await inter.response.send_message("An unexpected error occurred.", ephemeral=True)

def setup(bot: commands.InteractionBot):
    bot.add_cog(PingCommand(bot))

