#!/usr/bin/env python3
import gradio as gr
import os
import torch
import tempfile
import shutil
from pathlib import Path
from omegaconf import OmegaConf
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import MimicMotion functions
try:
    from inference import main as run_inference
except ImportError:
    logger.error("Could not import inference module. Please ensure all dependencies are installed.")
    exit(1)

def process_mimicmotion(ref_image, pose_video, num_frames=16, resolution=576, sample_stride=2, seed=42):
    """
    Process the input image and video to generate motion transfer
    """
    try:
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            image_path = os.path.join(temp_dir, "ref_image.jpg")
            video_path = os.path.join(temp_dir, "pose_video.mp4")
            
            # Save the reference image
            ref_image.save(image_path)
            
            # Save the pose video
            with open(video_path, 'wb') as f:
                f.write(pose_video)
            
            # Create a temporary config
            config = {
                "base_model_path": "stabilityai/stable-video-diffusion-img2vid-xt-1-1",
                "ckpt_path": "models/MimicMotion_1-1.pth",
                "test_case": [{
                    "ref_image_path": image_path,
                    "pose_video_path": video_path,
                    "resolution": resolution,
                    "frames": num_frames,
                    "sample_stride": sample_stride,
                    "seed": seed
                }]
            }
            
            # Save config to temporary file
            config_path = os.path.join(temp_dir, "temp_config.yaml")
            OmegaConf.save(config, config_path)
            
            # Create output directory
            output_dir = os.path.join(temp_dir, "outputs")
            os.makedirs(output_dir, exist_ok=True)
            
            # Run inference
            logger.info(f"Running inference with config: {config}")
            
            # Create args namespace for the main function
            class Args:
                inference_config = config_path
                output_dir = output_dir
                log_level = "INFO"
            
            args = Args()
            
            # Run the inference
            run_inference(args)
            
            # Find the output video
            output_videos = list(Path(output_dir).glob("*.mp4"))
            if output_videos:
                output_path = str(output_videos[0])
                
                # Copy to a persistent location
                result_path = f"outputs/result_{os.path.basename(output_path)}"
                os.makedirs("outputs", exist_ok=True)
                shutil.copy(output_path, result_path)
                
                return result_path
            else:
                return None
                
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise gr.Error(f"Processing failed: {str(e)}")

# Create Gradio interface
title = "MimicMotion - Motion Transfer"
description = """
# MimicMotion: High-Quality Human Motion Video Generation

Upload a reference image and a pose video to transfer the appearance to the motion.

**Note:** 
- First run will download the model (~2GB)
- Processing may take several minutes
- Requires GPU with 8GB+ VRAM
"""

with gr.Blocks(title=title) as demo:
    gr.Markdown(description)
    
    with gr.Row():
        with gr.Column():
            ref_image = gr.Image(label="Reference Image", type="pil")
            pose_video = gr.File(label="Pose Video", file_types=[".mp4", ".avi"])
            
            with gr.Accordion("Advanced Settings", open=False):
                num_frames = gr.Slider(
                    minimum=8, 
                    maximum=72, 
                    value=16, 
                    step=8, 
                    label="Number of Frames"
                )
                resolution = gr.Slider(
                    minimum=256, 
                    maximum=1024, 
                    value=576, 
                    step=64, 
                    label="Resolution"
                )
                sample_stride = gr.Slider(
                    minimum=1, 
                    maximum=4, 
                    value=2, 
                    step=1, 
                    label="Sample Stride"
                )
                seed = gr.Number(
                    value=42, 
                    label="Seed", 
                    precision=0
                )
            
            generate_btn = gr.Button("Generate Motion", variant="primary")
        
        with gr.Column():
            output_video = gr.Video(label="Generated Video")
            status = gr.Textbox(label="Status", interactive=False)
    
    # Example section
    with gr.Row():
        gr.Examples(
            examples=[
                # Add example files if available
            ],
            inputs=[ref_image, pose_video]
        )
    
    def generate_with_status(ref_img, pose_vid, frames, res, stride, s):
        if ref_img is None or pose_vid is None:
            raise gr.Error("Please upload both reference image and pose video")
        
        try:
            status_msg = "Processing... This may take a few minutes."
            yield gr.update(value=status_msg), None
            
            result = process_mimicmotion(ref_img, pose_vid, frames, res, stride, s)
            
            if result:
                status_msg = "Generation complete!"
                yield gr.update(value=status_msg), result
            else:
                raise gr.Error("Failed to generate video")
                
        except Exception as e:
            status_msg = f"Error: {str(e)}"
            yield gr.update(value=status_msg), None
    
    generate_btn.click(
        fn=generate_with_status,
        inputs=[ref_image, pose_video, num_frames, resolution, sample_stride, seed],
        outputs=[status, output_video]
    )

if __name__ == "__main__":
    # Check if models exist
    if not os.path.exists("models/MimicMotion_1-1.pth"):
        print("Warning: Model files not found. Please run the setup script first.")
        print("Models will be downloaded automatically on first run.")
    
    # Launch the app
    demo.launch(
        server_name="0.0.0.0",  # Listen on all network interfaces
        server_port=7860,       # Port number
        share=True,             # Create public URL
        show_error=True
    )