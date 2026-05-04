"""Twilio telephony integration.

Handles WebSocket connections from Twilio, manages inbound audio buffering,
and coordinates message flow between Twilio and the Deepgram agent.
"""

import asyncio
import base64
import json

from .deepgram_handler import sts_connect, sts_sender, sts_receiver, load_config

# Audio buffer size for Twilio (20ms of 8kHz 16-bit audio = 160 samples)
BUFFER_SIZE = 20 * 160


async def twilio_receiver(twilio_ws, audio_queue, streamsid_queue):
    """Receive audio and connection events from Twilio.
    
    Listens for Twilio WebSocket events, buffers inbound audio, and extracts
    the stream ID from the start event. Sends audio chunks to the Deepgram
    agent via the audio queue.
    
    Args:
        twilio_ws: WebSocket connection to Twilio client.
        audio_queue: AsyncIO queue to send audio chunks to Deepgram.
        streamsid_queue: Queue to store the Twilio stream ID.
    """
    inbuffer = bytearray(b"")

    async for message in twilio_ws:
        try:
            data = json.loads(message)
            event = data["event"]

            if event == "start":
                print("get our streamsid")
                start = data["start"]
                streamsid = start["streamSid"]
                streamsid_queue.put_nowait(streamsid)
            elif event == "connected":
                continue
            elif event == "media":
                media = data["media"]
                chunk = base64.b64decode(media["payload"])
                if media["track"] == "inbound":
                    inbuffer.extend(chunk)
            elif event == "stop":
                break

            # Send buffered audio in BUFFER_SIZE chunks to Deepgram
            while len(inbuffer) >= BUFFER_SIZE:
                chunk = inbuffer[:BUFFER_SIZE]
                audio_queue.put_nowait(chunk)
                inbuffer = inbuffer[BUFFER_SIZE:]
        except Exception:
            break


async def twilio_handler(twilio_ws):
    """Main handler for Twilio WebSocket connections.
    
    Orchestrates the connection between Twilio and Deepgram, managing
    concurrent tasks for:
    - Receiving audio from Twilio
    - Sending audio to Deepgram
    - Receiving responses from Deepgram
    
    Args:
        twilio_ws: WebSocket connection from Twilio.
    """
    audio_queue = asyncio.Queue()
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        config_message = load_config()
        await sts_ws.send(json.dumps(config_message))

        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws, audio_queue)),
                asyncio.ensure_future(sts_receiver(sts_ws, twilio_ws, streamsid_queue)),
                asyncio.ensure_future(twilio_receiver(twilio_ws, audio_queue, streamsid_queue)),
            ]
        )

        await twilio_ws.close()
