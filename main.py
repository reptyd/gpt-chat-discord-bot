"""
GPT Chat Discord Bot
--------------------

This script implements a Discord bot command (`!chat`) that forwards the user's
message to OpenAI's ChatCompletion API and returns the assistant's reply.  It
maintains a per user, per channel sliding window of the last five messages to
provide context for the model.  See README.md for setup instructions.
"""

import os
from collections import defaultdict, deque
from typing import Deque, Dict, List

import discord
from discord.ext import commands
import openai


# Maximum number of messages to retain in the history per user/channel
MAX_HISTORY = 5

# Read environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is required")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

openai.api_key = OPENAI_API_KEY

# Intents: enable message content so the bot can read commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Conversation history: history[user_id][channel_id] = deque of messages
history: Dict[int, Dict[int, Deque[Dict[str, str]]]] = defaultdict(lambda: defaultdict(lambda: deque(maxlen=MAX_HISTORY)))


@bot.command(name="chat")
async def chat(ctx: commands.Context, *, prompt: str) -> None:
    """Handle the !chat command by forwarding the prompt to OpenAI."""
    user_id = ctx.author.id
    channel_id = ctx.channel.id

    # Append the user's message to the history
    user_history = history[user_id][channel_id]
    user_history.append({"role": "user", "content": prompt})

    # Prepare the messages for OpenAI: start with a system prompt to set the assistant's behaviour
    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant embedded in a Discord server."
                " Answer concisely and clearly."
            ),
        }
    ]
    messages.extend(list(user_history))

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
        )
    except Exception as e:
        await ctx.send(f"⚠️ Failed to communicate with OpenAI API: {e}")
        return

    reply = response.choices[0].message["content"]
    # Append assistant's reply to the history
    user_history.append({"role": "assistant", "content": reply})
    await ctx.send(reply)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
