import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import date

# ========================
# CONFIGURAÇÕES
# ========================
TOKEN = ""

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)
# ========================
# DADOS
# ========================
dicas = [
    "Troque garrafas descartáveis por uma reutilizável 🧴♻️",
    "Evite copos descartáveis, use um copo fixo 🥤❌",
    "Separe o lixo reciclável do orgânico 🗑️",
    "Prefira comprar a granel quando possível 🌱"
]

lixos = {
    "garrafa pet": "♻️ Reciclável! Lave antes de descartar.",
    "casca de banana": "🍌 Orgânico. Pode virar adubo!",
    "embalagem de salgadinho": "❌ Geralmente não reciclável.",
    "papel": "♻️ Reciclável se estiver limpo."
}

desafios = [
    "Fique 3 dias sem usar copos descartáveis 🏆",
    "Use apenas garrafa reutilizável essa semana 💧",
    "Separe o lixo da sua casa por 5 dias ♻️"
]

# ========================
# SISTEMA DE PONTOS
# ========================
pontos = {}
ultima_dica = {}       # user_id -> data
lixo_hoje = {}         # user_id -> contagem

# ========================
# EVENTO
# ========================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🤖 Bot conectado como {bot.user}")

# ========================
# COMANDOS
# ========================

@bot.tree.command(name="dica", description="Receba uma dica sustentável 🌱")
async def dica(interaction: discord.Interaction):
    user_id = interaction.user.id
    hoje = date.today()

    if user_id not in pontos:
        pontos[user_id] = 0

    # Só ganha pontos 1x por dia
    if ultima_dica.get(user_id) != hoje:
        pontos[user_id] += 5
        ultima_dica[user_id] = hoje
        bonus = "\n+5 pontos 🌟"
    else:
        bonus = "\n(sem pontos hoje, volte amanhã 😉)"

    dica_aleatoria = random.choice(dicas)
    await interaction.response.send_message(
        f"💡 **Dica do dia:**\n{dica_aleatoria}{bonus}"
    )

@bot.tree.command(name="lixo", description="Descubra se algo é reciclável")
@app_commands.describe(item="Item que você quer verificar")
async def lixo(interaction: discord.Interaction, item: str):
    user_id = interaction.user.id

    if user_id not in pontos:
        pontos[user_id] = 0

    # Limite de 5 usos por dia
    lixo_hoje.setdefault(user_id, 0)

    if lixo_hoje[user_id] < 5:
        pontos[user_id] += 3
        lixo_hoje[user_id] += 1
        bonus = "\n+3 pontos ♻️"
    else:
        bonus = "\n(limite diário de pontos atingido)"

    resposta = lixos.get(item.lower(), "🤔 Não tenho info sobre isso ainda.")
    await interaction.response.send_message(resposta + bonus)

@bot.tree.command(name="desafio", description="Receba um desafio sustentável 🏆")
async def desafio(interaction: discord.Interaction):
    desafio_aleatorio = random.choice(desafios)
    await interaction.response.send_message(
        f"🏆 **Desafio da semana:**\n{desafio_aleatorio}\n\n"
        f"Quando completar, use `/completei`"
    )

@bot.tree.command(name="completei", description="Confirme que você completou um desafio 🏆")
async def completei(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in pontos:
        pontos[user_id] = 0

    pontos[user_id] += 50

    await interaction.response.send_message(
        f"🎉 Parabéns {interaction.user.mention}!\n"
        f"Você ganhou **+50 pontos** 🌟"
    )
@bot.tree.command(name="perfil", description="Veja seu perfil sustentável 🌍")
async def perfil(interaction: discord.Interaction):
    user_id = interaction.user.id
    pontos.setdefault(user_id, 0)

    nivel = "🌱 Iniciante Verde"
    if pontos[user_id] >= 100:
        nivel = "🍃 Eco Aprendiz"
    if pontos[user_id] >= 300:
        nivel = "🌍 Guardião do Planeta"

    await interaction.response.send_message(
        f"👤 **Perfil de {interaction.user.name}**\n"
        f"Pontos: {pontos[user_id]} ⭐\n"
        f"Nível: {nivel}"
    )

# ========================
# INICIAR BOT
# ========================
bot.run(TOKEN)
