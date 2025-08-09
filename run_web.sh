#!/bin/bash

echo "Starting MimicMotion Web Interface..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Gradio if not already installed
pip install gradio

# Check if models exist, if not download them
if [ ! -f "models/MimicMotion_1-1.pth" ]; then
    echo "Downloading models..."
    mkdir -p models/DWPose
    wget -O models/DWPose/yolox_l.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx"
    wget -O models/DWPose/dw-ll_ucoco_384.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx"
    wget -O models/MimicMotion_1-1.pth "https://huggingface.co/tencent/MimicMotion/resolve/main/MimicMotion_1-1.pth"
fi

# Run the web interface
echo "Starting web interface on http://0.0.0.0:7860"
echo "A public URL will be generated for external access..."
python app.py