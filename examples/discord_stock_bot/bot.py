from __future__ import annotations

import asyncio
import os

import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

from config import load_settings
from data_sources import read_stock_dataframe
from stock_days import build_stock_rows, format_top_shortage


load_dotenv()
settings = load_settings()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def build_report() -> str:
    df = await asyncio.to_thread(read_stock_dataframe, settings)
    rows = build_stock_rows(df)
    return format_top_shortage(rows)


@tree.command(name="dias_estoque", description="Mostra dias restantes por SKU")
async def dias_estoque(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    try:
        report = await build_report()
    except Exception as error:
        await interaction.followup.send(f"Erro ao ler planilha: {error}")
        return

    await interaction.followup.send(report)


@tasks.loop(hours=24)
async def daily_stock_report() -> None:
    if not settings.channel_id:
        return

    channel = client.get_channel(settings.channel_id)
    if channel is None:
        return

    try:
        report = await build_report()
        await channel.send(report)
    except Exception as error:
        await channel.send(f"Falha ao montar relatório diário: {error}")


@client.event
async def on_ready() -> None:
    guild_id = settings.guild_id
    if guild_id:
        guild = discord.Object(id=guild_id)
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)
    else:
        await tree.sync()

    if not daily_stock_report.is_running():
        daily_stock_report.start()

    print(f"Bot online como {client.user}.")


if __name__ == "__main__":
    token = settings.discord_token or os.environ["DISCORD_TOKEN"]
    client.run(token)
