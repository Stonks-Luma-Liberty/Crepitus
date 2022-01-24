import json

import aiofiles
from discord import Bot, ApplicationContext, Option, Embed

from config import (
    logger,
    gas_tracker,
    DISCORD_BOT_TOKEN,
    ETH_USDC,
    ETH_WETH,
    UNISWAP_ROUTER_ADDRESS,
)
from config import web3

bot = Bot()


@bot.event
async def on_ready():
    logger.info(f"{bot.user} successfully logged in!")


@bot.slash_command()
async def gas(
    ctx: ApplicationContext, network: Option(str, "Choose network", choices=["ETH"])
) -> None:
    logger.info(f"{ctx.user} executed gas command on {network} network")
    if network != "ETH":
        return
    route = [ETH_USDC, ETH_WETH]
    gas_prices = await gas_tracker.get_gasprices()
    gas_prices = {
        key: web3.fromWei(value, unit="gwei")
        for key, value in gas_prices.items()
        if value
    }

    logger.info(f"Gas Oracle {gas_prices}")
    base_fee = gas_prices["regular"] - 1
    gas_limit = 65000

    async with aiofiles.open("abi/erc20_router_v2.abi", mode="r") as file:
        data = await file.read()
        abi = json.loads(data)
    contract = web3.eth.contract(
        address=UNISWAP_ROUTER_ADDRESS,
        abi=abi,
    )

    fees = {
        key: web3.fromWei(
            contract.functions.getAmountsIn(
                web3.toWei((base_fee + value) * gas_limit, "gwei"), route
            ).call()[0],
            "mwei",
        )
        for key, value in gas_prices.items()
        if value
    }

    embed_message = Embed(title=f"{network} Gas Prices ⛽", colour=0xC2599B)

    for key, value_ in gas_prices.items():
        if key == "fast":
            name = "Average 🚶"
        elif key == "regular":
            name = "Slow 🦥"
        else:
            name = "Fast 🚀"
        embed_message.add_field(
            name=name, value=f"{value_} Gwei | Estimate: ${fees[key]}"
        )

    await ctx.respond(embed=embed_message)


bot.run(DISCORD_BOT_TOKEN)
