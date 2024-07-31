from telethon import TelegramClient
import time, random
import csv
import os

# from my.telegram.org
api_id = 20479779
api_hash = '54e2616e1eb77e85a8e4bc2a9cbf112e'

proxy = {
    'proxy_type': 'socks5',         # (mandatory) protocol to use
    'addr': '192.168.121.195',      # (mandatory) proxy IP address
    'port': 1088,                   # (mandatory) proxy port number  
}

client = TelegramClient(session='t1', api_id=api_id, api_hash=api_hash, proxy=proxy)


async def get_groups_joined():
    res = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            res.append(dialog)
    return res

async def scrape_group(group_id):
    file_name = f'{group_id}.csv'
    # Check if the file exists, if not, create it with headers

    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["first_name", "last_name", "phone", "user_name", "id"])
            writer.writeheader()
    # Function to add a row to the CSV file
    def add_row(record):
        fieldnames = ["first_name", "last_name", "phone", "user_name", "id"]
        with open(file_name, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(record)

    async for user in client.iter_participants(group_id):
        first_name = user.first_name if user.first_name else ''
        last_name = user.last_name if user.last_name else ''
        phone = user.phone if user.phone else ''
        username = user.username if user.username else ''

        record = {"first_name": first_name, "last_name": last_name,
                   "phone": phone, "user_name": username, "id": user.id}
        

        add_row(record)
        print(record)
        time.sleep(1+random.random())

async def main():
    # Most of your code should go here.
    # You can of course make and use your own async def (do_something).
    # They only need to be async if they need to await things.
    #groups = await get_groups_joined()
    await scrape_group(-1001313195059)
    #await scrape_group(groups[0])

with client:
    client.loop.run_until_complete(main())