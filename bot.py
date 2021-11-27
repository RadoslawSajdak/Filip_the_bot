# bot.py
from tokens import DISCORD_GUILD, DISCORD_TOKEN
import discord
from dotenv import load_dotenv
import multiprocessing
from TCP_server import tcp_server_func
from time import sleep
import socket
import subprocess

shared_list = multiprocessing.Manager().list()
connection_list = multiprocessing.Manager().list()
proc = multiprocessing.Process(target=tcp_server_func, args=(shared_list,connection_list))
proc.start()
sleep(5)
subprocess.Popen(["nodejs", "ewelink.js"])

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "Filipie, stopy!":
        response = "Tak jest, panie!"
        await message.channel.send(response)
        try:
            connection_list[0].sendall("Hotfloor ON".encode())
        except BrokenPipeError:
            connection_list.pop(0)
    elif message.content == "Stopy cieplutkie":
        response = "Cieszę się!"
        await message.channel.send(response)
        try:
            connection_list[0].sendall("Hotfloor OFF".encode())
        except BrokenPipeError:
            connection_list.pop(0)
    elif message.content == "Filipie, co umiesz?":
        response = "Filipie, stopy! - załączę Hotfloor\n" \
            "Stopy cieplutkie - wyłączę Hotfloor\n" \
            "Otwórz bramę - otworzę bramę numer 4 (WIP!!!)\n"
        await message.channel.send(response)

client.run(DISCORD_TOKEN)
