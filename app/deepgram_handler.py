"""Deepgram agent connection and message handling.

Handles WebSocket connections to the Deepgram agent, configuration management,
and bidirectional message flow between the agent and Twilio.
"""

import asyncio
import base64
import json
import websockets
import os
from dotenv import load_dotenv

from .function_dispatcher import handle_text_message

load_dotenv()


def sts_connect():
    """Create a WebSocket connection to Deepgram's agent service.
    
    Returns:
        WebSocket context manager for the Deepgram agent connection.
        
    Raises:
        Exception: If DEEPGRAM_API_KEY environment variable is not set.
    """
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise Exception("DEEPGRAM_API_KEY not found")

    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        subprotocols=["token", api_key]
    )
    return sts_ws


def load_config():
    """Load Deepgram agent configuration from config.json.
    
    Returns:
        Dictionary containing the agent configuration.
    """
    with open("config.json", "r") as f:
        return json.load(f)


async def sts_sender(sts_ws, audio_queue):
    """Send audio chunks from Twilio to Deepgram.
    
    Continuously retrieves audio chunks from the queue and sends them
    to the Deepgram agent over the WebSocket.
    
    Args:
        sts_ws: WebSocket connection to Deepgram agent.
        audio_queue: AsyncIO queue containing audio chunks from Twilio.
    """
    print("sts_sender started")
    while True:
        chunk = await audio_queue.get()
        await sts_ws.send(chunk)


async def sts_receiver(sts_ws, twilio_ws, streamsid_queue):
    """Receive messages from Deepgram and forward audio to Twilio.
    
    Listens for messages from the Deepgram agent. Handles both text messages
    (which are passed to the function handler) and audio responses (which are
    forwarded to Twilio in real-time).
    
    Args:
        sts_ws: WebSocket connection to Deepgram agent.
        twilio_ws: WebSocket connection to Twilio client.
        streamsid_queue: Queue containing the Twilio stream ID.
    """
    print("sts_receiver started")
    streamsid = await streamsid_queue.get()

    async for message in sts_ws:
        if type(message) is str:
            print(message)
            decoded = json.loads(message)
            await handle_text_message(decoded, twilio_ws, sts_ws, streamsid)
            continue

        raw_mulaw = message

        media_message = {
            "event": "media",
            "streamSid": streamsid,
            "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")}
        }

        await twilio_ws.send(json.dumps(media_message))
