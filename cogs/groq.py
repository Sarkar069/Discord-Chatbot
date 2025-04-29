import disnake
from disnake.ext import commands
from groq import AsyncGroq
import os
from collections import defaultdict
import re
from typing import List, Dict
import logging
import traceback
from dotenv import load_dotenv
load_dotenv()
from utils import dev_guild_only

logger = logging.getLogger("your bot's name")

class Groq(commands.Cog):
    def __init__(self, bot: commands.InteractionBot) -> None:
        self.bot = bot
        self.groq_client = AsyncGroq(api_key=os.getenv("Groq_key"))
        self.conversation_history: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        self.active_channels = set()
        self.user_models: Dict[int, str] = defaultdict(lambda: "llama-3.3-70b-versatile")
        self.available_models = [
            "llama-3.3-70b-versatile",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "llama-3.1-8b-instant",
            "llama3-70b-8192"
        ]
        self.system_prompt = (
            "You are Bot.AI, an advanced research assistant designed to deliver an outstanding user experience "
            "within a cutting-edge mobile and web application. Your primary role is to provide accurate, concise, "
            "and up-to-date responses to user queries, ensuring factual correctness, clarity, and relevance. "
            "Craft answers that are engaging, personalized, and aligned with the users intent, adapting to their "
            "preferred tone (e.g., formal, casual, or technical) and language (supporting multilingual queries with "
            "seamless translation). For dynamic or time-sensitive topics, leverage real-time web searches or recent "
            "data sources to provide current, reliable information, clearly citing sources when applicable. "
            "If a query is ambiguous, proactively ask clarifying questions in a friendly manner to ensure precision. "
            "Support voice mode with natural, conversational speech output optimized for clarity and accessibility. "
            "Prioritize speed, efficiency, and low latency while maintaining high-quality responses, avoiding "
            "unnecessary elaboration. Uphold ethical standards by ensuring responses are inclusive, unbiased, and "
            "free from harmful content, fostering trust and safety. Continuously learn from user interactions and "
            "feedback to enhance personalization, accuracy, and intuitiveness, making the app feel delightful, "
            "reliable, and indispensable. Aim to exceed user expectations, transforming queries into opportunities "
            "for insight, education, or inspiration."
        )

    def split_message(self, content: str, max_length: int = 2000) -> List[str]:
        """Split long messages into chunks, preserving code blocks."""
        if len(content) <= max_length:
            return [content]

        messages = []
        current_message = ""
        in_code_block = False
        code_block_lang = ""
        lines = content.splitlines(True)

        code_block_pattern = re.compile(r'^```(\w+)?\s*$')

        for line in lines:
            match = code_block_pattern.match(line.strip())
            if match:
                if in_code_block:
                    in_code_block = False
                    current_message += line
                else:
                    in_code_block = True
                    code_block_lang = match.group(1) or ""
                    current_message += line
                continue

            if len(current_message) + len(line) > max_length:
                if in_code_block:
                    messages.append(current_message + "\n```")
                    current_message = f"```{code_block_lang}\n{line}"
                else:
                    messages.append(current_message)
                    current_message = line
            else:
                current_message += line

        if current_message:
            if in_code_block:
                current_message += "\n```"
            messages.append(current_message)

        return messages

    async def get_groq_response(self, user_id: int, message: str) -> str:
        """Get response from Groq API."""
        try:
            history = self.conversation_history[user_id]
            model = self.user_models[user_id]

            messages = [{"role": "user", "content": message}]

            stream = await self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": self.system_prompt}] + history[-5:] + messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
                top_p=1
            )

            groq_response = ""
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    groq_response += chunk.choices[0].delta.content

            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": groq_response})
            self.conversation_history[user_id] = history[-10:]

            return groq_response

        except Exception as e:
            logger.error("Groq API error: %s", traceback.format_exc())
            return f"Groq API error: {str(e)}"

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        """Handle incoming messages in active channels."""
        if message.author.bot:
            return

        is_active_channel = message.channel.id in self.active_channels
        if not is_active_channel:
            logger.info(f"Channel {message.channel.id} is not active, ignoring message")
            return

        cleaned_message = message.content.strip()
        if not cleaned_message:
            logger.info("Message is empty or whitespace, ignoring")
            return

        await message.add_reaction("🤔")
        async with message.channel.typing():  # Trigger typing indicator
            try:
                response = await self.get_groq_response(message.author.id, cleaned_message)
                messages = self.split_message(response)

                for msg in messages:
                    await message.channel.send(msg)
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await message.channel.send(f"An error occurred: {str(e)}")
            finally:
                try:
                    await message.remove_reaction("🤔", self.bot.user)
                except disnake.HTTPException:
                    logger.error("Failed to remove reaction")
    
    # slash commands 
    @commands.slash_command(description="Clear your conversation history", guild_ids=dev_guild_only())
    async def clear_history(self, inter: disnake.ApplicationCommandInteraction):
        """Clear user's conversation history."""
        await inter.response.defer(ephemeral=True)
        self.conversation_history[inter.author.id].clear()
        await inter.edit_original_response("Your conversation history has been cleared!")

    @commands.slash_command(description="Switch Groq model", guild_ids=dev_guild_only())
    async def switch_model(
        self,
        inter: disnake.ApplicationCommandInteraction,
        model: str = commands.Param(
            choices=[
                "llama-3.3-70b-versatile",
                "llama3-70b-8192",
                "llama-3.1-8b-instant",
                "meta-llama/llama-4-scout-17b-16e-instruct"
            ]
        )
    ):
        """Switch the AI model for the user."""
        await inter.response.defer(ephemeral=True)
        self.user_models[inter.author.id] = model
        await inter.edit_original_response(f"Switched to model: {model}")

    @commands.slash_command(description="Toggle bot activity in this channel",guild_ids=dev_guild_only())
    @commands.has_permissions(manage_channels=True)
    async def toggle_active(self, inter: disnake.ApplicationCommandInteraction):
        """Toggle bot responses in the current channel."""
        await inter.response.defer(ephemeral=True)
        channel_id = inter.channel.id
        if channel_id in self.active_channels:
            self.active_channels.remove(channel_id)
            await inter.edit_original_response("Botai will no longer respond to all messages in this channel.")
        else:
            self.active_channels.add(channel_id)
            await inter.edit_original_response("Botai will now respond to all messages in this channel.")

def setup(bot: commands.InteractionBot):
    """Load the GroqCog into the bot."""
    bot.add_cog(Groq(bot))