import os
from dotenv import load_dotenv
import discord
from discord.ext import commands,tasks
from mascota.mascota import Mascota
import random
import asyncio


def load_discord_bot():
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='$', intents=intents)
        print("Bot cargado!")
        return bot
    except Exception as e:
        print(f"Error al cargar el bot {e}")

def is_developer(DEVELOPER_ID):
    def predicate(ctx):
        return ctx.author.id == DEVELOPER_ID
    return commands.check(predicate)

def main():
    # Cargar las variables del archivo .env
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")
    dev_id = int(os.getenv("DEV_ID"))
    # Crear una instancia de la mascota
    mascota = Mascota()

    try:
        bot = load_discord_bot()
        print("Bot generado!")
    except Exception as e:
        print(f"Error al generar el bot {e}")

    @bot.event
    async def on_ready():
        print(f"Estamos dentro! {bot.user}")
        channel = bot.get_channel(mascota.pet_channel_id)
        embed = discord.Embed(
        title="Bot en línea",
        description=f"¡{bot.user.name} está ahora en línea y funcionando correctamente!\n```Me llamo {mascota.nombre}```",
        color=discord.Color.green()  # Elige el color que prefieras
        )
        embed.set_image(url=mascota.get_random_gif("divertido"))
        await channel.send(embed=embed)
        reducir_niveles.start()

    @bot.command()
    async def test(ctx, *args):
        respuesta = ' '.join(args)
        await ctx.send(respuesta)

    @bot.command()
    async def renombrar(ctx, *args):
        nombre = ' '.join(args)
        nombre_anterior = mascota.nombre
        mascota.nombre = nombre
        mascota.guardar_atributos()

        embed = discord.Embed(
            title=f"```¡Nombre cambiado!```",
            description=f"```{nombre_anterior} a {mascota.nombre}```"
        )

        embed.set_image(url=mascota.get_random_gif("divertido"))


        await ctx.send(embed=embed)

    @bot.command()
    @is_developer(dev_id)
    async def reload(ctx):
        try:
            # Mensaje de configuración recargada
            message = await ctx.send("``` Configuraciones recargadas...```")
            
            # Esperar el tiempo deseado (por ejemplo, 10 segundos)
            await asyncio.sleep(10)
            
            # Borrar el mensaje
            await message.delete()
            await ctx.message.delete()

        except Exception as e:
            # Mensaje de error en caso de fallo
            error_message = await ctx.send(f"```Error al recargar configuraciones: {e}```")
            
            # Esperar el tiempo deseado (por ejemplo, 10 segundos) antes de borrar
            await asyncio.sleep(10)
            
            # Borrar el mensaje de error
            await error_message.delete()
            await ctx.message.delete()

    # Comando para mostrar el estado de la mascota
    @bot.command(name="estado")
    async def estado(ctx):
        
        estado_actual = (f"```Estadisticas: \n"
                        f"Hambre: {mascota.hambre}\n"
                        f"Sed: {mascota.sed}\n"
                        f"Higiene: {mascota.higiene}\n"
                        f"Felicidad: {mascota.felicidad}```")
        
        embed = discord.Embed(
            title=f"{mascota.nombre}",
            description=estado_actual
        )

        embed.set_image(url=mascota.get_random_gif("divertido"))

        await ctx.send(embed=embed)

    # Comando para alimentar a la mascota
    @bot.command(name="alimentar")
    async def alimentar(ctx):
        [url,resultado] = mascota.alimentar()
        embed = discord.Embed(
            title=f"```¡Has alimentado a {mascota.nombre}!```",
            description=resultado
        )

        embed.set_image(url=url)

        await ctx.send(embed=embed)

    # Comando para darle agua a la mascota
    @bot.command(name="beber")
    async def beber(ctx):
        [url,resultado] = mascota.dar_agua()
        embed = discord.Embed(
            title=f"```Has dado agua a {mascota.nombre}.```",
            description=resultado
        )

        embed.set_image(url=url)

        await ctx.send(embed=embed)

    # Comando para bañar a la mascota
    @bot.command(name="bañar")
    async def bañar(ctx):
        [url, resultado] = mascota.banar()
        embed = discord.Embed(
            title=f"```Has bañado a {mascota.nombre}.```" ,
            description=resultado
        )

        embed.set_image(url=url)
        await ctx.send(embed=embed)

    # Comando para jugar con la mascota
    @bot.command(name="jugar")
    async def jugar(ctx):
        [url,resultado] = mascota.jugar()
        embed = discord.Embed(
            title=f"```Has jugado con {mascota.nombre}.```" ,
            description=resultado
        )

        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @tasks.loop(minutes=40)  # Cada 60 segundos
    async def reducir_niveles():
        if mascota:
            canal = bot.get_channel(mascota.pet_channel_id)  # ID del canal donde se enviarán las alertas
            hambre_red = random.randint(mascota.min_reduccion, mascota.max_reduccion)
            sed_red = random.randint(mascota.min_reduccion, mascota.max_reduccion)
            higiene_red = random.randint(mascota.min_reduccion, mascota.max_reduccion)
            felicidad_red = random.randint(mascota.min_reduccion, mascota.max_reduccion)
            # Reducir atributos de la mascota
            mascota.hambre = max(0, mascota.hambre - hambre_red)
            mascota.sed = max(0, mascota.sed - sed_red)
            mascota.higiene = max(0, mascota.higiene - higiene_red)
            mascota.felicidad = max(0, mascota.felicidad - felicidad_red)
            # Chequear niveles críticos y enviar alerta
            if mascota.hambre <= mascota.nivel_critico or mascota.sed <= mascota.nivel_critico or mascota.higiene <= mascota.nivel_critico or mascota.felicidad <= mascota.nivel_critico:
                rol = discord.utils.get(canal.guild.roles, name=mascota.rol_alerta)
                mensaje = f"{rol.mention} \n\n ```Hambre: {mascota.hambre}\nSed: {mascota.sed}\nHigiene: {mascota.higiene}\nFelicidad: {mascota.felicidad} ```"
                url = mascota.get_random_gif("triste")
                embed = discord.Embed(
                    title= f"```⚠️ ¡Atención! {mascota.nombre} necesita cuidados:\n```",
                    description=mensaje
                )
                embed.set_image(url=url)
                await canal.send(embed=embed)


    bot.run(token)




if __name__=="__main__":
    main()