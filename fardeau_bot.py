#!/usr/bin/python3.4

import discord
from discord.ext import commands
import sys,random, asyncio, logging, json, os, markovify

sys.path.insert(0, 'nitw-text-stitch/')
import NITWText


logging.basicConfig(filename="fardeau_bot.log",format='%(asctime)s %(message)s',level=logging.INFO)

TOKEN_FILE = 'config/token'
SERVER_FILE = 'config/servers'
HELP_FILE = 'config/help'

description = '''A NITW Themed Bot that takes a text input, and outputs an image of the text in the NITW font and relevant colour.

Please message Fardeau#5501 with any issues, thoughts and suggestions! https://discord.gg/YCHAHGn
'''

bot = commands.Bot(command_prefix='.', description=description)
bot.remove_command("help")

logging.basicConfig(level=logging.INFO)


def getmarkov(character):

    markovdir = 'nitw-text-stitch/assets/markov/'
    scriptextension = ".txt"
    response = ""
    markovfile = open(markovdir + character.lower() + scriptextension).read()

    reconstituted_model = markovify.Text.from_json(markovfile)
    retries = 3
    lines = 0
    # if character.lower() == "selmers":
    #     while lines < 3 and retries > 0:
    #         generated = reconstituted_model.make_short_sentence(45)
    #         if generated is not None:
    #             lines+=1
    #             response += generated + "\n"
    #         else:
    #             retries -=1
    #
    # else:
    while retries > 0:
        retries -= 1
        response = reconstituted_model.make_short_sentence(140)
        if response is not None:
            break

    return response


def showhelp(ctx):

    response = None

    if valid_channel(ctx):
        with open(HELP_FILE, "r") as help_file:
            response=help_file.read()
    elif valid_server(ctx):
            response = None
    else:
            logging.info("Server " + str(ctx.message.server) + " requested help file!" + "ID: " + str(ctx.message.id))
            response="Hey, sorry this server needs to be permitted to use this bot! Please ask Fardeau for permission! https://discord.gg/YCHAHGn"

    return response

def getchannels(ctx):

    r_server = ctx.message.server
    r_channel = ctx.message.channel
    response = []

    if not (r_channel.is_private):

        with open(SERVER_FILE, "r") as server_file:

            server_data = json.load(server_file)
            for server in server_data["servers"]:
                if server["id"] == r_server.id:
                    for channel in server["channels"]:
                            if channel["permissions"] == "True":
                                buf_channel = r_server.get_channel(channel["id"])
                                response.append(buf_channel.name)
    else:
        response.append("PRIVATE_CHANNEL")

    return response

def setlogging(ctx, requested_channel):

    r_server = ctx.message.server
    r_channel = ctx.message.channel
    user = ctx.message.author
    response = None
    found = False
    user_permissions = r_channel.permissions_for(user)

    if (user_permissions.administrator):

        with open(SERVER_FILE, "r") as server_file:
            server_data = json.load(server_file)


        for server in server_data["servers"]:
            if server["id"] == r_server.id:
                if requested_channel is not None:
                    server["logging"] = requested_channel
                    found = True
                else:
                    server["logging"] = False
                    found = True

        if found:


            with open(SERVER_FILE, "w") as server_file:
                json.dump(server_data, server_file)
            if requested_channel is not None:
                channel_found = r_server.get_channel(requested_channel)
                channel_found_name = channel_found.name
                response = "Logging enabled in channel: " + channel_found_name
                logging.info("Server: " + str(r_server) + " - Logging enabled in channel: " + channel_found_name)
            else:
                response = "Logging disabled"
                logging.info("Server: " + str(r_server) + " - Logging disabled")

        else:
            response = "Could not find channel with id: " + requested_channel

    return response

def setchannels(ctx, requested_channel, enable):

    r_server = ctx.message.server
    r_channel = ctx.message.channel
    user = ctx.message.author
    response = None
    found = False
    user_permissions = r_channel.permissions_for(user)

    if (user_permissions.administrator):

        with open(SERVER_FILE, "r") as server_file:

            server_data = json.load(server_file)

        for server in server_data["servers"]:
            if server["id"] == r_server.id:
                for channel in server["channels"]:
                        if channel["id"] == requested_channel:

                            channel["permissions"] = enable
                            found = True

                if (found == False): # May be a newly added channel: If it exists, enable/disable it!

                    for channel in r_server.channels:

                        if (requested_channel == channel.id):
                            entry = {'id': requested_channel, 'permissions': enable }
                            server["channels"].append(entry)

                            found = True

        if found:

            channel_found = r_server.get_channel(requested_channel)
            channel_found_name = channel_found.name
            with open(SERVER_FILE, "w") as server_file:
                json.dump(server_data, server_file)
            if enable is "True":
                response = "Response enabled in channel: " + channel_found_name
                logging.info("Server: " + str(r_server) + " - Channel enabled: " + channel_found_name)
            else:
                response = "Response disabled in channel: " + channel_found_name
                logging.info("Server: " + str(r_server) + " - Channel disabled: " + channel_found_name)

        else:
            response = "Could not find channel with id: " + requested_channel

    return response


def valid_channel(ctx):

    r_server = ctx.message.server
    r_channel = ctx.message.channel

    if (r_channel.is_private):
        with open(SERVER_FILE, "r") as server_file:

            server_data = json.load(server_file)
            for server in server_data["servers"]:
                if server["id"] == "private":
                    if server["permissions"] == "True":
                        return True
                    else:
                        return False

    else:


        with open(SERVER_FILE, "r") as server_file:

            server_data = json.load(server_file)
            for server in server_data["servers"]:
                logging.debug(r_server.id)
                logging.debug(server["id"])
                if server["id"] == r_server.id:
                    for channel in server["channels"]:
                        if channel["id"] == r_channel.id:
                            if channel["permissions"] == "True":
                                return True
                            else:
                                return False


def valid_server(ctx):

    response = False

    r_server = ctx.message.server

    with open(SERVER_FILE, "r") as server_file:

        server_data = json.load(server_file)
        for server in server_data["servers"]:
            logging.debug(r_server.id)
            logging.debug(server["id"])
            if server["id"] == r_server.id:
                response = True

    return response

def logging_enabled(ctx):

# Check if logging is enabled on this server: if so, write return Channel ID
    response = None

    r_server = ctx.message.server

    with open(SERVER_FILE, "r") as server_file:

        server_data = json.load(server_file)
        for server in server_data["servers"]:
            logging.debug(r_server.id)
            logging.debug(server["id"])
            if server["id"] == r_server.id:
                logging_status = server.get('logging', False)
                if logging_status is not False:
                    response = server["logging"]

    return response


def image_request(message_type, animated, ctx, message):

    channel = ctx.message.channel
    user = ctx.message.author
    user_id = ctx.message.author.id
    user_name = ctx.message.author.name
    message_id = ctx.message.id
    logging_channel = None
    logging_response = None
    max_length = 140
    if (channel.is_private):
        logging.info("Private Message: " + "Incoming Message Request from " + user_name  + "\t User ID: " + user_id  + "\nType: " + message_type + "\tAnimated: " + animated + "\tMessage: " + message)
    else:
        server_id = ctx.message.server.id
        logging.info("Server: " + server_id + "Incoming Message Request from " + user_name  + "\t User ID: " + user_id  + "\nType: " + message_type + "\tAnimated: " + animated + "\tMessage: " + message)
# Here's where I need to check server id against json - see if we have a logging channel set
        logging_channel = logging_enabled(ctx)
        if logging_channel is not None:
        # add logging message and channel to response
            logging_response = "Incoming Message Request from " + user_name  + "\t User ID: " + user_id  + "\nType: " + message_type + "\tAnimated: " + animated + "\tMessage: " + message



    channel = ctx.message.channel
    user = ctx.message.author
    message_id = ctx.message.id

    if not valid_channel(ctx):
        response = {'status': False}
        logging.info("Message Failed - Not in Valid Channel")
    elif len(message) == 0:
        response = {'status': False}
        logging.info("Message Failed - No Message Content")
    elif len(message) > max_length:
        response_message = 'Requested Message is ' + str(len(message)) + ' characters long, max length allowed is ' + str(max_length)
        response = {'status': False, 'error': response_message, 'log_message': logging_response, 'log_channel': logging_channel }
        logging.info("Message Failed - Message too Long")
    else:
        if (channel.is_private):  destination = user
        else: destination = channel
        generated_image = NITWText.create(message, message_type, animated, message_id)
        if generated_image['status'] is True:
            response = {'status': True, 'destination': destination, 'image': generated_image['image'], 'log_message': logging_response, 'log_channel': logging_channel}
            logging.info("Message Created Successfully")
        else:
            if 'error' in generated_image:
                response = {'status': False, 'error': generated_image['error'],'log_message': logging_response, 'log_channel': logging_channel}
                logging.info("Message Failed: " + generated_image['error'])
            else:
                response = {'status': False}
    return response


@bot.event
@asyncio.coroutine
def on_ready():
    logging.info('Logged in as')
    logging.info(bot.user.name)
    logging.info(bot.user.id)
    logging.info('------')
    logging.info('Bot Starting')

@bot.command(pass_context=True)
@asyncio.coroutine
def say(ctx):
    """Input: (character) (text)    Output: Image of (text) in (character colour) using NITW Font"""
    parsed_input = ctx.message.clean_content.replace('.say','').strip()

    character, space, message = parsed_input.partition(' ')
    character = character.lower()
    response = image_request(character, 'no', ctx, message)
    if (response['log_channel']):
        yield from bot.send_message(discord.Object(id=response['log_channel']), response['log_message'])

    if (response['status'] is True):

        yield from bot.send_file(response['destination'] , response['image'])

        # If logging in response, send message to logging channel
    else:
        if 'error' in response:
            yield from bot.say("```Error: " + response['error'] + "```")


@bot.command(pass_context=True)
@asyncio.coroutine
def markov(ctx):
    """Input: (character) (text)    Output: Image of (text) in white using NITW Font"""
    characters = ['gregg', 'mae', 'bea', 'selmers', 'lori', 'germ', 'dad', 'mom', 'angus']
    parsed_input = ctx.message.clean_content.replace('.markov','').strip()

    character, space, message = parsed_input.partition(' ')
    character = character.lower()
    if character in characters:

        message = getmarkov(character)
        if message is not None:
            response = image_request(character, 'no', ctx, message)
            if (response['log_channel']):
                yield from bot.send_message(discord.Object(id=response['log_channel']), response['log_message'])

            if (response['status'] is True):

                yield from bot.send_file(response['destination'] , response['image'])

                # If logging in response, send message to logging channel
            else:
                if 'error' in response:
                    yield from bot.say("```Error: " + response['error'] + "```")
        else:
            yield from bot.say("```Error: Failed to generate a message. Please try again later.```")
    else:
        yield from bot.say("```markov can only be used with Mae, Gregg, Bea, Angus, Lori, Selmers, Germ, Dad and Mom.```")

@bot.command(pass_context=True)
@asyncio.coroutine
def showchannels(ctx):
    """Input: none    Output: Shows channels bot will respond in"""
    response = getchannels(ctx)

    if not response:
        yield from bot.say("```The bot isn't configured to respond in any channels yet!```")
    elif "PRIVATE_CHANNEL" not in response:
        channels = ",".join(response)
        yield from bot.say("```The bot is configured to respond in the following channels: " + channels + "```")

@bot.command(pass_context=True)
@asyncio.coroutine
def enablelogging(ctx):
    """ADMIN ONLY   Input: (channel)    Output: Enables Bot Logging in Channel"""
    requested_channel = ctx.message.clean_content.replace('.enablelogging','').strip()
    response = setlogging(ctx, requested_channel)

    if response:
        yield from bot.say("```" + response + "```")

@bot.command(pass_context=True)
@asyncio.coroutine
def disablelogging(ctx):
    """ADMIN ONLY   Input: (channel)    Output: Enables Bot Logging in Channel"""
    response = setlogging(ctx, None)

    if response:
        yield from bot.say("```" + response + "```")

@bot.command(pass_context=True)
@asyncio.coroutine
def enablechannel(ctx):
    """ADMIN ONLY   Input: (channel)    Output: Enables Bot in Channel"""
    requested_channel = ctx.message.clean_content.replace('.enablechannel','').strip()
    response = setchannels(ctx, requested_channel, "True")

    if response:
        yield from bot.say("```" + response + "```")


@bot.command(pass_context=True)
@asyncio.coroutine
def disablechannel(ctx):
    """ADMIN ONLY   Input: (channel)    Output: disables Bot in Channel"""
    requested_channel = ctx.message.clean_content.replace('.disablechannel','').strip()
    response = setchannels(ctx, requested_channel, "False")

    if response:
        yield from bot.say("```" + response + "```")

@bot.command(pass_context=True)
@asyncio.coroutine
def help(ctx):

    response=showhelp(ctx)
    if response: yield from bot.say("```" + response + "```")


with open(TOKEN_FILE, "r") as token_file:

    token_data = json.load(token_file)
    token = token_data["token"]
    bot.run(token)
