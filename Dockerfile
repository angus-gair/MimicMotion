FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set python3.11 as default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY environment.yaml .

# Install conda (for environment.yaml)
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

ENV PATH="/opt/conda/bin:${PATH}"

# Create conda environment
RUN conda env create -f environment.yaml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "mimicmotion", "/bin/bash", "-c"]

# Copy the rest of the application
COPY . .

# Create models directory
RUN mkdir -p models/DWPose

# Download model weights
RUN wget https://huggingface.co/yzd-v/DWPose/resolve/main/yolox_l.onnx?download=true -O models/DWPose/yolox_l.onnx && \
    wget https://huggingface.co/yzd-v/DWPose/resolve/main/dw-ll_ucoco_384.onnx?download=true -O models/DWPose/dw-ll_ucoco_384.onnx && \
    wget -P models/ https://huggingface.co/tencent/MimicMotion/resolve/main/MimicMotion_1-1.pth

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256

# Create directories for outputs
RUN mkdir -p outputs

# Expose port if needed (for future web interface)
EXPOSE 8000

# Default command
CMD ["conda", "run", "-n", "mimicmotion", "python", "inference.py", "--inference_config", "configs/test.yaml"]