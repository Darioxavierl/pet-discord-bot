import os
from dotenv import load_dotenv
import discord
from discord.ext import commands,tasks
import requests
from mascota.mascota import Mascota
import random


def load_discord_bot():
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='$', intents=intents)
        print("Bot cargado!")
        return bot
    except Exception as e:
        print(f"Error al cargar el bot {e}")

def main():
    # Cargar las variables del archivo .env
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    # Crear una instancia de la mascota
    mascota = Mascota("Neko")
    # Definir el nivel crítico y el rol de alerta
    NIVEL_CRITICO = 20
    ROL_ALERTA = "Papis"  # El nombre del rol que será etiquetado
    PET_CHANNEL_ID = 1302037809045049374

    try:
        bot = load_discord_bot()
        print("Bot generado!")
    except Exception as e:
        print(f"Error al generar el bot {e}")

    @bot.event
    async def on_ready():
        print(f"Estamos dentro! {bot.user}")
        reducir_niveles.start()

    @bot.command()
    async def test(ctx, *args):
        respuesta = ' '.join(args)
        await ctx.send(respuesta)

    # Comando para mostrar el estado de la mascota
    @bot.command(name="estado")
    async def estado(ctx):
        estado_actual = (f"```  Estado de: {mascota.nombre}     \n"
                        f"Hambre: {mascota.hambre}\n"
                        f"Sed: {mascota.sed}\n"
                        f"Higiene: {mascota.higiene}\n"
                        f"Felicidad: {mascota.felicidad}```")
        await ctx.send(estado_actual)

    # Comando para alimentar a la mascota
    @bot.command(name="alimentar")
    async def alimentar(ctx):
        [url,resultado] = mascota.alimentar()
        embed = discord.Embed(
            title=f"¡Has alimentado a {mascota.nombre}!",
            description=resultado
        )

        embed.set_image(url=url)

        await ctx.send(embed=embed)

    # Comando para darle agua a la mascota
    @bot.command(name="beber")
    async def beber(ctx):
        [url,resultado] = mascota.dar_agua()
        embed = discord.Embed(
            title=f"Has dado agua a {mascota.nombre}.",
            description=resultado
        )

        embed.set_image(url=url)

        await ctx.send(embed=embed)

    # Comando para bañar a la mascota
    @bot.command(name="bañar")
    async def bañar(ctx):
        [url, resultado] = mascota.banar()
        embed = discord.Embed(
            title=f"Has bañado a {mascota.nombre}." ,
            description=resultado
        )

        embed.set_image(url=url)
        await ctx.send(embed=embed)

    # Comando para jugar con la mascota
    @bot.command(name="jugar")
    async def jugar(ctx):
        [url,resultado] = mascota.jugar()
        embed = discord.Embed(
            title=f"Has jugado con {mascota.nombre}." ,
            description=resultado
        )

        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @tasks.loop(minutes=40)  # Cada 60 segundos
    async def reducir_niveles():
        if mascota:
            canal = bot.get_channel(PET_CHANNEL_ID)  # ID del canal donde se enviarán las alertas
            hambre_red = random.randint(1, 20)
            sed_red = random.randint(1, 20)
            higiene_red = random.randint(1, 20)
            felicidad_red = random.randint(1, 20)
            # Reducir atributos de la mascota
            mascota.hambre = max(0, mascota.hambre - hambre_red)
            mascota.sed = max(0, mascota.sed - sed_red)
            mascota.higiene = max(0, mascota.higiene - higiene_red)
            mascota.felicidad = max(0, mascota.felicidad - felicidad_red)
            # Chequear niveles críticos y enviar alerta
            if mascota.hambre <= NIVEL_CRITICO or mascota.sed <= NIVEL_CRITICO or mascota.higiene <= NIVEL_CRITICO or mascota.felicidad <= NIVEL_CRITICO:
                rol = discord.utils.get(canal.guild.roles, name=ROL_ALERTA)
                mensaje = f"{rol.mention} \n > **Hambre**: `{mascota.hambre}`\n > **Sed**: `{mascota.sed}`\n > **Higiene**: `{mascota.higiene}`\n > **Felicidad**: `{mascota.felicidad}`"
                url = mascota.get_random_gif("triste")
                embed = discord.Embed(
                    title= f"⚠️ ¡Atención! {mascota.nombre} necesita cuidados:\n",
                    description=mensaje
                )
                embed.set_image(url=url)
                await canal.send(embed=embed)


    bot.run(token)




if __name__=="__main__":
    main()