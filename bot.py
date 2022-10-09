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

# ---------------------------------------- Eventos ---------------------------------------- #

# Evento que se llama una vez el bot está listo para ser usado.
@bot.event
async def on_ready():
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
        content = str(message.content.lower())

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
    await message.channel.send(random.randint(0,6))

# Comando !limpiar
@bot.command()
@commands.has_permissions(manage_messages=True)
async def limpiar(context, amount=5):
    await context.channel.purge(limit=amount+1)

# Ejecuta el bot
bot.run(TOKEN)
