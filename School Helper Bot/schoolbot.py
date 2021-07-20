from googletrans import Translator
from discord.ext import commands
from decouple import config
import random as r
import googletrans
import wikipedia
import asyncio
import discord
import os

translator = Translator()
client = commands.Bot(command_prefix="s?")
client.remove_command("help")

async def unsure(topic):
  try: p = wikipedia.page(topic)
  except wikipedia.DisambiguationError as error: topic = error.options[0]
  return await topic 

async def isint(s):
  try: 
    int(s); return await True
  except ValueError: return await False

@client.event
async def on_ready(): 
  await client.change_presence(
    status = discord.Status.online,
    activity = discord.Activity(type=discord.ActivityType.watching, name="FreeCodeCamp Tutorials")
  )
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(msg):
  if msg.author == client.user: return
  await client.process_commands(msg)

@client.command() #Help (Link to repo)
async def help(ctx):
  embed = discord.Embed(
    title = "Help",
    color = 0x62f980,
    description = "Need help? Go to the repo! (https://github.com/Not-TNB/SchoolBot/blob/main/README.md)"
  )
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRQPA8Qi7lg9kj1shVj4E4uhH6lblZKa03WOSf0Hqm_XCuQyrd3-wROXjx4qG6bol4kfA&usqp=CAU")
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command() #Ping (Latency)
async def ping(ctx): await ctx.send(f"🏓Pong!\nLatency: {round(client.latency * 1000)}ms")

@client.command(aliases = ["ws"]) #Search Article
async def wsearch(ctx, sentences="_", *, topic="Wikipedia"):
  if sentences == "_": sentences = "2"
  embed = discord.Embed(title = "Results for: " + unsure(topic), color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRQPA8Qi7lg9kj1shVj4E4uhH6lblZKa03WOSf0Hqm_XCuQyrd3-wROXjx4qG6bol4kfA&usqp=CAU")
  if len(wikipedia.summary(unsure(topic), sentences=sentences)) >= 2000: embed.description = "Sorry, your sentences argument is too large or too little"
  else:  embed.description = wikipedia.summary(unsure(topic), sentences=sentences)
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command(aliases = ["wrand"]) #Random Article
async def wrandom(ctx, sentences="_"):
  if sentences == "_": sentences = "2"
  topic = unsure(wikipedia.random())
  embed = discord.Embed(title = "Random Article: \"" + topic + "\"", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRQPA8Qi7lg9kj1shVj4E4uhH6lblZKa03WOSf0Hqm_XCuQyrd3-wROXjx4qG6bol4kfA&usqp=CAU")
  if len(wikipedia.summary(unsure(topic), sentences=sentences)) >= 2000: embed.description = "Sorry, your sentences argument is too large or too little"
  else: embed.description = wikipedia.summary(topic, sentences=sentences)
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command(aliases = ["wlang"]) #Set Language
async def wsetlang(ctx, lang=""):
  embed = discord.Embed(title = "Set Language", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRQPA8Qi7lg9kj1shVj4E4uhH6lblZKa03WOSf0Hqm_XCuQyrd3-wROXjx4qG6bol4kfA&usqp=CAU")
  if lang not in wikipedia.languages().keys():
    embed.description = "Go to https://en.wikipedia.org/wiki/List_of_Wikipedias to see a list of language prefixes"
  else:
    wikipedia.set_lang(lang)
    embed.description = "Language set to: " + wikipedia.languages()[lang]
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")
    
@client.command() #Donate Link
async def wdonate(ctx):
  embed = discord.Embed(
    title = "Donation Landing Page", 
    description = "Sent " + str(ctx.message.author) + " to the Wikimedia Donation Landing Page",
    color = 0x62f980
  )
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRQPA8Qi7lg9kj1shVj4E4uhH6lblZKa03WOSf0Hqm_XCuQyrd3-wROXjx4qG6bol4kfA&usqp=CAU")
  wikipedia.donate()
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command()
async def rps(ctx, choice=""):
  player = choice.lower()
  embed = discord.Embed(title = "Rock Paper Scissors", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://miro.medium.com/max/612/1*G9UfaUBS_VqtFILMe37fZw.jpeg")
  if player not in ["rock", "paper", "scissors"]: embed.description = "You must put rock, paper or scissors as your input"
  else:
    com = r.choice(["rock", "paper", "scissors"])
    if player == com: result = "Its a draw!"
    elif (player=="rock" and com=="scissors") or (player=="paper" and com=="rock") or (player=="scissors" and com=="paper"): result = "You win!"
    else: result = "You lost!"
    embed.description = ("You chose: " + player.upper() + "\nSchool Bot chose: " + com.upper() + "\nResult: " + result)
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command()
async def dice(ctx, sides="6"):
  embed = discord.Embed(title = "Dice Roller", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://miro.medium.com/max/10368/0*Ne__AeTXlgXayR3n")
  if not isint(sides): embed.description = "You need to give me an integer as your input"
  else:
    result = r.randint(1, int(sides))
    embed.description = "Your dice of " + sides + " side(s) has rolled a " + str(result) + "!"
  await ctx.send(embed = embed)
  await ctx.message.add_reaction("👍")

@client.command()
async def calc(ctx, calculation=""):
  embed = discord.Embed(title = "Calculator", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://lh3.googleusercontent.com/proxy/ntlyANejzMUBF3beig7zRfvf1DqbwARnrtOPY95Qg38fwC8sV_qciw0xbMnwCNv4z8iDsdGkUTl1tPs4rThfL1zZE3TOgjdjFITrjac_n0Qxta6puph-4WtOecMRqxQ9")
  chars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "+", "-", "*", "/", "%", "(", ")"]
  calculation = calculation.replace("^", "**").replace("sqrt", "math.sqrt")
  if all(c in chars for c in calculation):
    try: eval(calculation)
    except OverflowError: embed.description = "One of your calculations was too big to handle!"
    except ZeroDivisionError: embed.description = "You cant divide or modulo a number by 0!"
    except: embed.description = "Something went wrong..."
    else: embed.description = str(eval(calculation))
  await ctx.send(embed = embed)

@client.command(aliases = ["t"])
async def translate(ctx, src="auto", dest="en", *, text):
  embed = discord.Embed(title = "Translator", color = 0x62f980)
  embed.set_footer(text="School Bot")
  embed.set_thumbnail(url="https://www.jumpfly.com/wp-content/uploads/2019/09/google-translate-app-icon.jpg")
  if dest not in googletrans.LANGUAGES.keys(): embed.description = "Sorry! Your language prefix doesnt seem to be right (see https://developers.google.com/admin-sdk/directory/v1/languages)"  
  else: embed.description = f"Original Text: \n{text}\n\nTranslated Text: \n{(translator.translate(text, dest=dest)).text}"
  await ctx.send(embed = embed)

#EASTER EGGS
@client.command() #Rickroll
async def rickroll(ctx): 
  await ctx.send(file = discord.File(r"\Wikipedia Searcher\say_goodbye.jpg"))
  await ctx.message.add_reaction("👍")
@client.command() #Twerking Amogus
async def sussy_baka(ctx): 
  await ctx.send(file = discord.File(r"Wikipedia Searcher\amogus.gif"))
  await ctx.message.add_reaction("👍")
@client.command() #Return to Monke
async def reject_humanity(ctx): 
  await ctx.send(file = discord.File(r"Wikipedia Searcher\return_to_monke.jpg"))
  await ctx.message.add_reaction("👍")
@client.command() #Saddam Hussein Hiding Place
async def hiding_place(ctx): 
  await ctx.send(file = discord.File(r"Wikipedia Searcher\hiding_place.png"))
  await ctx.message.add_reaction("👍")
@client.command() #Loss Lines
async def loss(ctx):
  await ctx.send(file = discord.File(r"Wikipedia Searcher\loss.jpg"))
  await ctx.message.add_reaction("👍")

client.run(config("SCHOOL_BOT_TOKEN"))