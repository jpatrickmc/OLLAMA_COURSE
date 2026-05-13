# Title: Make Llava Describe the Image
#
# Description:
# This script demonstrates "Multimodal" capabilities using Ollama.
# Multimodal means the model can understand more than just text—in this case,
# it can see and describe images.
#
# We use the 'llava' model (Large Language-and-Vision Assistant), which is
# specifically designed for image understanding.
#
# Installation:
# 1. Install the Python library:
#    pip install ollama
#
# 2. Pull the multimodal model (Required!):
#    Run this command in your terminal:
#    ollama pull llava:7b
#
# Note: Ensure you have a file named 'image.jpg' in the same folder as this script.
#
# How to run:
# python describe_image.py

import ollama  # Import the Ollama library
from pathlib import Path


# Resolve the image path relative to this script so execution from any cwd works.
image_path = Path(__file__).with_name('image.jpg')
if not image_path.exists():
    raise FileNotFoundError(f"Expected image at: {image_path}")

# Call the ollama.chat function.
# Unlike text-only models, we pass an extra 'images' list in the message.
response = ollama.chat(
    model='llava:7b',  # We MUST use a vision-capable model like 'llava'. 'llama3' will not work for images.
    messages=[
        {
            'role': 'user',
            'content': 'Describe the image.', # The text prompt asking the model what to do with the image.
            'images': [str(image_path)]       # A list of paths to image files. The model will analyze this file.
        }
    ]
)

# Print the model's textual description of the image.
print(response['message']['content'])
