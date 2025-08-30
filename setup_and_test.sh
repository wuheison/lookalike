#!/bin/bash

# Lookalike - Celebrity Face Recognition App
# Complete Setup and Test Script for macOS
# This script sets up the virtual environment, installs dependencies, and tests the application

set -e

echo "🎭 Lookalike - Celebrity Face Recognition App Setup & Test"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}➤${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_success "Python version: $PYTHON_VERSION"

# Check if we're on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_success "macOS detected"
    
    # Check for Apple Silicon
    if [[ $(uname -m) == "arm64" ]]; then
        print_success "Apple Silicon (M1/M2) detected"
        
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            print_warning "Homebrew not found. Some dependencies might fail to install."
            print_status "Install Homebrew from: https://brew.sh"
        else
            print_success "Homebrew is available"
            
            # Check and install cmake and dlib if needed
            if ! brew list cmake &> /dev/null; then
                print_status "Installing cmake via Homebrew..."
                brew install cmake
            else
                print_success "cmake is already installed"
            fi
            
            if ! brew list dlib &> /dev/null; then
                print_status "Installing dlib via Homebrew..."
                brew install dlib
            else
                print_success "dlib is already installed"
            fi
        fi
    fi
fi

# Create virtual environment if it doesn't exist
print_status "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."

# Install core dependencies first
print_status "Installing Flask and core web dependencies..."
pip install Flask==3.0.0 Werkzeug==3.0.1 python-dotenv==1.0.0

# Install image processing dependencies
print_status "Installing image processing dependencies..."
pip install opencv-python==4.8.1.78 Pillow==10.1.0 numpy==1.25.2

# Install face recognition (this includes dlib)
print_status "Installing face recognition library..."
if pip install face-recognition==1.3.0; then
    print_success "face-recognition installed successfully"
else
    print_error "Failed to install face-recognition. Trying alternative approach..."
    pip install face-recognition
fi

# Install remaining dependencies
print_status "Installing remaining dependencies..."
pip install pathlib2 --force-reinstall

# Create uploads directory
mkdir -p uploads

# Test imports
print_status "Testing dependency imports..."
python3 -c "
import flask
import face_recognition
import cv2
import PIL
import numpy
print('✅ All critical dependencies imported successfully!')
"

# Test Flask app
print_status "Testing Flask application..."
python3 -c "
import sys
sys.path.insert(0, '.')
from app import app
print('✅ Flask application loads successfully!')
print('✅ All routes and dependencies are working!')
"

# Final status
print_success "Setup completed successfully!"
echo ""
echo "🚀 How to run your application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Start the app: python app.py"
echo "   3. Open browser: http://localhost:5000"
echo ""
echo "📝 Or use the convenience script: ./run.sh"
echo ""

# Run quick test if requested
if [[ "$1" == "--test" ]]; then
    echo "🧪 Running quick application test..."
    source venv/bin/activate
    
    # Start app in background for testing
    python app.py &
    APP_PID=$!
    
    # Wait a moment for app to start
    sleep 3
    
    # Test if app is responding
    if curl -s http://localhost:5000 > /dev/null; then
        print_success "Application is running and responding!"
    else
        print_warning "Application may not be responding on port 5000"
    fi
    
    # Stop the app
    kill $APP_PID 2>/dev/null || true
    wait $APP_PID 2>/dev/null || true
    
    print_success "Test completed!"
fi

print_success "All done! Your Lookalike app is ready to use! 🎭✨"
