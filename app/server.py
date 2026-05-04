"""WebSocket server entry point.

Main application server that sets up the WebSocket listener for Twilio
connections and starts the asyncio event loop.
"""

import asyncio
import websockets

from .twilio_handler import twilio_handler


async def main():
    """Start the WebSocket server.
    
    Initializes the WebSocket server on localhost:5000 to accept connections
    from Twilio clients. The server listens indefinitely for incoming connections.
    """
    await websockets.serve(twilio_handler, "localhost", 5000)
    print("Started server.")
    await asyncio.Future()


def run():
    """Run the application.
    
    Entry point for starting the voice agent server.
    """
    asyncio.run(main())


if __name__ == "__main__":
    run()
