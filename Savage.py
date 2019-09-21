import discord
import time
import datetime
import asyncio
import os
import pickle
import ffmpeg
import youtube_dl
import emoji
from discord.ext import commands
from itertools import cycle
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

prefix = 'us.'

client = commands.Bot(command_prefix='us.')
client.remove_command('help')
servers = [564685379173613568]
bot_location = "E:\\Coding_Practice\\Python\\Savage_Discord_Bot"
log_location = bot_location + "\\Savage_Logs"
log_name = time.strftime("%m_%d_%y.txt")
joined_file = log_location + "\\" + time.strftime("%m_%d_%y_Savage_Joined_Number.txt")
message_count_file = log_location + "\\" + time.strftime("%m_%d_%y_Savage_Number_File.txt")
sugestions_location = log_location + "\\Sugestions_File.txt"
delay_log = 900
bot_name = "$ɒʋɒɢə"
Creator = "-=UNiTY=- AriatCowboy"
Founder = "ßøηez"
message_history_file = log_location + "\\" + time.strftime("%m_%d_%y_Savage_Message_History.txt")
valid_users = [Creator + "#0404", Creator + "#3827", "Bonez#5941", "404_Ghost#0732"]
bad_words = []#["nigger", "shit", "fuck", "ass", "bitch", "bastard", "dick", "penis", "vagina", "cock", "tit", "boob", "pussy", "damn", "cunt", "piss", "nigga", "cracker", "arse", "twat", "bollocks", "a$$", "d1ck", "d|ck", "sh1t", "n1gger", "alladamnit", "dmmit", "dammit", "fag", "homo", "p3nn15", "bugga", "whore"]
lordsname = []#["jesus", "god", "lord", "christ"]
GuestID = 566831538550079502
status = ["$ɒʋɒɢə Music", "Type " + prefix + "help", "Type " + prefix + "music", "I Love My Creator", "We have the best Founder", "Be Savage", "United as Savages", "No Homo", "Alright Alright Alright", "YAOOO"]
play_music = [prefix + "yt", prefix + "queue", prefix + "pause", prefix + "resume", prefix + "volume", prefix + "join", prefix + "skip", prefix + "stop"]
players = []
queues = []

#Writes to a log file
async def open_log_file():
	time = datetime.datetime.now()
	message_count = read_message_count()
	joined = read_joined_count()
	log_file_location = log_location + '\\' + log_name
	if os.path.isfile(log_file_location):
		write_log = open(log_file_location, "a")
		with write_log as wl:
			wl.write('Time: {}, Message Count: {}, New Member Count: {}\n'.format(time, message_count, joined))
	else:
		write_log = open(log_file_location, "w")
		with write_log as wl:
			wl.write('Time: {}, Message Count: {}, New Member Count: {}\n'.format(time, message_count, joined))

#Function called to start the updating of the log file
async def update_logs():
	await client.wait_until_ready()
	while not client.is_closed():
		try:
			await open_log_file()
			message_count = 0
			joined = 0
			await asyncio.sleep(delay_log)
		except Exception as e:
			print(e)
			await asyncio.sleep(delay_log)

#reads file that keeps track of the amount of member joined per day
def read_joined_count():
	joined = 0
	if os.path.isfile(joined_file):
		read_joined_file = open(joined_file, "rb")
		with read_joined_file as wjf:
			joined = pickle.load(read_joined_file)
			return joined
	else:
		return joined

#writes the joined number to a file
def write_joined_count():
	joined = read_joined_count() + 1
	with open(joined_file, "wb") as wjf:
		pickle.dump(joined, wjf)

#reads the message count file that keeps track of how many messages were sent
def read_message_count():
	message_count = 0
	if os.path.isfile(message_count_file):
		read_message_count_file = open(message_count_file, "rb")
		with read_message_count_file as wjf:
			message_count = pickle.load(read_message_count_file)
			return message_count
	else:
		return message_count

#writes the the file that keeps track of the amount of messages sent per day
def write_message_count():
	message_count = read_message_count() + 1
	with open(message_count_file, "wb") as f:
		pickle.dump(message_count, f)

#logs all the data into a easy to read formate in a TXT file
def log_message_data(time, author, content, channel):
	try:
		if os.path.isfile(message_history_file):
			write_chat_history = open(message_history_file, "a")
			with write_chat_history as wch:
				wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, content, channel))
		else:
			write_chat_history = open(message_history_file, "w")
			with write_chat_history as wch:
				wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, content, channel))
	except:
		UnicodeEncodeError

#changes the bots status
async def change_status():
	await client.wait_until_ready()
	msgs = cycle(status)
	while not client.is_closed():
		current_status = next(msgs)
		await client.change_presence(activity=discord.Game(name=current_status))
		await asyncio.sleep(5)

#initializes tha bot
@client.event
async def on_ready():
	print(f"Logged in as {client.user}, {client.user.name}, {client.user.id}")

#when a member joines the server gives the guest tab and keeps a log of it within a channel called guest-log
@client.event
async def on_member_join(member):
	write_joined_count()
	role = discord.utils.get(member.guild.roles, name='Guest')
	await member.add_roles(role)
	for channel in member.guild.channels:
		if str(channel) == "guest-log":
			await channel.send("{} has joined the community. Say Hi to the player and set their roles.".format(member.name))

#if someone tries to updata their nickname to the bots name it will not let them
@client.event
async def on_member_update(before, after):
	Creator_names = Creator
	nickname = after.nick
	last = before.nick
	if nickname:
		if nickname.lower().count(bot_name) > 0:
			if last:
				await after.edit(nick=last)
			else:
				await after.edit(nick="ThereCanOnlyBeOne")

#keeps track of the emojies added to posts and append it to the message history file
@client.event
async def on_reaction_add(reaction, user):
	reaction_convert = emoji.demojize(str(reaction))
	time = datetime.datetime.now()
	channel = reaction.message.channel
	print(reaction_convert)
	if os.path.isfile(message_history_file):
		write_chat_history = open(message_history_file, "a")
		with write_chat_history as wch:
			wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
			print('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
			print('Appended file')
	else:
		write_chat_history = open(message_history_file, "w")
		with write_chat_history as wch:
			wch.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
			print('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\nEmoji: {}\n\n'.format(time, user.name, reaction.message.content, channel, reaction_convert))
			print('Created new file')


#checks if there is a curse word or someone using some sort of offensive language
@client.event
async def on_message(message):
	write_message_count()
	userID = message.author.id
	msg = message.content.lower()
	author = message.author
	content = message.content
	channel = message.channel
	channels = ["bot-command-center", "general"]
	musicchannel = "music-bot"
	time = datetime.datetime.now()
	print('{} {} {}'.format(time, author, content, channel))
	log_message_data(time, author, content, channel)
	if str(message.channel) == musicchannel:
		for word in play_music:
			if msg.startswith(word):
				if message.author == client.user:
					return
				else:
					await client.process_commands(message)
	else:
		for word in bad_words:
			if message.content.count(word) > 0:
				print("A Bad word was said. Message Deleted.")
				await message.delete()
				if msg.startswith(prefix + "say"):
					await author.send('{0.author.mention}, You cannot make me curse!'.format(message))
					return
				else:
					await author.send('Hello {0.author.mention}, Stop Cursing!'.format(message))
					return
		for word in lordsname:
			if message.content.count(word) > 0:
				print('They Said Something Offencive So I Took The Liberty To Delete It.')
				await message.delete()
				await author.send('Do Not Say The Lords Name In Vein!{0.author.mention}'.format(message))
		if str(channel) in channels:
			if message.author == client.user:
				return
			else:
				await client.process_commands(message)

@client.command()
async def suggest(ctx, *args):
	output = ''
	time = datetime.datetime.now()
	author = ctx.message.author
	count = len(args)
	for word in args:
		output += word
		if count > 1:
			count = count - 1
			output += ' '
	channel = ctx.message.channel
	if os.path.isfile(sugestions_location):
		write_sugest = open(sugestions_location, "a")
		with write_sugest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')
	else:
		write_sugest = open(sugestions_location, "w")
		with write_sugest as ws:
			ws.write('Time: {}\nAuthor: {}\nContent: {}\nChannel: {}\n\n'.format(time, author, output, channel))
			await ctx.send('Suggestion has been sent!')

# plays the shortest game of Ping Pong with the user
@client.command()
async def ping(ctx):
	await ctx.send('Pong!')

#Gives the user a status of everyone online, idle, and offline
@client.command()
async def report(ctx):
	message_channel = ctx.message.channel
	usguild = client.get_guild(servers)
	online = 0
	idle = 0
	offline = 0
	for mem in usguild.members:
		if str(mem.status) == "online":
			online += 1
		if str(mem.status) == "offline":
			offline += 1
		else:
			idle += 1
	author = ctx.message.author
	embed = discord.Embed(colour=discord.Colour.green())
	embed.set_author(name='Status')
	embed.add_field(name="Online", value=online, inline=False)
	embed.add_field(name="Offline", value=offline, inline=False)
	embed.add_field(name="Idle", value=idle, inline=False)
	await ctx.channel.send(embed=embed) 

#echoes what the user said
@client.command()
async def say(ctx, *args):
	output = ''
	for word in args:
		output += word
		if count > 1:
			count = count - 1
			output += ' '
	output
	await ctx.send('{0.author.mention} '.format(ctx) + output)

#logs the bot offline
@client.command()
async def logoff(ctx):
	if str(ctx.author) in valid_users:
		await ctx.message.author.send('Hello {0.author.mention}, I\'m Logging off!'.format(ctx))
		await client.close()
	else:
		await ctx.message.author.send('Hello {0.author.mention}, You dont have permission!'.format(ctx))

#The next 4 commands are variation on hello to the bot, which replies acordingly
@client.command()
async def hello(ctx):
	userID = ctx.author.id
	if userID == 149044658549424128 or userID == 149042697305456640:
		await ctx.send('Hello {0.author.mention}, My Creator!'.format(ctx))
	elif userID == 108068068231491584:
		await ctx.send('Hello {0.author.mention}, The Founder of United Savages!'.format(ctx))
	else:
		await ctx.send('Hello {0.author.mention}, You Are A Savage!'.format(ctx))

@client.command()
async def sup(ctx):
	userID = ctx.author.id
	if userID == 149044658549424128 or userID == 149042697305456640:
		await ctx.send('My Services, {0.author.mention}'.format(ctx))
	elif userID == 108068068231491584:
		await ctx.send('Shut up B****, Alright Alright Alright. You Gonna Learn today {0.author.mention}.'.format(ctx))
	else:
		await ctx.send('Discord is, {0.author.mention}'.format(ctx))

@client.command()
async def whatsup(ctx):
	userID = ctx.author.id
	if userID == 149044658549424128 or userID == 149042697305456640:
		await ctx.send('The Sky, {0.author.mention}'.format(ctx))
	elif userID == 108068068231491584:
		await ctx.send('This long d***, {0.author.mention}'.format(ctx))
	else:
		await ctx.send('The Sun, {0.author.mention}'.format(ctx))

@client.command()
async def whatup(ctx):
	userID = ctx.author.id
	if userID == 149044658549424128 or userID == 149042697305456640:
		await ctx.send('Oh your back, {0.author.mention}'.format(ctx))
	elif userID == 108068068231491584:
		await ctx.send('What It Do, {0.author.mention}'.format(ctx))
	else:
		await ctx.send('Sup, {0.author.mention}'.format(ctx))

#counts the amount of members on the server
@client.command()
async def usercount(ctx):
	for ID in servers:
		try:
			client.get_guild(ID)
			if client.get_guild(ID):
				serverID = client.get_guild(ID)
				await ctx.message.author.send(f"""Number of Members: {serverID.member_count}""")
		except:
			ValueError

#clears a certian amount of user defined messages
@client.command(pass_context=True)
async def clear(ctx, amount):
	if str(ctx.author) in valid_users:
		amount = int(amount)
		amount += 1
		channel = ctx.message.channel
		messages = []
		async for message in channel.history(limit=amount):
			messages.append(message)
		await channel.delete_messages(messages)
		await ctx.message.author.send('Messages Deleted!')
	else:
		await ctx.message.author.send('You do not have permission to do that.')

#displays the help command
@client.command(pass_context=True)
async def help(ctx):
	author = ctx.message.author
	embed = discord.Embed(colour=discord.Colour.green())
	embed.set_author(name='Help')
	embed.add_field(name=prefix + 'ping', value='Plays Ping Pong', inline=False)
	embed.add_field(name=prefix + 'say', value='Echos what you enter after command', inline=False)
	embed.add_field(name=prefix + 'logoff', value='Logs off $ɒʋɒɢə. Requires certain perms from within', inline=False)
	embed.add_field(name=prefix + 'hello', value='Says hello to the user', inline=False)
	embed.add_field(name=prefix + 'sup', value='Says sup to the user', inline=False)
	embed.add_field(name=prefix + 'whatsup', value='Says something to the user', inline=False)
	embed.add_field(name=prefix + 'whatup', value='Says a greeting to the user', inline=False)
	embed.add_field(name=prefix + 'usercount', value='Counts all users on the server', inline=False)
	embed.add_field(name=prefix + 'clear', value='Deletes Messages. Requires certain perms from within', inline=False)
	embed.add_field(name=prefix + 'help', value='Displays this menu', inline=False)
	embed.add_field(name=prefix + 'music', value='Displays music help menu', inline=False)
	embed.add_field(name=prefix + 'suggest', value='Enter your suggestions for the bot.', inline=False)
	embed.add_field(name=prefix + 'report', value='Gives you a status report of the current members of the discord.', inline=False)
	await author.send(embed=embed) 
	
#displays the music bot help command
@client.command(pass_context=True)
async def music(ctx):
	author = ctx.message.author
	embed = discord.Embed(colour=discord.Colour.green())
	embed.set_author(name='Help')
	embed.add_field(name=prefix + 'join', value='Joins server (must add channel name)', inline=False)
	embed.add_field(name=prefix + 'yt', value='Posts a YT link', inline=False)
	embed.add_field(name=prefix + 'volume', value='Changes the volume', inline=False)
	embed.add_field(name=prefix + 'stop', value='Kicks savage from channel', inline=False)
	embed.add_field(name=prefix + 'queue', value='Adds song to queue', inline=False)	
	embed.add_field(name=prefix + 'pause', value='Pauses current song', inline=False)	
	embed.add_field(name=prefix + 'resume', value='Resumes current song', inline=False)
	embed.add_field(name=prefix + 'skip', value='Skips current song', inline=False)	
	await author.send(embed=embed) 


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '10.0.0.160' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.1):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


def check_queue(ctx, queues, players):
	if queues != []:
		player = queues.pop(0)
		players = player
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))

@client.command()
async def play(ctx, *, query):
	"""Plays a file from the local filesystem"""
	source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
	ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))
	await ctx.send('Now playing: {}'.format(query))

@client.command()
async def join(ctx, *, channel: discord.VoiceChannel):
	"""Joins a voice channel"""
	if ctx.voice_client is not None:
		return await ctx.voice_client.move_to(channel)
	await channel.connect()

@client.command()
async def yt(ctx, *, url):
	"""Plays from a url (almost anything youtube_dl supports)"""
	guild = ctx.message.guild
	async with ctx.typing():
		player = await YTDLSource.from_url(url, loop=client.loop)
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))
		players = player
	await ctx.send('Now playing: {}'.format(player.title))

@client.command()
async def stream(ctx, *, url):
	"""Streams from a url (same as yt, but doesn't predownload)"""
	async with ctx.typing():
		player = await YTDLSource.from_url(url, loop=client.loop, stream=True)
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else check_queue(ctx, queues, players))
		players = player
	await ctx.send('Now playing: {}'.format(player.title))

@client.command()
async def volume(ctx, volume: int):
	"""Changes the player's volume"""
	if ctx.voice_client is None:
		return await ctx.send("Not connected to a voice channel.")
	ctx.voice_client.source.volume = volume / 100
	await ctx.send("Changed volume to {}%".format(volume))

@client.command()
async def queue(ctx, url):
	guild = ctx.message.guild
	player = await YTDLSource.from_url(url)
	queues.append(player)
	await ctx.send('The song has been entered into the queue.')

@client.command()
async def stop(ctx):
	"""Stops and disconnects the bot from voice"""
	await ctx.voice_client.disconnect()

@client.command()
async def pause(ctx):
	await ctx.voice_client.pause()

@client.command()
async def resume(ctx):
	await ctx.voice_client.resume()

@client.command()
async def skip(ctx):
	ctx.voice_client.stop()
	check_queue(ctx, queues, players)

@queue.before_invoke
@yt.before_invoke
async def ensure_voice(ctx):
	if ctx.voice_client is None:
		if ctx.author.voice:
			await ctx.author.voice.channel.connect()
		else:
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")
			
client.loop.create_task(change_status())
client.loop.create_task(update_logs())
client.run(TOKEN)