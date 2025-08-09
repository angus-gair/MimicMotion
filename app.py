import gradio as gr
import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import MimicMotion modules
try:
    from inference import MimicMotionInference
    from omegaconf import OmegaConf
except ImportError:
    print("Please install dependencies first: pip install -r requirements.txt")
    sys.exit(1)

class MimicMotionApp:
    def __init__(self):
        self.model = None
        self.config_path = "configs/test.yaml"
        
    def load_model(self):
        if self.model is None:
            print("Loading MimicMotion model...")
            self.model = MimicMotionInference(self.config_path)
            print("Model loaded successfully!")
            
    def process_video(self, input_image, input_video, num_frames=16, resolution=576, seed=42):
        try:
            self.load_model()
            
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_img:
                input_image.save(tmp_img.name)
                image_path = tmp_img.name
                
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_vid:
                # Write video bytes to file
                tmp_vid.write(input_video.read())
                video_path = tmp_vid.name
            
            # Update config
            config = OmegaConf.load(self.config_path)
            config.inference_config.ref_image_path = image_path
            config.inference_config.pose_video_path = video_path
            config.inference_config.num_frames = num_frames
            config.inference_config.resolution = resolution
            config.inference_config.seed = seed
            
            # Run inference
            output_path = self.model.run(config)
            
            # Cleanup temp files
            os.unlink(image_path)
            os.unlink(video_path)
            
            return output_path
            
        except Exception as e:
            return f"Error: {str(e)}"

# Create the Gradio interface
app = MimicMotionApp()

def gradio_interface(input_image, input_video, num_frames, resolution, seed):
    if input_image is None or input_video is None:
        return "Please upload both an image and a video"
    
    result = app.process_video(input_image, input_video, num_frames, resolution, seed)
    return result

# Create Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Image(type="pil", label="Reference Image"),
        gr.File(type="binary", label="Pose Video (.mp4)"),
        gr.Slider(minimum=8, maximum=72, value=16, step=8, label="Number of Frames"),
        gr.Slider(minimum=256, maximum=1024, value=576, step=64, label="Resolution"),
        gr.Number(value=42, label="Seed", precision=0)
    ],
    outputs=gr.Video(label="Generated Video"),
    title="MimicMotion: High-Quality Human Motion Video Generation",
    description="Upload a reference image and a pose video to generate a motion video. The model will transfer the appearance from the reference image to follow the poses in the video.",
    examples=[
        # You can add example files here if you have them
    ]
)

if __name__ == "__main__":
    # Launch with public sharing enabled
    iface.launch(
        server_name="0.0.0.0",  # Listen on all interfaces
        server_port=7860,       # Default Gradio port
        share=True              # Create a public URL
    )