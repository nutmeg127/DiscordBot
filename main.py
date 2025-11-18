# Import discord and the necessary commands
import random
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver
from groq import Groq
import pathlib

# Load the env file 
# Get the directory where this script is located
script_dir = pathlib.Path(__file__).parent.resolve()
env_path = script_dir / '.env'
print(f"DEBUG: Looking for .env at: {env_path}")
print(f"DEBUG: .env exists: {env_path.exists()}")
load_dotenv(dotenv_path=str(env_path))

# Get the token for the bot
token = os.getenv('DISCORD_TOKEN')

# Get the token for Groq
groq_api_key = os.getenv("GROQ_API_KEY")
print(f"DEBUG: API key loaded: {groq_api_key is not None}")
if groq_api_key is None:
    raise ValueError("GROQ_API_KEY not found in environment variables. Make sure .env file exists and is properly formatted.")
client = Groq(api_key=groq_api_key)

# Creates or updates the discord.log file to log current bot activity
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Set up our necessary intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create the bot and give it a prefix
bot = commands.Bot(command_prefix='Nutmeg ', intents=intents)

# LLM Section
def generate_llm_reply(user_text: str, username: str) -> str:
    """
    Call the LLM and get a reply in your style.
    """
    # Load system prompt from prompt.txt file
    prompt_file = pathlib.Path(__file__).parent / 'prompt.txt'
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read().strip()
    except FileNotFoundError:
        system_prompt = "You are Nutmeg, a helpful Discord bot."
        print("Warning: prompt.txt not found, using default prompt")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{username}: {user_text}"}
        ],
        max_tokens=60,
        temperature=0.9,
    )

    return response.choices[0].message.content

# Message displayed when bot is running
@bot.event
async def on_ready():
    print("Ready to go!")

# Displays a welcome message when a user joins
@bot.event
async def on_member_join(member):
    # Get the welcome channel ID
    welcomechannel = bot.get_channel(1387631583900602491)
    
    # If the bot doesn't have the channel ID yet, fetch it
    if welcomechannel is None:
        welcomechannel = await bot.fetch_channel(1387631583900602491)
    
    # An array that contains random welcome messages
    welcomemessages = [f'Did I know you from Chill Vibe Rant {member.name}?', f'Oh great, it\'s {member.name}',
                       f'Oh shit, its {member.name}',
                       f'So, {member.name}, this is my goon cave.',
                       f'@everyone: Since {member.name} joined, I should let you know they were the reason Chill Vibe Rant got deleted!']
    
    # Display a random welcome message!
    await welcomechannel.send(random.choice(welcomemessages))
    
# This event basically reads every message that comes its way and sends an appropriate reply
@bot.event
async def on_message(message):
    # Don't reply to yourself
    if message.author == bot.user:
        return

    # Make sure commands still work
    await bot.process_commands(message)

    # Keep your Pregnant Man reaction logic
    if (random.randint(0, 4) == 2) and (message.author != bot.user):
        if message.author.id == 971593663333429338:
            await message.add_reaction('🫃')

    # If user calls prefix (Nutmeg ...) OR mentions the bot → use LLM
    if message.content.startswith('Nutmeg') or (bot.user in message.mentions):
        try:
            reply_text = generate_llm_reply(
                user_text=message.content,
                username=message.author.display_name
            )
        except Exception as e:
            # Fallback if API dies
            print(f"LLM error: {e}")
            fallback_responses = [
                "Bro I'm broke, my OpenAI credits ran out 💀",
                "My brain's offline (ran out of API credits)",
                "Hold up lemme check my bank account... oh wait I'm broke",
                "ERROR 429: Too broke to think rn",
                "ChatGPT said no more free thoughts for me today"
            ]
            reply_text = random.choice(fallback_responses)
        
        try:
            await message.channel.send(reply_text)
        except Exception as e:
            print(f"Error sending message: {e}")
        return

        
# Command that allows the bot to join the VC when "summoned"
@bot.command()
async def join(ctx):
    # Check if the command author is in a VC first
    if ctx.author.voice:
        # Grab the voice channel and connect if the user is present
        voicechannel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voicechannel.connect()
        else:
            await ctx.voice_client.move_to(voicechannel)
    else:
        await ctx.send('Join a VC first dumbass')

# Of course we have to run the bot, so this runs the bot
webserver.keep_alive()
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
