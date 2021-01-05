import os
import discord
from dotenv import load_dotenv
from random import randint
from math import floor
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

prefix = "+"
debug = True
version = "1.1"
width = 9
height = 9
nBombs = 20
board = [[0 for i in range(width)] for j in range(height)]
bombs = [[0, 0]] * nBombs
emojis = [":blue_square:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]
emojiBomb = ":boom:"


def genBomb(bombs):
    x = randint(0, width - 1)
    y = randint(0, height - 1)
    if [x, y] in bombs:
        return genBomb(bombs)
    return [x, y]


def genBoard():
    newBoard = [[0 for i in range(width)] for j in range(height)]
    bombs = [[0, 0]] * nBombs
    for i in range(nBombs):
        b = genBomb(bombs)
        bombs[i] = b
        newBoard[b[1]][b[0]] = 10
        for y in range(-1, 2):
            for x in range(-1, 2):
                yc = b[1] + y
                xc = b[0] + x
                if 0 <= xc < width and 0 <= yc < height:
                    newBoard[yc][xc] += 1
    placeVoid = True
    i = 0
    while placeVoid and i < 200:
        x = randint(0, width - 1)
        y = randint(0, height - 1)
        if newBoard[y][x] == 0:
            newBoard[y][x] = -10
            placeVoid = False
        i += 1
    return (newBoard, bombs)


def printBoard(b):
    output = ""
    output += "```markdown\n"
    output += "##### MINESWEEPER #####\n"
    output += "*v{} by Yolwoocle#6689*\n".format(version)
    output += "```"
    output += "**Size:** {0}x{1} · ".format(width, height)
    output += "**Mines:** {0} ({1}%)\n".format(nBombs, floor(nBombs / (height * width) * 100))
    output += "`Start from the blue square`\n"
    for i in b:
        for j in i:
            if j < 0:
                output += emojis[0]
            elif j < 9:
                output += "{1}{0}{1}".format(emojis[j], "||")
            else:
                output += "{1}{0}{1}".format(emojiBomb, "||")
        output += "\n"
    return output


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="@ me to play!"))


@client.event
async def on_message(message):
    mention = f'<@!{client.user.id}>'
    msg = message.content
    if mention in msg:
        board, bombs = genBoard()
        msg = printBoard(board)
        await message.channel.send(msg)


client.run(TOKEN)