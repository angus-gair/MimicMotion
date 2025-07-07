# Docker Deployment Guide for MimicMotion

This guide helps you deploy MimicMotion locally using Docker.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 1.29+)
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit installed

## Quick Start

1. **Build the Docker image:**
   ```bash
   docker-compose build
   ```

2. **Run the inference:**
   ```bash
   docker-compose up
   ```

   This will automatically:
   - Download all required models (DWPose and MimicMotion)
   - Set up the conda environment
   - Run inference using the test configuration

## Custom Usage

### Running with custom configuration:

1. Place your configuration file in the `configs/` directory
2. Update the command in `docker-compose.yaml`:
   ```yaml
   command: ["conda", "run", "-n", "mimicmotion", "python", "inference.py", "--inference_config", "configs/your_config.yaml"]
   ```

### Interactive shell:

To get an interactive shell in the container:
```bash
docker-compose run --rm mimicmotion bash
```

Then activate the conda environment:
```bash
conda activate mimicmotion
```

### Using pre-downloaded models:

If you've already downloaded the models, place them in the `models/` directory:
```
models/
├── DWPose/
│   ├── dw-ll_ucoco_384.onnx
│   └── yolox_l.onnx
└── MimicMotion_1-1.pth
```

The docker-compose.yaml is configured to mount this directory, so models won't be re-downloaded.

## Volume Mounts

The following directories are mounted:
- `./outputs`: Generated videos will be saved here
- `./configs`: Configuration files
- `./assets`: Input images and videos
- `./models`: Model weights (optional, to avoid re-downloading)

## GPU Memory

If you encounter GPU memory issues:
- The environment variable `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256` is already set
- You can reduce the number of frames in your configuration
- Minimum requirement: 8GB for 16-frame model, 16GB for 72-frame model

## Troubleshooting

1. **NVIDIA Container Toolkit not installed:**
   Follow the official guide: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

2. **Permission denied errors:**
   Make sure your user has permission to access the GPU:
   ```bash
   sudo usermod -aG docker $USER
   ```

3. **Model download issues:**
   The Dockerfile uses the mirror endpoint by default. You can remove or modify the `HF_ENDPOINT` environment variable in docker-compose.yaml if needed.