import requests
import base64
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the Hugging Face API key from the environment variable
HF_API_KEY = os.getenv("HF_API_KEY")
print("HF_API_KEY: ",HF_API_KEY)
if not HF_API_KEY:
    raise ValueError("Please set your HF_API_KEY in the .env file.")

# Headers used for all Hugging Face API calls
hf_headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Endpoint for text generation (using gpt2 for simplicity)
HF_TEXT_MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"

# Endpoint for image generation (Stable Diffusion)
HF_IMAGE_MODEL_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

def generate_image_prompt(chapter_text):
    """
    Uses Hugging Face's text generation API to generate a creative image prompt
    for a book illustration based on the chapter text (first 500 characters).
    """
    prompt = (
        "Generate a creative image prompt for a book illustration based on the following text:\n"
        f"{chapter_text[:500]}\n"
        "Describe the scene, mood, and colors in one or two sentences."
    )
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_length": 100, "temperature": 0.7}
    }
    response = requests.post(HF_TEXT_MODEL_URL, headers=hf_headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "").strip()
            # Optionally remove the input prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            return generated_text
        else:
            print("Unexpected response format:", result)
            return None
    else:
        print("Hugging Face Text API error:", response.status_code, response.text)
        return None

def generate_image(image_prompt):
    """
    Generates an image using Hugging Face's Stable Diffusion Inference API based on the provided prompt.
    If the model is still loading (status code 503), it waits for the estimated time and retries.
    Measures and prints the total time taken to generate the image.
    Returns the generated image as a base64-encoded PNG string, or None on failure.
    """
    start_time = time.time()
    payload = {"inputs": image_prompt}
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        response = requests.post(HF_IMAGE_MODEL_URL, headers=hf_headers, json=payload)
        if response.status_code == 200:
            image_data = response.content
            base64_image = base64.b64encode(image_data).decode('utf-8')
            total_time = time.time() - start_time
            print(f"Total image generation time: {total_time:.2f} seconds.")
            return base64_image
        elif response.status_code == 503:
            try:
                error_data = response.json()
                wait_time = error_data.get("estimated_time", 60)
            except Exception:
                wait_time = 60
            print(f"Model is loading (503). Waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            attempt += 1
        else:
            print("Hugging Face Image API error:", response.status_code, response.text)
            return None
    print("Exceeded maximum attempts to generate an image.")
    return None

if __name__ == "__main__":
    # For testing, read chapter text from a file if provided; otherwise, use sample text.
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            chapter_text = f.read()
    else:
        chapter_text = (
            "Sample chapter text: In a dimly lit room, a mysterious figure stood gazing "
            "into the distance, with neon lights casting vibrant hues across the walls."
        )
    
    print("Generating image prompt from chapter text using Hugging Face text model...")
    image_prompt = generate_image_prompt(chapter_text)
    if image_prompt:
        print("Generated Image Prompt:", image_prompt)
    
        print("Generating image using Hugging Face Stable Diffusion API...")
        base64_image = generate_image(image_prompt)
        if base64_image:
            with open("output.png", "wb") as f:
                f.write(base64.b64decode(base64_image))
            print("Image saved as output.png")
        else:
            print("Failed to generate image.")
    else:
        print("Failed to generate image prompt.")
