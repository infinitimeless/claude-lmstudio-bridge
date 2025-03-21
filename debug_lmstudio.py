#!/usr/bin/env python3
"""
debug_lmstudio.py - Simple diagnostic tool for LM Studio connectivity

This script tests the connection to LM Studio's API server and helps identify
issues with the connection or API calls.
"""
import sys
import json
import traceback
import argparse
import os
import httpx
import asyncio

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Test connection to LM Studio API")
parser.add_argument("--host", default="127.0.0.1", help="LM Studio API host (default: 127.0.0.1)")
parser.add_argument("--port", default="1234", help="LM Studio API port (default: 1234)")
parser.add_argument("--test-prompt", action="store_true", help="Test with a simple prompt")
parser.add_argument("--test-chat", action="store_true", help="Test with a simple chat message")
parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
args = parser.parse_args()

# Configure API URL
API_URL = f"http://{args.host}:{args.port}/v1"
print(f"Testing connection to LM Studio API at {API_URL}")

async def test_connection():
    """Test basic connectivity to the LM Studio API server"""
    try:
        print("\n=== Testing basic connectivity ===")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/models", timeout=5.0)
            
            if response.status_code == 200:
                print("✅ Connection successful!")
                
                # Check for available models
                data = response.json()
                if "data" in data and isinstance(data["data"], list):
                    if len(data["data"]) > 0:
                        models = [model.get("id", "Unknown") for model in data["data"]]
                        print(f"✅ Found {len(models)} available model(s): {', '.join(models)}")
                    else:
                        print("⚠️ No models are currently loaded in LM Studio")
                else:
                    print("⚠️ Unexpected response format from models endpoint")
                
                if args.verbose:
                    print("\nResponse data:")
                    print(json.dumps(data, indent=2))
                
                return True
            else:
                print(f"❌ Connection failed with status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        if args.verbose:
            traceback.print_exc()
        return False

async def test_completion():
    """Test text completion API with a simple prompt"""
    if not await test_connection():
        return False
    
    print("\n=== Testing text completion API ===")
    try:
        # Simple test prompt
        payload = {
            "prompt": "Hello, my name is",
            "max_tokens": 50,
            "temperature": 0.7,
            "stream": False
        }
        
        print("Sending test prompt: 'Hello, my name is'")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/completions",
                json=payload,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    completion = data["choices"][0].get("text", "")
                    print(f"✅ Received completion response: '{completion[:50]}...'")
                    
                    if args.verbose:
                        print("\nFull response data:")
                        print(json.dumps(data, indent=2))
                    
                    return True
                else:
                    print("❌ No completion text received in the response")
                    print(f"Response: {json.dumps(data, indent=2)}")
                    return False
            else:
                print(f"❌ Completion request failed with status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error during completion test: {str(e)}")
        if args.verbose:
            traceback.print_exc()
        return False

async def test_chat():
    """Test chat completion API with a simple message"""
    if not await test_connection():
        return False
    
    print("\n=== Testing chat completion API ===")
    try:
        # Simple test chat message
        payload = {
            "messages": [
                {"role": "user", "content": "What is the capital of France?"}
            ],
            "max_tokens": 50,
            "temperature": 0.7,
            "stream": False
        }
        
        print("Sending test chat message: 'What is the capital of France?'")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/chat/completions",
                json=payload,
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    if "message" in data["choices"][0] and "content" in data["choices"][0]["message"]:
                        message = data["choices"][0]["message"]["content"]
                        print(f"✅ Received chat response: '{message[:50]}...'")
                        
                        if args.verbose:
                            print("\nFull response data:")
                            print(json.dumps(data, indent=2))
                        
                        return True
                    else:
                        print("❌ No message content received in the response")
                        print(f"Response: {json.dumps(data, indent=2)}")
                        return False
                else:
                    print("❌ No choices received in the response")
                    print(f"Response: {json.dumps(data, indent=2)}")
                    return False
            else:
                print(f"❌ Chat request failed with status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Error during chat test: {str(e)}")
        if args.verbose:
            traceback.print_exc()
        return False

async def run_tests():
    """Run all selected tests"""
    try:
        connection_ok = await test_connection()
        
        if args.test_prompt and connection_ok:
            await test_completion()
        
        if args.test_chat and connection_ok:
            await test_chat()
            
        if not args.test_prompt and not args.test_chat and connection_ok:
            # If no specific tests are requested, but connection is OK,
            # give a helpful message about next steps
            print("\n=== Next Steps ===")
            print("Connection to LM Studio API is working.")
            print("Try these additional tests:")
            print("  python debug_lmstudio.py --test-prompt  # Test text completion")
            print("  python debug_lmstudio.py --test-chat    # Test chat completion")
            print("  python debug_lmstudio.py -v --test-chat # Verbose test output")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        traceback.print_exc()

# Run the tests
if __name__ == "__main__":
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\nTests interrupted.")
        sys.exit(1)
