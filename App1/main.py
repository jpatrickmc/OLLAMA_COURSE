#!/usr/bin/env python3
"""
Basic Ollama Python Script
This script demonstrates how to interact with Ollama using the Python library.
"""

import ollama


def main():
    """Main function to interact with Ollama."""
    
    # Example 1: Simple chat completion
    # print("=" * 50)
    # print("Example 1: Simple Chat Completion")
    # print("=" * 50)
    
    # response = ollama.chat(
    #     model='llama2',  # Change this to your preferred model
    #     messages=[
    #         {
    #             'role': 'user',
    #             'content': 'Why is the sky blue?',
    #         },
    #     ]
    # )
    
    # print(f"Response: {response['message']['content']}\n")

    
    
    # Example 2: Streaming response
    print("=" * 50)
    print("Example 2: Streaming Response")
    print("=" * 50)
    
    stream = ollama.chat(
        model='llama2',
        messages=[
            {
                'role': 'user',
                'content': 'Why is the sky blue.',
            },
        ],
        stream=True,
    )
    
    print("Response: ", end='', flush=True)
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
    print("\n")
    
    
    # # Example 3: Generate text
    # print("=" * 50)
    # print("Example 3: Text Generation")
    # print("=" * 50)
    
    # response = ollama.generate(
    #     model='llama2',
    #     prompt='Write a haiku about programming.',
    # )
    
    # print(f"Response: {response['response']}\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is installed on your system")
        print("2. Ollama service is running (run 'ollama serve' in another terminal)")
        print("3. You have pulled the model (run 'ollama pull llama2')")

# Made with Bob
