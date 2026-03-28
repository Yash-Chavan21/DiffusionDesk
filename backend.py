import torch
from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline
from PIL import Image
import random
import os
import uuid
import os
from dotenv import load_dotenv

# Load the hidden variables from the .env file
load_dotenv() 

# Fetch the token securely
auth_token = os.getenv("HF_AUTH_TOKEN") # <--- 1. ADD THIS IMPORT

# --- 1. SETUP: Load Models (This runs only once) ---

print("Loading models... This might take a few minutes.")

# Set up the main Stable diffusion pipeline
model_id = "Lykon/dreamshaper-8"

device = "cuda"

# Load the pipeline from the original app
sd_pipe = StableDiffusionPipeline.from_pretrained(
    model_id, 
    torch_dtype=torch.float16,
    use_auth_token=auth_token # <--- 2. CHANGE 'True' TO 'auth_token'
)
sd_pipe = sd_pipe.to(device)

# Load the 4x Upscaler pipeline
upscaler_model_id = "stabilityai/stable-diffusion-x4-upscaler"
upscaler_pipe = StableDiffusionUpscalePipeline.from_pretrained(
    upscaler_model_id,
    revision="fp16",
    torch_dtype=torch.float16
)
upscaler_pipe = upscaler_pipe.to(device)

print("Models loaded successfully.")

# --- 2. GENERATION FUNCTION ---

def generate_image(prompt, neg_prompt, guidance, steps, seed):
    """
    Generates an image using Stable Diffusion and returns it.
    """
    
    # Handle the seed
    if seed == -1:
        seed = random.randint(0, 9999999999)
    generator = torch.Generator(device).manual_seed(seed)
    
    print(f"Generating image with seed: {seed}")
    
    with torch.autocast(device):
        # Generate the image
        image = sd_pipe(
            prompt, 
            negative_prompt=neg_prompt,
            guidance_scale=guidance,  # Replaces hard-coded '8.5'
            num_inference_steps=steps,
            generator=generator
        ).images[0]
        
    return image, seed # Return the image and the seed that was used

# --- 3. UPSCALING FUNCTION ---

def upscale_image(image, prompt):
    """
    Upscales a given PIL image using the upscaler model.
    """
    print("Upscaling image...")
    
    with torch.autocast(device):
        upscaled_image = upscaler_pipe(
            prompt=prompt, # The upscaler also uses the prompt
            image=image
        ).images[0]
        
    return upscaled_image

# --- 4. GALLERY FUNCTION ---

def save_to_gallery(image):
    """
    Saves a PIL image to the /gallery folder with a unique name.
    Returns the updated list of all image paths in the gallery.
    """
    if not os.path.exists("gallery"):
        os.makedirs("gallery")
        
    filename = f"gallery/{uuid.uuid4()}.png"
    image.save(filename)
    
    # Get all images in the gallery
    images = [os.path.join("gallery", f) for f in os.listdir("gallery") if f.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort(key=os.path.getmtime, reverse=True) # Sort by most recent
    
    print(f"Image saved to {filename}. Gallery updated.")
    return images