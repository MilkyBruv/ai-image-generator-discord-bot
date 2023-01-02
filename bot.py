# Modules
import discord
from discord import app_commands
from discord.ext import commands
import openai


# set openai key
openai.api_key = "."


# Initialize bot
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
token = "."


# When the bot is online
print("Bot is starting...")

@bot.event
async def on_ready():

    print("Bot online!")

    try:

        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")

    except Exception as e:

        print(e)


# Help command
@bot.tree.command(name="commands")
async def commands(interaction: discord.Interaction):

    # Add all the commands
    embed_text = "**/help:**\nShows a list of commands and how to use them\n\n**/image <promt>:**\nGenerates an image using AI"
    
    embed = discord.Embed(title="List of commands", description=embed_text, color=0x123456)

    await interaction.response.send_message(embed=embed)


# Image generator command
@bot.tree.command(name="image")
async def image(interaction: discord.Interaction, prompt: str):

    await interaction.response.defer()

    # Generate the image
    response = openai.Image.create(

        prompt=prompt,
        n=1,
        size=f"512x512"

    )

    # Get the link to the image
    image_url = response["data"][0]["url"]
    
    # Put everything in an embed
    embed = discord.Embed(title=f"{prompt} (from {interaction.user})", color=0x898989)
    embed.set_image(url=image_url)

    # Send back the embed and the button
    await interaction.followup.send(embed=embed)


# Run the bot
bot.run(token)