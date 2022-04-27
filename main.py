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
    """Check bot."""
    logger.info(f"{bot.user} successfully logged in!")


@bot.slash_command()
async def gas(
    ctx: ApplicationContext,
    network: Option(str, "Choose network", choices=["ETH"]),  # type: ignore
) -> None:
    """
    Get gas prices.

    :param ctx: Discord bot application context
    :param network: Blockchain network
    """
    logger.info(f"{ctx.user} executed gas command on {network} network")
    if network != "ETH":
        return
    route = [ETH_USDC, ETH_WETH]
    gas_prices = await gas_tracker.get_gasprices()
    gas_prices = {
        transaction_speed: web3.fromWei(gas_price, unit="gwei")
        for transaction_speed, gas_price in gas_prices.items()
        if gas_price
    }

    logger.info(f"Gas Oracle {gas_prices}")
    base_fee = gas_prices["regular"] - 1
    gas_limit = 65000

    async with aiofiles.open("abi/erc20_router_v2.abi", mode="r") as abi_file:
        abi_text = await abi_file.read()
        abi = json.loads(abi_text)
    contract = web3.eth.contract(
        address=UNISWAP_ROUTER_ADDRESS,
        abi=abi,
    )

    fees = {
        transaction_speed: web3.fromWei(
            contract.functions.getAmountsIn(
                web3.toWei((base_fee + gas_price) * gas_limit, "gwei"), route
            ).call()[0],
            "mwei",
        )
        for transaction_speed, gas_price in gas_prices.items()
        if gas_price
    }

    embed_message = Embed(title=f"{network} Gas Prices ⛽", colour=0xC2599B)

    for transaction_speed, gas_price in gas_prices.items():
        if transaction_speed == "fast":
            name = "Average 🚶"
        elif transaction_speed == "regular":
            name = "Slow 🦥"
        else:
            name = "Fast 🚀"
        embed_message.add_field(
            name=name, value=f"{gas_price} Gwei | Estimate: ${fees[transaction_speed]}"
        )

    await ctx.respond(embed=embed_message)


bot.run(DISCORD_BOT_TOKEN)
