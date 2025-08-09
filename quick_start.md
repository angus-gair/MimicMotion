# Quick Start Guide for MimicMotion

## Option 1: Use Docker (Recommended)

Since PyTorch installation is taking time, use the Docker approach:

```bash
# Use the fast Docker build
docker-compose -f docker-compose-fast.yaml build
docker-compose -f docker-compose-fast.yaml up
```

## Option 2: Manual Python Setup

If you prefer local installation:

1. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies (this will take time):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install diffusers transformers accelerate opencv-python pillow numpy
pip install omegaconf einops decord onnxruntime-gpu matplotlib av
```

3. **Download models:**
```bash
mkdir -p models/DWPose
wget -O models/DWPose/yolox_l.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx"
wget -O models/DWPose/dw-ll_ucoco_384.onnx "https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx"
wget -O models/MimicMotion_1-1.pth "https://huggingface.co/tencent/MimicMotion/resolve/main/MimicMotion_1-1.pth"
```

4. **Run inference:**
```bash
python inference.py --inference_config configs/test.yaml
```

## Option 3: Use Hugging Face Spaces

Visit: https://huggingface.co/spaces/tencent/MimicMotion

## Notes

- PyTorch with CUDA is ~2GB download
- Models are ~1GB total
- Requires NVIDIA GPU with 8GB+ VRAM
- First run will download additional models automatically