# DiffusionDesk
A lightweight, local Gradio application for high-quality image generation using the Dreamshaper-8 Stable Diffusion model, featuring built-in 4x AI upscaling and a local gallery system.

# DiffusionDesk

A sleek, lightweight web interface built with [Gradio](https://gradio.app/) and [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index) to run Stable Diffusion models locally on your machine. 

This project uses the **Dreamshaper-8** model for high-quality generations and includes a specialized **4x AI Upscaler** to turn standard outputs into incredibly sharp, high-resolution masterpieces.

## ✨ Features
*   **🖼️ High-Quality Generation**: Powered by the `Lykon/dreamshaper-8` Stable Diffusion model.
*   **🔍 4x Built-In Upscaling**: One-click upscaling using `stabilityai/stable-diffusion-x4-upscaler` to enhance image resolution and detail.
*   **⚙️ Advanced Controls**: Fine-tune your prompts with Negative Prompting, CFG Guidance Scale, Inference Steps, and Seed Control.
*   **💾 Local Image Gallery**: Automatically saves your favorite generated images and upscaled results to a local `gallery/` folder, displaying them directly in the UI.
*   **🚀 Modern UI**: Clean, responsive layout for both generating and post-processing images seamlessly.

## 🛠️ Prerequisites
- Python 3.9+
- An NVIDIA GPU with CUDA support (Recommended for fast generation)
- A [Hugging Face Account](https://huggingface.co/) and Access Token.

## 📦 Installation

1. **Clone the repository:**
   ```bash

   
   git clone https://github.com/yourusername/YourProjectName.git
   cd YourProjectName
