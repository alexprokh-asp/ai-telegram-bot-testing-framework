# -*- coding: utf-8 -*-
import asyncio
from telethon import TelegramClient, events
import aiohttp
from aiohttp import web
import json

# Telegram credentials (replace with your own)
api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'

# Telegram client
client = TelegramClient('telegram_qa_client', api_id, api_hash)

# n8n webhook URL (where incoming messages are sent - use your own)
#WEBHOOK_URL = 'http://localhost:5678/webhook-test/YOUR_WH'
WEBHOOK_URL = 'http://localhost:5678/webhook/YOUR_WH'

async def send_to_n8n(data):
    """Asynchronous data send to n8n"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=data) as resp:
                print(f"Sent to n8n, status code: {resp.status}")
    except Exception as e:
        print(f"Error sending to n8n: {e}")

@client.on(events.NewMessage)
async def handler(event):
    """Handle incoming Telegram messages"""
    message = event.message.message
    sender = await event.get_sender()
    print(f"New message from {sender.id}: {message}")

    data = {
        'sender': str(sender.id),
        'message': message
    }
    asyncio.create_task(send_to_n8n(data))  # send to n8n

# -------- HTTP server to receive commands from n8n --------
async def handle_send_message(request):
    try:
        body = await request.json()
        recipient = body.get('recipient')
        message = body.get('message')

        if not recipient or not message:
            return web.json_response({'status': 'error', 'error': 'recipient or message missing'}, status=400)

        # Send message through Telethon
        await client.send_message(int(recipient), message)
        print(f"Sent message to {recipient}: {message}")
        return web.json_response({'status': 'ok'})
    except Exception as e:
        print(f"Error in HTTP handler: {e}")
        return web.json_response({'status': 'error', 'error': str(e)}, status=500)

async def start_http_server():
    app = web.Application()
    app.router.add_post('/send_message', handle_send_message)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 5000)  # port 5000, can be changed
    await site.start()
    print("HTTP server started at http://localhost:5000/send_message")

# -------- Main function --------
async def main():
    await client.start()  # on first run, you'll enter the phone number once
    print("Telegram client started. Waiting for messages...")
    
    # Start HTTP server in parallel
    await start_http_server()
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
