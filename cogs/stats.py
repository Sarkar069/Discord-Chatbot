import disnake
from disnake.ext import commands
import datetime
import time
from utils import dev_guild_only

avatar_url = "your bot's avatar url"


startTime = time.time()


class Stats(commands.Cog):
    def __init__(self, bot : commands.InteractionBot):
        self.bot = bot
        
    
    def find_members(self) -> int:
     total_member_count = 0
     for guild in self.bot.guilds:
         total_member_count += guild.member_count
     return total_member_count


    @commands.slash_command(description="Info about bot stats", guild_ids=dev_guild_only())
    async def stats(self, inter: disnake.ApplicationCommandInteraction):
     

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
            title="your bot's name", url=avatar_url,
            description=stats_str,
            color=disnake.Colour.blue(), timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=inter.author)

        
        await inter.edit_original_response(embed=embed)
        
            
            
    @commands.slash_command(description="Get the bot's current websocket latency.", guild_ids=dev_guild_only())
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
     

        await inter.response.defer(ephemeral=True)
        latency = round(self.bot.latency * 1000)
        embed = disnake.Embed(title=f"Pong..! 🏓 `{latency}` ms", color=disnake.Colour.blue())
        embed.set_author(name="your bot's name", icon_url=avatar_url)
        await inter.edit_original_response(embed=embed)
  
    

def setup(bot : commands.InteractionBot):
    bot.add_cog(Stats(bot))