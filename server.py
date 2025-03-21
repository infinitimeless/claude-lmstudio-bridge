import sys
import traceback
import os
import json
import logging
from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

# Print startup message
logging.info("Starting LMStudio bridge server...")

try:
    # ===== Configuration =====
    # Load from environment variables with defaults
    LMSTUDIO_HOST = os.getenv("LMSTUDIO_HOST", "127.0.0.1")
    LMSTUDIO_PORT = os.getenv("LMSTUDIO_PORT", "1234")
    LMSTUDIO_API_URL = f"http://{LMSTUDIO_HOST}:{LMSTUDIO_PORT}/v1"
    DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # Set more verbose logging if debug mode is enabled
    if DEBUG:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug(f"Debug mode enabled")

    logging.info(f"Configured LM Studio API URL: {LMSTUDIO_API_URL}")

    # Initialize FastMCP server
    mcp = FastMCP("lmstudio-bridge")

    # ===== Helper Functions =====
    async def call_lmstudio_api(endpoint: str, payload: Dict[str, Any], timeout: float = 60.0) -> Dict[str, Any]:
        """Unified API communication function with better error handling"""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "claude-lmstudio-bridge/1.0"
        }
        
        url = f"{LMSTUDIO_API_URL}/{endpoint}"
        logging.debug(f"Making request to {url}")
        logging.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=timeout
                )
                
                # Better error handling with specific error messages
                if response.status_code != 200:
                    error_message = f"LM Studio API error: {response.status_code}"
                    try:
                        error_json = response.json()
                        if "error" in error_json:
                            if isinstance(error_json["error"], dict) and "message" in error_json["error"]:
                                error_message += f" - {error_json['error']['message']}"
                            else:
                                error_message += f" - {error_json['error']}"
                    except:
                        error_message += f" - {response.text[:100]}"
                    
                    logging.error(f"Error response: {error_message}")
                    return {"error": error_message}
                
                result = response.json()
                logging.debug(f"Response received: {json.dumps(result, indent=2, default=str)[:200]}...")
                return result
        except httpx.RequestError as e:
            logging.error(f"Request error: {str(e)}")
            return {"error": f"Connection error: {str(e)}"}
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}

    def prepare_chat_messages(messages_input: Union[str, List, Dict]) -> List[Dict[str, str]]:
        """Convert various input formats to what LMStudio expects"""
        try:
            # If messages_input is a string
            if isinstance(messages_input, str):
                # Try to parse it as JSON
                try:
                    parsed = json.loads(messages_input)
                    if isinstance(parsed, list):
                        return parsed
                    else:
                        # If it's parsed but not a list, make it a user message
                        return [{"role": "user", "content": messages_input}]
                except json.JSONDecodeError:
                    # If not valid JSON, assume it's a simple message
                    return [{"role": "user", "content": messages_input}]
            
            # If it's a list already
            elif isinstance(messages_input, list):
                return messages_input
            
            # If it's a dict, assume it's a single message
            elif isinstance(messages_input, dict) and "content" in messages_input:
                if "role" not in messages_input:
                    messages_input["role"] = "user"
                return [messages_input]
                
            # If it's some other format, convert to string and make it a user message
            else:
                return [{"role": "user", "content": str(messages_input)}]
        except Exception as e:
            logging.error(f"Error preparing chat messages: {str(e)}")
            # Fallback to simplest format
            return [{"role": "user", "content": str(messages_input)}]

    # ===== MCP Tools =====
    @mcp.tool()
    async def check_lmstudio_connection() -> str:
        """Check if the LM Studio server is running and accessible.
        
        Returns:
            Connection status and model information
        """
        try:
            # Try to get the server status via models endpoint
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{LMSTUDIO_API_URL}/models", timeout=5.0)
                
            if response.status_code == 200:
                models_data = response.json()
                if "data" in models_data and len(models_data["data"]) > 0:
                    active_model = models_data["data"][0]["id"]
                    return f"✅ Connected to LM Studio. Active model: {active_model}"
                else:
                    return "✅ Connected to LM Studio but no models are currently loaded"
            else:
                return f"❌ LM Studio returned an error: {response.status_code}"
        except Exception as e:
            return f"❌ Failed to connect to LM Studio: {str(e)}"

    @mcp.tool()
    async def list_lmstudio_models() -> str:
        """List available LLM models in LM Studio.
        
        Returns:
            A formatted list of available models with their details.
        """
        logging.info("list_lmstudio_models function called")
        try:
            # Use the API helper function
            models_response = await call_lmstudio_api("models", {}, timeout=10.0)
            
            # Check for errors from the API helper
            if "error" in models_response:
                return f"Error listing models: {models_response['error']}"
            
            if not models_response or "data" not in models_response:
                return "No models found or unexpected response format."
            
            models = models_response["data"]
            model_info = []
            
            for model in models:
                model_info.append(f"ID: {model.get('id', 'Unknown')}")
                model_info.append(f"Name: {model.get('name', 'Unknown')}")
                if model.get('description'):
                    model_info.append(f"Description: {model.get('description')}")
                model_info.append("---")
            
            if not model_info:
                return "No models available in LM Studio."
            
            return "\n".join(model_info)
        except Exception as e:
            logging.error(f"Unexpected error in list_lmstudio_models: {str(e)}")
            traceback.print_exc(file=sys.stderr)
            return f"Unexpected error: {str(e)}"

    @mcp.tool()
    async def generate_text(
        prompt: str,
        model_id: str = "",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate text using a local LLM in LM Studio.
        
        Args:
            prompt: The text prompt to send to the model
            model_id: ID of the model to use (leave empty for default model)
            max_tokens: Maximum number of tokens in the response (default: 1000)
            temperature: Randomness of the output (0-1, default: 0.7)
        
        Returns:
            The generated text from the local LLM
        """
        logging.info("generate_text function called")
        try:
            # Validate inputs
            if not prompt or not prompt.strip():
                return "Error: Prompt cannot be empty."
            
            if max_tokens < 1:
                return "Error: max_tokens must be a positive integer."
            
            if temperature < 0 or temperature > 1:
                return "Error: temperature must be between 0 and 1."
            
            # Prepare payload
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            # Add model if specified
            if model_id and model_id.strip():
                payload["model"] = model_id.strip()
            
            # Make request to LM Studio API using the helper function
            response = await call_lmstudio_api("completions", payload)
            
            # Check for errors from the API helper
            if "error" in response:
                return f"Error generating text: {response['error']}"
            
            # Extract and return the generated text
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0].get("text", "")
            
            return "No response generated."
        except Exception as e:
            logging.error(f"Unexpected error in generate_text: {str(e)}")
            traceback.print_exc(file=sys.stderr)
            return f"Unexpected error: {str(e)}"

    @mcp.tool()
    async def chat_completion(
        messages: str,
        model_id: str = "",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate a chat completion using a local LLM in LM Studio.
        
        Args:
            messages: JSON string of messages in the format [{"role": "user", "content": "Hello"}, ...]
              or a simple text string which will be treated as a user message
            model_id: ID of the model to use (leave empty for default model)
            max_tokens: Maximum number of tokens in the response (default: 1000)
            temperature: Randomness of the output (0-1, default: 0.7)
        
        Returns:
            The generated text from the local LLM
        """
        logging.info("chat_completion function called")
        try:
            # Standardize message format using the helper function
            messages_formatted = prepare_chat_messages(messages)
            
            logging.debug(f"Formatted messages: {json.dumps(messages_formatted, indent=2)}")
            
            # Validate inputs
            if not messages_formatted:
                return "Error: At least one message is required."
            
            if max_tokens < 1:
                return "Error: max_tokens must be a positive integer."
            
            if temperature < 0 or temperature > 1:
                return "Error: temperature must be between 0 and 1."
            
            # Prepare payload
            payload = {
                "messages": messages_formatted,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            # Add model if specified
            if model_id and model_id.strip():
                payload["model"] = model_id.strip()
            
            # Make request to LM Studio API using the helper function
            response = await call_lmstudio_api("chat/completions", payload)
            
            # Check for errors from the API helper
            if "error" in response:
                return f"Error generating chat completion: {response['error']}"
            
            # Extract and return the generated text
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
            
            return "No response generated."
        except Exception as e:
            logging.error(f"Unexpected error in chat_completion: {str(e)}")
            traceback.print_exc(file=sys.stderr)
            return f"Unexpected error: {str(e)}"

    if __name__ == "__main__":
        logging.info("Starting server with stdio transport...")
        # Initialize and run the server
        mcp.run(transport='stdio')
except Exception as e:
    logging.critical(f"CRITICAL ERROR: {str(e)}")
    logging.critical("Traceback:")
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
