# (c) Tulir Asokan & @AbirHasan2005

import logging

from telethon import TelegramClient, events, Button

from .paralleltransfer import ParallelTransferrer
from .config import (
    session_name,
    api_id,
    api_hash,
    public_url,
    start_message,
    group_chat_message
)
from .util import pack_id, get_file_name

log = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)
transfer = ParallelTransferrer(client)


@client.on(events.NewMessage)
async def handle_message(evt: events.NewMessage.Event) -> None:
    if not evt.is_private:
        await evt.reply(group_chat_message)
        return
    if not evt.file:
        channel_link = "https://t.me/FlixBots"
        group_link = "https://t.me/FlixHelpBot"
        dev_link = "https://t.me/Iggie"
        keyboard = [
            [  
                Button.url("Updates Channel 📢", channel_link), 
                Button.url("Support Bot 👤", group_link)
            ],
            [
                Button.url("Developer 🧕", dev_link)
            ]
        ]
        await evt.reply(start_message,buttons=keyboard,parse_mode='md')
        return
    url = public_url / str(pack_id(evt)) / get_file_name(evt)
    url_button = [
        [
            Button.url("Download Now", f"{url}")
        ],
        [
            Button.url("Join Bots Updates Channel", "https://t.me/FlixBots")
        ]
    ]
    await evt.reply(f"**Link Generated Successfully!!.\n\nFile Name :** `{get_file_name(evt)}`\n\n**Download Link :** `{url}`\n\n__(Tap to Copy!)__",buttons=url_button,parse_mode="md")
    log.info(f"Replied with link for {evt.id} to {evt.from_id} in {evt.chat_id}")
    log.debug(f"Link to {evt.id} in {evt.chat_id}: {url}")
