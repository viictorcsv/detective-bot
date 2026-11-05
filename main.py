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
    embed.set_footer(text="Investigue as pistas e escolha um suspeito. Expira após 5 min sem interação.")
    return embed


def criar_embed_resultado(caso, escolha):
    acertou = escolha == caso["culpado"]
    embed = discord.Embed(
        title="✅ Caso resolvido!" if acertou else "❌ Acusação incorreta",
        description=caso["titulo"],
        color=discord.Color.green() if acertou else discord.Color.red(),
    )
    embed.add_field(name="Sua acusação", value=caso["suspeitos"][escolha], inline=False)
    embed.add_field(
        name="Culpado", value=caso["suspeitos"][caso["culpado"]], inline=False
    )
    embed.add_field(name="Solução", value=caso["solucao"], inline=False)
    embed.set_footer(text="Investigação encerrada. Use /caso para jogar novamente.")
    return embed


class InvestigacaoView(discord.ui.View):
    def __init__(self, chave, caso, jogador):
        super().__init__(timeout=300)
        self.chave = chave
        self.caso = caso
        self.pistas_reveladas = 0
        self.ativa = True
        self.mensagem = None
        self.embed = criar_embed_caso(caso, jogador)
        self.selecionar.options = [
            discord.SelectOption(label=suspeito.split(" — ")[0], value=str(indice))
            for indice, suspeito in enumerate(caso["suspeitos"])
        ]
        self.remove_item(self.selecionar)

    async def interaction_check(self, interaction):
        if (interaction.guild_id, interaction.user.id) != self.chave:
            await interaction.response.send_message(
                "Esta investigação pertence a outro jogador. Use /caso para iniciar a sua.",
                ephemeral=True,
            )
            return False
        if not self.ativa or investigacoes.get(self.chave) is not self:
            await interaction.response.send_message(
                "Esta investigação foi encerrada ou substituída. Use /caso para começar outra.",
                ephemeral=True,
            )
            return False
        self.mensagem = interaction.message
        return True

    def encerrar(self, motivo):
        self.ativa = False
        if investigacoes.get(self.chave) is self:
            del investigacoes[self.chave]
        for componente in self.children:
            componente.disabled = True
        self.embed.set_footer(text=motivo)
        self.stop()

    async def atualizar_mensagem(self):
        if self.mensagem is not None:
            try:
                await self.mensagem.edit(embed=self.embed, view=self)
            except discord.HTTPException:
                # O estado continua encerrado mesmo se a mensagem tiver sido apagada.
                print("Não foi possível atualizar a mensagem da investigação.")

    async def on_timeout(self):
        self.encerrar("Tempo esgotado. Use /caso para começar outra investigação.")
        await self.atualizar_mensagem()

    async def on_error(self, interaction, error, item):
        print(f"Falha em uma interação: {type(error).__name__}.")
        try:
            texto = "Não foi possível concluir a ação. Use /caso se precisar recomeçar."
            if interaction.response.is_done():
                await interaction.followup.send(texto, ephemeral=True)
            else:
                await interaction.response.send_message(texto, ephemeral=True)
        except discord.HTTPException:
            pass  # Uma interação expirada já não permite enviar respostas.

    @discord.ui.button(label="Investigar pistas", emoji="🔎", style=discord.ButtonStyle.primary)
    async def investigar(self, interaction, button):
        total = len(self.caso["pistas"])
        if self.pistas_reveladas < total:
            self.pistas_reveladas += 1
            texto = f"Nova pista descoberta! Evidências: {self.pistas_reveladas}/{total}."
        else:
            texto = "Não existem novas evidências. Consulte abaixo todas as pistas obtidas."
        embed = discord.Embed(
            title=f"🔐 Pistas — {self.caso['titulo']}",
            description=texto,
            color=discord.Color.gold(),
        )
        for indice, pista in enumerate(self.caso["pistas"][:self.pistas_reveladas], start=1):
            embed.add_field(name=f"Pista {indice}", value=pista, inline=False)
        embed.set_footer(text="Somente você vê estas pistas. O botão permite consultá-las novamente.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Acusar suspeito", emoji="⚖️", style=discord.ButtonStyle.danger)
    async def acusar(self, interaction, button):
        if self.selecionar not in self.children:
            self.add_item(self.selecionar)
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder="Escolha o culpado — a seleção encerra o caso", row=1)
    async def selecionar(self, interaction, select):
        escolha = int(select.values[0])
        resultado = criar_embed_resultado(self.caso, escolha)
        # Encerra antes do await para impedir duas acusações simultâneas.
        self.encerrar("Investigação concluída. Use /caso para jogar novamente.")
        try:
            await interaction.response.send_message(embed=resultado, ephemeral=True)
        finally:
            await self.atualizar_mensagem()


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
            "Use /caso e leia o relato. Clique em **Investigar pistas** para revelar "
            "uma pista por vez e consultar as anteriores em uma resposta privada. "
            "Clique em **Acusar suspeito** para abrir o menu. Selecionar um nome "
            "encerra o caso e revela a solução, mesmo se você errar."
        ),
        inline=False,
    )
    embed.add_field(
        name="Novo caso e tempo limite",
        value=(
            "Só o dono pode usar os controles. /caso substitui sua investigação atual "
            "e pode sortear o mesmo mistério. Após 5 minutos sem interação, o caso expira."
        ),
        inline=False,
    )
    embed.set_footer(text="Uma investigação por jogador em cada servidor. O resultado é privado.")
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
    view = InvestigacaoView(chave, caso, interaction.user)
    aviso = "A investigação anterior foi substituída." if chave in investigacoes else None
    try:
        await interaction.response.send_message(content=aviso, embed=view.embed, view=view)
    except discord.HTTPException:
        view.stop()
        raise
    anterior = investigacoes.get(chave)
    investigacoes[chave] = view
    if anterior is not None:
        anterior.encerrar("Investigação substituída por um novo caso.")
        await anterior.atualizar_mensagem()
    try:
        view.mensagem = await interaction.original_response()
    except discord.HTTPException:
        pass  # O próximo clique também fornece a mensagem para a View.
    if not view.ativa:
        await view.atualizar_mensagem()


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
