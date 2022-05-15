from telethon import TelegramClient, events, utils
import discord

# The script logs in to an actual Telegram account to monitor events
# in channel & groups. API ID and API Hash are required to login to an
# account. They can be obtained from https://my.telegram.org/
# Currently only configured for text + any type of media

# All required details:
#   - Telegram API ID
#   - Telegram API Hash
#   - Telegram channel ID to monitor
#   - Discord Channel ID to forward
#   - A discord bot token which will forward the messages

api_id = "123456789"     #api id from https://my.telegram.org/. 
api_hash = "123456789abcdefgh98745654321"   #api hash from https://my.telegram.org/

chan_id = -123456789    #telegram group/channel ID to monitor
bin_channel = 123456789    #the discord channel ID where it will be forwarded

disc_token = "123456789abcdefgh98745654321"  #discord bot token. Make sure the bot has sufficient permissions

client = TelegramClient('tg_sess', api_id, api_hash)    #this creates a session file to auto login next time

dis_client = discord.Client()

@dis_client.event
async def on_ready():
    print("Logged in to discord")

async def send_mess_media(mess, media):
    channel = dis_client.get_channel(id=bin_channel)
    if mess == "":
        await channel.send(file=discord.File(media))
        print("Sent Media\n\n")
    else:
        await channel.send(file=discord.File(media), content=mess)
        print("Sent", mess, "and Media\n\n")
    
async def send_mess(mess):
    channel = dis_client.get_channel(id=bin_channel)
    await channel.send(mess)
    print("Sent", mess, "\n\n")
    
    
@client.on(events.NewMessage(incoming=True))
async def py_main(event):
    await dis_client.wait_until_ready()
    if event.chat_id != chan_id:
        return
    
    message = event.message
    media = message.media
    
    if media is not None:
        extension = utils.get_extension(message.media)
        await client.download_media(media, f"download{extension}")
        await send_mess_media(message.message, f"download{extension}")
    else:
        await send_mess(message.message)

client.start()
dis_client.run(disc_token)
