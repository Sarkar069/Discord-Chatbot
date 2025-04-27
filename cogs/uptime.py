import disnake
import datetime
import time
from disnake.ext import commands
from utils import dev_guild_only

url = "your bot's avatar url"

bot = commands.InteractionBot()

startTime = time.time()

class NoPrivateMessageError(commands.CommandError):
    """Custom error for when a command is used in DMs but is restricted to guilds."""
    pass


class UptimeCommand(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        
    def find_members(self) -> int:
     total_member_count = 0
     for guild in self.bot.guilds:
         total_member_count += guild.member_count
     return total_member_count


    @commands.slash_command(description="Info about bot stats", guild_ids=dev_guild_only())
    async def stats(self, inter: disnake.ApplicationCommandInteraction):
        if inter.guild is None:
         raise NoPrivateMessageError("This command cannot be used in private messages.")
     

        await inter.response.defer(ephemeral=True)

        uptime_seconds = int(round(time.time() - startTime))
        uptime_timedelta = datetime.timedelta(seconds=uptime_seconds)
        days, seconds = uptime_timedelta.days, uptime_timedelta.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        uptime_string = f"{days}d {hours}h {minutes}m {seconds}s"
        
        stats_str = (
         f'➠ **Server Count** : {len(inter.bot.guilds)}\n'
         f'➠ **Users** : {self.find_members()}\n'
         f'➠ **Language** : [Python](https://www.python.org/)\n'
         f'➠ **Library** : [Disnake](https://guide.disnake.dev/)\n'
         f'➠ **Uptime** ```{uptime_string}```'
        )
        

        embed = disnake.Embed(
            title="bot's name", url=url,
            description=stats_str,
            color=disnake.Colour.blue(), timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=url)
        embed.set_footer(text='Sarkar#8662')

        
        await inter.edit_original_response(embed=embed)
        
    @stats.error
    async def uptime_error(self, inter: disnake.AppCommandInteraction, error: commands.CommandError):
        if isinstance(error, NoPrivateMessageError):
            await inter.response.send_message(str(error), ephemeral=True)
        else:
            await inter.response.send_message("An unexpected error occurred.", ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(UptimeCommand(bot))
