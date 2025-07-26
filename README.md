# GPT Chat Discord Bot

This project implements a mini chat assistant inside Discord powered by OpenAI’s GPT 3.5 model.  Users can chat with the bot in any channel where it has permission.  The bot maintains the last 5 messages per user per channel to provide short‑term context and returns a coherent reply using the OpenAI Chat API.

## Purpose

Bring the power of GPT to Discord servers.  Instead of leaving the platform to use ChatGPT, users can ask questions directly in chat channels and get intelligent responses.  Conversation history is scoped to each user and channel, ensuring privacy and context separation.

## Technology Stack

* **Python 3**
* **discord.py** – to interact with Discord
* **openai** – official API client for GPT 3.5
* **collections.deque** – to manage a fixed‑size conversation history

## Installation

1. Obtain a Discord bot token and invite the bot to your server with the `Send Messages` and `Read Message History` permissions.
2. Sign up for the [OpenAI API](https://platform.openai.com/) and generate an API key.
3. Clone the repository and install dependencies:

   ```bash
   git clone https://github.com/your‑username/gpt-chat-discord.git
   cd gpt-chat-discord
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Set the following environment variables:

   - `DISCORD_TOKEN` – your Discord bot token
   - `OPENAI_API_KEY` – your OpenAI API key

5. Run the bot:

   ```bash
   python main.py
   ```

## Usage

By default the bot listens to the `!chat` command.  In any channel where the bot is present, type:

```
!chat What is the difference between a list and a tuple in Python?
```

The bot will respond with an answer.  The last five interactions with the bot are stored per user per channel to maintain a short conversation history.  Once the limit is reached the oldest messages are discarded.

## Demonstration idea (≤2 min)

1. Start recording and introduce the bot in a test channel.
2. Show how to ask a question using `!chat` and demonstrate the GPT‑generated reply.
3. Ask a follow‑up question to showcase that the bot remembers previous context for the user within the channel.
4. Open a different channel or use a different user to show that histories are isolated.
5. Emphasise that the bot uses the OpenAI API and can be extended for other tasks (translation, summarisation, code explanation, etc.).

## Possible extensions for a client

* **Persistent history** – store conversation logs in a database to provide longer context windows.
* **Rate limiting** – implement per‑user quotas to manage API costs.
* **Slash commands** – migrate from prefixed commands to Discord’s slash commands for a more native UX.
* **Rich formatting** – support code blocks and markdown in responses.
* **Multiple models** – allow users to choose between GPT 3.5 and GPT‑4 or other models via command options.

## Notes on usage

This bot uses the `openai.ChatCompletion` endpoint.  Make sure your OpenAI API usage is within your quota.  The conversation context is limited to five messages per user per channel to control token usage and costs.  Feel free to adjust the `MAX_HISTORY` constant in the code to balance context versus cost.
