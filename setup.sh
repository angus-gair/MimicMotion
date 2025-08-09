#!/bin/bash

echo "Setting up MimicMotion locally..."

# Create virtual environment
python3 -m venv venv

# Activate and install
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate
pip install opencv-python pillow numpy
pip install omegaconf einops decord
pip install onnxruntime-gpu
pip install matplotlib av

# Create models directory
mkdir -p models/DWPose

# Download models
echo "Downloading models..."
wget -O models/DWPose/yolox_l.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx"
wget -O models/DWPose/dw-ll_ucoco_384.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx"
wget -O models/MimicMotion_1-1.pth "https://huggingface.co/tencent/MimicMotion/resolve/main/MimicMotion_1-1.pth"

echo "Setup complete!"
echo "To run MimicMotion:"
echo "  source venv/bin/activate"
echo "  python inference.py --inference_config configs/test.yaml"