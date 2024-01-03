import discord
import time
from discord.ext import commands

intents = discord.Intents.default()
uid = ADMIN_UID
intents.message_content = True
bot = commands.Bot(command_prefix='#', help_command=None, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')

@bot.command()
async def ping(ctx):
    start_time = time.time()
    sent_msg = await ctx.send("Pinging...")
    end_time = time.time()
    response_time = (end_time - start_time) * 100
    response_embed = discord.Embed(
        title="Ping",
        description=f"Response time: {response_time:.2f} ms",
        color=discord.Color.blue()
    )
    await sent_msg.edit(content="", embed=response_embed)

@bot.command()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    if ctx.author.id != uid:
        no_perms = discord.Embed(
            title="Insufficient permissions!",
            description="You do not have sufficient permissions to run this command",
            color=discord.Color.red()
        )
        await ctx.send(embed=no_perms)
        return

    await member.ban(reason=reason)
    ban_embed = discord.Embed(
        title="User banned",
        description=f"{member.name} has been banned.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=ban_embed)

@bot.command()
async def say(ctx, *, text):
    if ctx.author.id != uid:
        no_perms = discord.Embed(
            title="Insufficient permissions!",
            description="You do not have sufficient permissions to run this command",
            color=discord.Color.red()
        )
        await message.delete()
        await ctx.send(embed=no_perms)
        return

    message = ctx.message
    await ctx.reply(text)

@bot.command()
async def whois(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f"User info for {member.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Display Name", value=member.display_name, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%a, %b %d, %Y %I:%M %p UTC"), inline=True)
    embed.add_field(name="Joined Discord", value=member.created_at.strftime("%a, %b %d, %Y %I:%M %p UTC"), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", color=discord.Color.blue())
    embed.add_field(name="whois", value="Shows information about a member.", inline=True)
    embed.add_field(name="ban", value="Ban someone", inline=True)
    embed.add_field(name="say", value="Print a message", inline=True)
    embed.add_field(name="ping", value="Shows bot's response time in ms", inline=True)
    embed.add_field(name="avatar", value="Shows user's avatar", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(
        title=f"Avatar for {member.name}",
        color=discord.Color.blue(),
    )
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def announce(ctx, *, text, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(
            title=f"Announcement from {member.name}",
            description=f"{text} @everyone",
            color=discord.Color.blue()
    )
    await ctx.reply(embed=embed)

@bot.command()
async def credits(ctx):
    embed = discord.Embed(
            title="Info",
            description="Written by kevin",
            color=discord.Color.blue()
    )
    await ctx.reply(embed=embed)


@bot.command()
async def purge(ctx, limit: int):
    if ctx.author.id != uid:
        no_perms = discord.Embed(
            title="Insufficient permissions!",
            description="You do not have sufficient permissions to run this command",
            color=discord.Color.red()
        )
        await ctx.send(embed=no_perms)
        return

    if limit > 1000:
        await ctx.send("The maximum number of messages that can be purged is 1000.")
        return

    await ctx.channel.purge(limit=limit + 1)
    embed = discord.Embed(
        title="Purge Complete!",
        description=f"{limit} messages have been purged.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
async def verify(ctx):
    user = ctx.author
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = ImageCaptcha()
    data = image.generate(captcha_text)
    image.write(captcha_text, 'captcha.png')
    await ctx.send(f"Here's your CAPTCHA. Enter the code to verify!")
    await ctx.send(file=discord.File('captcha.png'))
    def check(message):
        return message.author == ctx.author and message.content == captcha_text

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        guild = ctx.guild
        role = discord.utils.get(guild.roles, id=1177239019667603538)
        if role:
            await user.add_roles(role)
            await ctx.send("You have been verified and given the role!")
        else:
            await ctx.send("Role not found.")
    except asyncio.TimeoutError:
        await ctx.send("Verification timed out. Please try again.")

bot.run('BOT_TOKEN')
