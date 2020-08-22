async def owner_check(ctx):
    return ctx.author.id == ctx.bot.config["discord"]["owner"]
