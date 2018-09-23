from telethon import TelegramClient, sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from tqdm import tqdm

def start_client(api_id, api_hash, proxy_args=None):
    client = TelegramClient('session_name', api_id, api_hash,
                            proxy=proxy_args)
    client.start()
    return client

def get_chat(client, chat_name):
    chat = None
    for d in client.get_dialogs():
        if d.name == chat_name:
            chat = d
            break
    if chat is None:
        print("Can't find chat named '{}'".format(chat_name))
    return chat



def get_chat_messages(client, chat):
    if chat.is_channel:
        entity = PeerChannel(chat.id)
    elif chat.is_group:
        entity = PeerChat(chat.id)
    else:
        raise ValueError('Unknown type of group chat!')

    chat_entity = client.get_input_entity(entity)
    history = dict()


    for message in tqdm(client.iter_messages(chat_entity), desc='# messages retrieved', unit=''):
        sender = message.sender
        username = '@{}'.format(sender.username)

        if message.sender.username is None:
            username = sender.first_name
            if sender.last_name is not None:
                username = '{} {}'.format(username, sender.last_name)

        if not username in history:
            history[username] = {'raw_messages': []}
            
        history[username]['raw_messages'].append(message)
        
    return history

def count_messages(history, username):
    info = history[username]['raw_messages']
    n_messages = len(info)
    return n_messages

def process_dates(history):
    import pandas as pd
    for user in history:
        history[user]['dates'] = pd.to_datetime([m.date for m in history[user]['raw_messages']])

def count_messages_after_date(history, date):
    counter = dict.fromkeys(history)
    for user in counter:
        dates = history[user]['dates']
        counter[user] = len(dates[dates > date])
    return counter
