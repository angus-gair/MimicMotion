#!/bin/bash

echo "Setting up MimicMotion Web Interface..."

# Install Gradio in the existing venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install gradio
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install gradio
fi

# Create outputs directory
mkdir -p outputs

echo "Setup complete!"
echo ""
echo "To run the web interface:"
echo "1. source venv/bin/activate"
echo "2. python web_app.py"
echo ""
echo "The app will:"
echo "- Start a local server at http://localhost:7860"
echo "- Generate a public URL for external access"
echo "- Download models automatically on first run"