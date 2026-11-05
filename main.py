import os
import random

import discord
from discord import app_commands
from dotenv import load_dotenv

from casos import CASOS


intents = discord.Intents.none()
intents.guilds = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)
investigacoes = {}


def carregar_configuracao():
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    token = os.getenv("DISCORD_TOKEN", "").strip()
    servidor_id = os.getenv("DISCORD_GUILD_ID", "").strip()

    if not token or token == "cole_seu_token_aqui":
        raise ValueError("Preencha DISCORD_TOKEN no arquivo .env.")

    if not servidor_id.isascii() or not servidor_id.isdecimal():
        raise ValueError("DISCORD_GUILD_ID deve ser o ID numérico do servidor.")

    if not 0 < int(servidor_id) < 2**64:
        raise ValueError("DISCORD_GUILD_ID está fora do intervalo permitido.")

    return token, discord.Object(id=int(servidor_id))


def criar_embed_caso(caso, jogador):
    embed = discord.Embed(
        title=f"🔎 Caso {caso['id']:02d} — {caso['titulo']}",
        description=caso["descricao"],
        color=discord.Color.dark_blue(),
    )
    embed.set_author(name=f"Detetive: {jogador.display_name}")
    for numero, suspeito in enumerate(caso["suspeitos"], start=1):
        embed.add_field(name=f"Suspeito {numero}", value=suspeito, inline=False)
    embed.set_footer(text="Leia o relato e os suspeitos. /caso inicia outra investigação.")
    return embed


@tree.command(name="ajuda", description="Conheça o DetectiveBot e os comandos disponíveis.")
@app_commands.guild_only()
async def ajuda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🕵️ DetectiveBot — Central de investigação",
        description="Assuma o papel de detetive em mistérios fictícios de Eldoria.",
        color=discord.Color.teal(),
    )
    embed.add_field(name="/ajuda", value="Exibe estas instruções.", inline=False)
    embed.add_field(
        name="/caso",
        value="Sorteia um dos três mistérios e apresenta o relato e os suspeitos.",
        inline=False,
    )
    embed.add_field(
        name="Como começar",
        value=(
            "Use /caso e leia o relato com atenção. Observe os três suspeitos "
            "e formule suas hipóteses. Use /caso novamente para substituir "
            "sua investigação atual; o sorteio pode repetir o mistério."
        ),
        inline=False,
    )
    embed.set_footer(text="Uma investigação por jogador em cada servidor.")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="caso", description="Inicie uma investigação com um mistério aleatório.")
@app_commands.guild_only()
async def iniciar_caso(interaction: discord.Interaction):
    if interaction.guild_id is None:
        await interaction.response.send_message(
            "Use /caso dentro de um servidor.", ephemeral=True
        )
        return

    chave = (interaction.guild_id, interaction.user.id)
    caso = random.choice(CASOS)
    aviso = "A investigação anterior foi substituída." if chave in investigacoes else None
    await interaction.response.send_message(
        content=aviso,
        embed=criar_embed_caso(caso, interaction.user),
    )
    investigacoes[chave] = {
        "caso": caso,
        "pistas_reveladas": 0,
        "ativa": True,
    }


@bot.event
async def on_ready():
    print(f"DetectiveBot online como {bot.user} (ID: {bot.user.id}).")


def main():
    try:
        token, servidor = carregar_configuracao()
    except ValueError as erro:
        raise SystemExit(str(erro)) from None

    @bot.event
    async def setup_hook():
        # A sincronização acontece uma vez no login, antes da conexão ao gateway.
        tree.copy_global_to(guild=servidor)
        comandos = await tree.sync(guild=servidor)
        print(f"{len(comandos)} comando(s) sincronizado(s) no servidor {servidor.id}.")

    try:
        bot.run(token)
    except discord.LoginFailure:
        raise SystemExit("Token inválido. Confira DISCORD_TOKEN no .env.") from None
    except discord.Forbidden:
        raise SystemExit(
            "Acesso negado. Confira o servidor e o convite com bot e applications.commands."
        ) from None
    except (discord.HTTPException, OSError):
        raise SystemExit(
            "Não foi possível conectar ou sincronizar. Confira a rede e DISCORD_GUILD_ID."
        ) from None


if __name__ == "__main__":
    main()
