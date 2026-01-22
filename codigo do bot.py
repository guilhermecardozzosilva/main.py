import discord
import random
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Fizemos login como {client.user}')

@client.event
async def on_member_join(member):
    canal = member.guild.system_channel
    if canal:
        await canal.send(
            f"👋 Olá {member.mention}, seja bem-vindo(a) ao **{member.guild.name}**!"
        )

def get_cat_meme():
    url = "https://api.thecatapi.com/v1/images/search"
    response = requests.get(url)
    data = response.json()
    return data[0]['url']

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('$hi'):
        await message.channel.send("Eai betinha")

    elif message.content.startswith('$bye'):
        await message.channel.send("🙂")

    elif message.content.startswith('$ping'):
        await message.channel.send("pong")

    elif message.content.startswith('$coin'):
        resultado = random.choice(["🪙 Cara", "🪙 Coroa"])
        await message.channel.send(f"O resultado foi: **{resultado}**")

    elif message.content.startswith('$dado'):
        numero = random.randint(1, 6)
        await message.channel.send(f"🎲 O dado rolou e caiu em **{numero}**")

    elif message.content.startswith('$d20'):
        numero = random.randint(1, 20)
        await message.channel.send(f"🎲 O dado rolou e caiu em **{numero}**")

    elif message.content.startswith('$MOP'):
        await message.channel.send(
            "Master Of Puppets, Battery, Lepper Messiah, "
            "Disposable Heroes, The Thing That Should Not Be, "
            "Orion, Welcome Home (Sanitarium), Damage, Inc."
        )

    elif message.content.startswith('$ppt'):
        args = message.content.split()
        if len(args) < 2:
            await message.channel.send("Use: $ppt pedra | papel | tesoura")
            return

        usuario = args[1].lower()
        opcoes = ['pedra', 'papel', 'tesoura']
        bot = random.choice(opcoes)

        if usuario not in opcoes:
            await message.channel.send("Escolha inválida!")
            return

        if usuario == bot:
            resultado = "Empate!"
        elif (
            (usuario == 'pedra' and bot == 'tesoura') or
            (usuario == 'papel' and bot == 'pedra') or
            (usuario == 'tesoura' and bot == 'papel')
        ):
            resultado = "Você ganhou! 🎉"
        else:
            resultado = "Você perdeu 😢"

        await message.channel.send(
            f"Você: **{usuario}**\n"
            f"Bot: **{bot}**\n"
            f"👉 {resultado}"
        )

    elif message.content.startswith('$cat'):
        cat_url = get_cat_meme()
        await message.channel.send(cat_url)

client.run('')
