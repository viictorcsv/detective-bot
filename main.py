import os

import discord
from discord import app_commands
from dotenv import load_dotenv


intents = discord.Intents.none()
intents.guilds = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


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
