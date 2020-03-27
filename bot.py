# bot.py
import csv
import os
import discord
from discord.ext import commands

TOKEN = "Njg0MDYyMTMwMzg2ODk0OTcw.XmADZQ.McCDZLUUB7smn6SjvuagzjU8eZ8"
bot = commands.Bot(command_prefix='/')


@bot.command(name='create-channel', help='Creates channel, takes channel name as input')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await ctx.send(f'Channel {channel_name} already exists')
    else:
        await ctx.send(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='kys')
async def kill(ctx):
    await bot.close()


@bot.command(name='cov', help='Shows how many COVID-19 cases there are now in given country')
async def cov(ctx, country, type):
    confirmed = "D:/Projects/Matlab/covid/COVID-19/csse_covid_19_data/csse_covid_19_time_series" \
                "/time_series_covid19_confirmed_global.csv "
    deaths = "D:/Projects/Matlab/covid/COVID-19/csse_covid_19_data/csse_covid_19_time_series" \
             "/time_series_covid19_deaths_global.csv "
    recovered = "D:/Projects/Matlab/covid/COVID-19/csse_covid_19_data/csse_covid_19_time_series" \
                "/time_series_covid19_recovered_global.csv "
    if type == "deaths":
        localization = deaths
    elif type == "recovered":
        localization = recovered
    else:
        localization = confirmed
        type = "cases"

    with open(localization) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        date = next(csv_reader)[-1]
        success = True

        if country == "date":
            await ctx.send(f'Last update: {date}')
            success = False
        else:
            for row in csv_reader:
                if row[1] == country:
                    await ctx.send(f'There are already {row[-1]} {type} in {row[0]} {country}')
                    success = False

        if success:
            await ctx.send(f'Something went wrong')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
