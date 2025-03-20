import sys
import traceback
from mcp.server.fastmcp import FastMCP
import httpx
import json
import typing as t

# Print startup message to stderr for debugging
print("Starting LMStudio bridge server...", file=sys.stderr)

try:
    # LMStudio API configuration
    LM_STUDIO_API_URL = "http://localhost:1234/v1"
    USER_AGENT = "claude-lmstudio-bridge/1.0"

    print("Initializing FastMCP server...", file=sys.stderr)
    # Initialize FastMCP server
    mcp = FastMCP("lmstudio-bridge")

    class LMStudioError(Exception):
        """Custom exception for LMStudio API errors"""
        pass

    async def make_lmstudio_request(endpoint: str, payload: dict, timeout: float = 60.0) -> dict:
        """Make a request to the LMStudio API with proper error handling."""
        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json"
        }
        
        url = f"{LM_STUDIO_API_URL}/{endpoint}"
        
        try:
            print(f"Making request to {url}...", file=sys.stderr)
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=headers, 
                    timeout=timeout
                )
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors with detailed error message
            error_message = f"HTTP error: {e.response.status_code}"
            try:
                error_json = e.response.json()
                if "error" in error_json:
                    error_message = f"{error_message} - {error_json['error']['message']}"
            except Exception:
                pass
            print(f"HTTP Error: {error_message}", file=sys.stderr)
            raise LMStudioError(error_message)
        except httpx.RequestError as e:
            # Handle request errors (connection issues, timeouts)
            print(f"Request Error: {str(e)}", file=sys.stderr)
            raise LMStudioError(f"Request error: {str(e)}")
        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected Error in request: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise LMStudioError(f"Unexpected error: {str(e)}")

    @mcp.tool()
    async def list_lmstudio_models() -> str:
        """List available LLM models in LM Studio.
        
        Returns:
            A formatted list of available models with their details.
        """
        print("list_lmstudio_models function called", file=sys.stderr)
        try:
            models_response = await make_lmstudio_request("models", {}, timeout=10.0)
            
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
        except LMStudioError as e:
            return f"Error listing models: {str(e)}"
        except Exception as e:
            print(f"Unexpected error in list_lmstudio_models: {str(e)}", file=sys.stderr)
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
        print("generate_text function called", file=sys.stderr)
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
            
            # Make request to LM Studio API
            response = await make_lmstudio_request("completions", payload)
            
            # Extract and return the generated text
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0].get("text", "")
            
            return "No response generated."
        except LMStudioError as e:
            return f"Error generating text: {str(e)}"
        except Exception as e:
            print(f"Unexpected error in generate_text: {str(e)}", file=sys.stderr)
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
            model_id: ID of the model to use (leave empty for default model)
            max_tokens: Maximum number of tokens in the response (default: 1000)
            temperature: Randomness of the output (0-1, default: 0.7)
        
        Returns:
            The generated text from the local LLM
        """
        print("chat_completion function called", file=sys.stderr)
        try:
            # Parse messages JSON
            try:
                parsed_messages = json.loads(messages)
                if not isinstance(parsed_messages, list):
                    return "Error: messages must be a JSON array of message objects."
            except json.JSONDecodeError:
                return "Error: Invalid JSON format for messages. Expected format: [{\"role\": \"user\", \"content\": \"Hello\"}, ...]"
            
            # Validate inputs
            if not parsed_messages:
                return "Error: At least one message is required."
            
            if max_tokens < 1:
                return "Error: max_tokens must be a positive integer."
            
            if temperature < 0 or temperature > 1:
                return "Error: temperature must be between 0 and 1."
            
            # Prepare payload
            payload = {
                "messages": parsed_messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            # Add model if specified
            if model_id and model_id.strip():
                payload["model"] = model_id.strip()
            
            # Make request to LM Studio API
            response = await make_lmstudio_request("chat/completions", payload)
            
            # Extract and return the generated text
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    return choice["message"]["content"]
            
            return "No response generated."
        except LMStudioError as e:
            return f"Error generating chat completion: {str(e)}"
        except Exception as e:
            print(f"Unexpected error in chat_completion: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return f"Unexpected error: {str(e)}"

    if __name__ == "__main__":
        print("Starting server with stdio transport...", file=sys.stderr)
        # Initialize and run the server
        mcp.run(transport='stdio')
except Exception as e:
    print(f"CRITICAL ERROR: {str(e)}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
