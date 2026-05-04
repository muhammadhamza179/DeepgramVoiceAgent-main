"""Function call dispatching and request handling.

Routes function calls from the Deepgram agent to pharmacy operations,
handles barge-in detection, and sends results back to the agent.
"""

import json

from .pharmacy import FUNCTION_MAP


async def handle_barge_in(decoded, twilio_ws, streamsid):
    """Handle user interruption (barge-in) detection.
    
    When the user starts speaking, clear the audio stream to interrupt
    the agent's current response.
    
    Args:
        decoded: Decoded message from Deepgram.
        twilio_ws: WebSocket connection to Twilio.
        streamsid: Twilio stream ID for targeting the media clear.
    """
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {
            "event": "clear",
            "streamSid": streamsid
        }
        await twilio_ws.send(json.dumps(clear_message))


def execute_function_call(func_name, arguments):
    """Execute a pharmacy function call.
    
    Routes function calls to the appropriate handler in FUNCTION_MAP.
    
    Args:
        func_name: Name of the function to call (e.g., 'get_drug_info').
        arguments: Dictionary of arguments to pass to the function.
        
    Returns:
        Function result or error dictionary.
    """
    if func_name in FUNCTION_MAP:
        result = FUNCTION_MAP[func_name](**arguments)
        print(f"Function call result: {result}")
        return result
    else:
        result = {"error": f"Unknown function: {func_name}"}
        print(result)
        return result


def create_function_call_response(func_id, func_name, result):
    """Create a function call response message for Deepgram.
    
    Formats the function result into the expected message format for
    sending back to the Deepgram agent.
    
    Args:
        func_id: Unique ID of the function call from Deepgram.
        func_name: Name of the function that was called.
        result: Result data from the function.
        
    Returns:
        Formatted function call response dictionary.
    """
    return {
        "type": "FunctionCallResponse",
        "id": func_id,
        "name": func_name,
        "content": json.dumps(result)
    }


async def handle_function_call_request(decoded, sts_ws):
    """Handle incoming function call requests from Deepgram.
    
    Processes function calls requested by the Deepgram agent, executes
    them, and sends results back to the agent.
    
    Args:
        decoded: Decoded function call request from Deepgram.
        sts_ws: WebSocket connection to Deepgram agent.
    """
    try:
        for function_call in decoded["functions"]:
            func_name = function_call["name"]
            func_id = function_call["id"]
            arguments = json.loads(function_call["arguments"])

            print(f"Function call: {func_name} (ID: {func_id}), arguments: {arguments}")

            result = execute_function_call(func_name, arguments)

            function_result = create_function_call_response(func_id, func_name, result)
            await sts_ws.send(json.dumps(function_result))
            print(f"Sent function result: {function_result}")

    except Exception as e:
        print(f"Error calling function: {e}")
        error_result = create_function_call_response(
            func_id if "func_id" in locals() else "unknown",
            func_name if "func_name" in locals() else "unknown",
            {"error": f"Function call failed with: {str(e)}"}
        )
        await sts_ws.send(json.dumps(error_result))


async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid):
    """Route text messages from Deepgram to appropriate handlers.
    
    Delegates to barge-in handler and function request handler based
    on the message type.
    
    Args:
        decoded: Decoded message from Deepgram.
        twilio_ws: WebSocket connection to Twilio.
        sts_ws: WebSocket connection to Deepgram agent.
        streamsid: Twilio stream ID.
    """
    await handle_barge_in(decoded, twilio_ws, streamsid)

    if decoded["type"] == "FunctionCallRequest":
        await handle_function_call_request(decoded, sts_ws)
