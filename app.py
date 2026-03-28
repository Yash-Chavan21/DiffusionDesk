import gradio as gr
import backend # This imports all the code from backend.py

# --- 1. DEFINE THE UI LAYOUT ---

with gr.Blocks(css="body { background-color: #f4f4f4 }") as app:
    
    gr.Markdown("Stable Diffusion Studio")
    gr.Markdown("Transform your imagination into reality using the power of Stable Diffusion AI. Generate, refine, and upscale stunning high-resolution images in seconds.")


    with gr.Row():
        with gr.Column(scale=1): # Left column for inputs
            gr.Markdown("### 1. Generation Controls")
            
            prompt = gr.Textbox(label="Prompt", placeholder="A cinematic photo of a robot in a field of flowers...")
            neg_prompt = gr.Textbox(label="Negative Prompt", placeholder="blurry, ugly, deformed, text, watermark...")
            
            with gr.Row():
                guidance = gr.Slider(label="Guidance (CFG)", minimum=1, maximum=20, value=8.5)
                steps = gr.Slider(label="Inference Steps", minimum=10, maximum=100, step=1, value=25)
            
            with gr.Row():
                seed = gr.Number(label="Seed", value=-1, precision=0)
                randomize_seed = gr.Button("🎲 Randomize")
            
            generate_button = gr.Button("Generate Image", variant="primary")

        with gr.Column(scale=1): # Right column for outputs
            gr.Markdown("### 2. Results")
            
            output_image = gr.Image(label="Generated Image", type="pil")
            used_seed = gr.Textbox(label="Used Seed", interactive=False)
            
            gr.Markdown("### 3. Post-processing")
            
            with gr.Accordion("Upscale Image (4x)", open=False):
                upscaled_image = gr.Image(label="Upscaled Image", type="pil")
                upscale_button = gr.Button("Upscale This Image", variant="secondary")
            
            save_button = gr.Button("Save to Gallery")
            
            help_button = gr.Button("ℹ️ What do these buttons do?", size="sm", variant="secondary")
            help_output = gr.Markdown("")

    gr.Markdown("--- \n ### 🖼️ Your Gallery")
    gallery = gr.Gallery(label="Saved Images", columns=6, object_fit="contain", height="auto")

    # --- 2. CONNECT UI TO BACKEND FUNCTIONS ---

    # Helper function to randomize seed
    def get_random_seed():
        return -1

    # Help Function
    def show_button_help():
        return "✨ **Upscale This Image:** Runs the generated image through a specialized AI to make its resolution 4x larger, making it extremely sharp and detailed. \n\n 💾 **Save to Gallery:** Permanently saves the image to your local 'gallery' folder so it is not lost when you generate a new one, and adds it to the grid below."

    # Button clicks
    generate_button.click(
        fn=backend.generate_image,
        inputs=[prompt, neg_prompt, guidance, steps, seed],
        outputs=[output_image, used_seed]
    )
    
    randomize_seed.click(
        fn=get_random_seed,
        inputs=[],
        outputs=[seed]
    )
    
    upscale_button.click(
        fn=backend.upscale_image,
        inputs=[output_image, prompt], # Pass original image and prompt
        outputs=[upscaled_image]
    )
    
    save_button.click(
        fn=backend.save_to_gallery,
        inputs=[output_image],
        outputs=[gallery]
    )
    
    help_button.click(
        fn=show_button_help,
        inputs=[],
        outputs=[help_output]
    )
    
    # Load initial gallery on app start
    app.load(
        fn=lambda: [os.path.join("gallery", f) for f in os.listdir("gallery") if f.endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists("gallery") else [],
        inputs=[],
        outputs=[gallery]
    )

# --- 3. LAUNCH THE APP ---

print("Launching Gradio app...")
app.launch(share=True) # share=True gives you a public link