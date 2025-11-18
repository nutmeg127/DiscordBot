# Import discord and the necessary commands
import random
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import webserver

# Load the env file 
load_dotenv()

# Get the token for the bot
token = os.getenv('DISCORD_TOKEN')

# Creates or updates the discord.log file to log current bot activity
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Set up our necessary intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create the bot and give it a prefix
bot = commands.Bot(command_prefix='Nutmeg ', intents=intents)

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
                       f'Oh shit, it's {member.name} 😨', f'So, {member.name}, this is my goon cave.',
                       f'@everyone: Since {member.name} joined, I should let you know they were the reason Chill Vibe Rant got deleted!']
    
    # Display a random welcome message!
    await welcomechannel.send(random.choice(welcomemessages))
    
# This event basically reads every message that comes its way and sends an appropriate reply
@bot.event
async def on_message(message):
   # Don't want to cause an infinite loop? Then don't let the bot reply to itself!
   if message.author == bot.user:
       return

   # When we override the on_message event, we need to include this line otherwise the bot won't listen for any other messages
   await bot.process_commands(message)

   # This makes it so that there's a 1 in 5 chance of Bolu getting Pregnant Man reacted
   if(random.randint(0, 4) == 2) and (message.author != bot.user):
        if message.author.id == 971593663333429338:
            await message.add_reaction('🫃') 
    
   # Replies for the bot
   replys = [
       "Are you a twink? Can I touch you?",
    "Hold up lemme hit this hip thrust PR",
    "Would you like me if my ass measurement was 45?",
    "Let me consult ChatGPT",
    "You're kind of like Simeon Ntafos in a way.",
    "Hold up let me ask my magic 8 ball",
    "The lion agrees",
    "The lion disagrees",
    "Okay but have you considered killing yourself",
    "The lion does not care about the opinion of people like YOU",
    "I just fluked pawg status from 80%",
    "Hop on among us tn?",
    "ICE is at my door hold up",
    "*claps my cheeks*",
    "Aba is torturing me again",
    "A lion does not care about the opinions of sheep like you.",
    "Why are you staring at my ass?",
    "Hold up lemme finish this ntafos assignment",
    ]
   
   # Phrases for the bot
   phrases = ["Are you a twink? Can I touch you?",
    "Hold up lemme hit this hip thrust PR",
    "Would you like me if my ass measurement was 45?",
    "Let me consult ChatGPT",
    "You're kind of like Simeon Ntafos in a way.",
    "Hold up let me ask my magic 8 ball",
    "The lion agrees",
    "The lion disagrees",
    "The lion does not care about the opinion of people like YOU",
    "I just fluked pawg status from 80%",
    "Hop on among us tn?",
    "ICE is at my door hold up",
    "*claps my cheeks*",
    "Aba is torturing me again",
    "A lion does not care about the opinions of sheep like you.",
    "Why are you staring at my ass?",
    "Hold up lemme finish this ntafos assignment",
    "Did you know that the size of my suicidal ideation is negatively correlated with the size of my ass?", 
    "Generating a banger hold on"]
   
   # If the messages starts with Nutmeg, a random reply is sent
   if message.content.startswith('Nutmeg'):
       await message.channel.send(random.choice(replys))
   
   # Replies to the user when the bot is mentioned
   elif(bot.user in message.mentions):
        await message.channel.send(random.choice(replys))
        
   # This makes it so that there's a 1 in 5 chance of the bot replying with a random phrase
   elif(random.randint(0, 4) == 2) and (message.author != bot.user):
        await message.channel.send(random.choice(phrases))

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