import discord
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import random

# ---------------------------------------- Configuración inicial ---------------------------------------- #

# Por motivos de seguridad, no se quiere quiere tener el token del bot como una variable en el código.
# Por lo tanto, se carga un archivo .env que contiene el token asignado como un valor.
load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

# Se crea el prefijo, se crea y extrae el bot y removemos el comando help para personalizarlo.
prefix = '!'
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command('help')
staticRoute = "./static/images/"
# ---------------------------------------- Adicional ---------------------------------------- #

# Funciones para cargar configuración inicial
async def setUpVariables(init: str, log: str):
    print(init)
    global common, uncommon, rare, epic, legendary, mythic
    common = "común"
    uncommon = "poco común"
    rare = "raro"
    epic = "épico"
    legendary = "legendario"
    mythic = "mítico"
    print(log)
    
    
async def setUpImages(init: str, log: str):
    print(init)
    global commonFile, uncommonFile, rareFile, epicFile, legendaryFile, mythicFile
    commonFile = discord.File(staticRoute + "comun.png", filename="comun.png")
    uncommonFile = discord.File(staticRoute + "pococomun.png", filename="pococomun.png")
    rareFile = discord.File(staticRoute + "raro.png", filename="raro.png")
    epicFile = discord.File(staticRoute + "epico.png", filename="epico.png")
    legendaryFile = discord.File(staticRoute + "legendario.png", filename="legendario.png")
    mythicFile = discord.File(staticRoute + "mitico.png", filename="mitico.png")
    print(log)


# ---------------------------------------- Eventos ---------------------------------------- #

# Evento que se llama una vez el bot está listo para ser usado.
@bot.event
async def on_ready():
    await setUpVariables("Cargando variables globales . . .", "Variables cargadas.")
    await setUpImages("Cargando imágenes . . .", "Imágenes cargadas.")
    print('¡LevelUp Bot está listo para su uso!')

# Evento que se llama una vez un mensaje es creado y enviado.
@bot.event
async def on_message(message):
    # Si el mensaje contiene el prefijo, es un comando. Esperar a que se procese.
    if prefix in message.content:
        await bot.process_commands(message)
    else:
        author = message.author
        channel = message.channel
        content = str(message.content.strip().lower())

        # Aquí se pone cualquier algoritmo o mensaje que el bot quiera enviar en reacción a un mensaje.

        if content == "level":
            await message.reply("Up!")
        elif content == "ayer tenía un amor":
            await message.reply("que hoy me abandonó")
        elif content == "porque no me quería":
            await message.reply("fue tanta mi ilusión")
        elif content == "por hacerla feliz":
            await message.reply("pero todo fue en vano")
        elif content == "sus juramentos falsos trajeron a mi alma tristes esperanzas":
            await message.reply("que la vida nos dio con todo su fulgor, caricias y esplendor")
        
        # No tocar.
        await bot.process_commands(message)

# ---------------------------------------- Moderación ---------------------------------------- #

@bot.event
async def on_command_error(context, error):

    # Errores de Usuario.
    if isinstance(error, commands.MissingRequiredArgument):
        await context.send("Te falta un argumento en tu comando. Intenta de nuevo.")
    if isinstance(error, commands.MissingPermissions):
        await context.send("¡Lo siento usuario! Al parecer no tienes el nivel para usar ese comando.")
    if isinstance(error, commands.MissingRole):
        await context.send("¡Lo siento usuario! Al parecer no tienes el nivel para usar ese comando.")

    # Errores del Bot.
    if isinstance(error, commands.BotMissingPermissions):
        await context.send("¡Lo siento! No tengo el nivel para usar ese comando.")
    if isinstance(error, commands.BotMissingRole):
        await context.send("¡Lo siento! No tengo el nivel para usar ese comando.")
    

# ---------------------------------------- Comandos ---------------------------------------- #

# Comando !ayuda
@bot.command()
async def ayuda(message):
    name = "¡Bienvenido a LevelUp!"
    value = "Insertar descripción . . ."
    colour = discord.Colour.from_rgb(239,201,60)
    embed = discord.Embed(colour=colour, title=name, description=value)
    
    name = "Título #1"
    value = "Descripción . . ."
    embed.add_field(name=name, value=value, inline=False)
    
    name = "Título #2"
    value = "Descripción . . ."
    embed.add_field(name=name, value=value, inline=False)
    
    await message.channel.send(embed=embed)

# Comando !roll
@bot.command()
async def roll(message):
    choice = random.randint(1, 100)
    rarity = ""
    path = ""
    colour = discord.Colour.from_rgb(0, 0, 0)
    if choice <= 50:
        rarity = "común"
        path = "comun.png" # 50 of 100 = 50
        colour = discord.Colour.from_rgb(94, 94, 94)
    elif choice <= 75: 
        rarity = "poco común"
        path = "pococomun.png" # 25 of 100 = 75
        colour = discord.Colour.from_rgb(52, 124, 48)
    elif choice <= 87: 
        rarity = "raro"
        path = "raro.png" # 12 of 100 = 85
        colour = discord.Colour.from_rgb(56, 106, 132)
    elif choice <= 95: 
        rarity = "épico"
        path = "epico.png" # 8 of 100 = 92
        colour = discord.Colour.from_rgb(123, 69, 145)
    elif choice <= 98:
        rarity = "legendario"
        path = "legendario.png" # 4 of 100 = 98
        colour = discord.Colour.from_rgb(159, 122, 23)
    elif choice <= 100:
        rarity = "mítico"
        path = "mitico.png" # 2 of 100 = 100
        colour = discord.Colour.from_rgb(217, 81, 81)
    print(rarity)
    
    file = discord.File(staticRoute + path, filename=path)
    
    name = f"¡Felicidades, has encontrado un objeto {rarity}!"
    value = "Insertar descripción . . ."
    embed = discord.Embed(colour=colour, title=name, description=value)
    embed.set_image(url="attachment://" + path)
    
    name = "Título #1"
    value = "Descripción . . ."
    embed.add_field(name=name, value=value, inline=False)
    
    await message.channel.send(embed=embed, file=file)

# Comando !limpiar
@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(context, amount=5):
    await context.channel.purge(limit=amount+1)

# Ejecuta el bot
bot.run(TOKEN)
