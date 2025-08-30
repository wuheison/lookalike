# 🎭 Lookalike Setup Guide

## Quick Start (Recommended)

### Option 1: Automated Setup
```bash
# Run the comprehensive setup script
./setup_and_test.sh

# Or with testing
./setup_and_test.sh --test
```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install Flask==3.0.0 Werkzeug==3.0.1 python-dotenv==1.0.0
   pip install opencv-python==4.8.1.78 Pillow==10.1.0 numpy==1.25.2
   pip install face-recognition
   pip install pathlib2 --force-reinstall
   ```

3. **Test the setup:**
   ```bash
   python -c "import flask, face_recognition, cv2, PIL, numpy; print('✅ All dependencies work!')"
   ```

## Running the Application

### Method 1: Direct Python
```bash
source venv/bin/activate
python app.py
```

### Method 2: Using the run script
```bash
./run.sh
```

### Method 3: Using setup.py
```bash
source venv/bin/activate
python setup.py
```

## Accessing the Application

Once running, open your browser and go to:
**http://localhost:5000**

## Troubleshooting

### Common Issues on macOS (Apple Silicon)

1. **dlib installation fails:**
   ```bash
   # Install via Homebrew first
   brew install cmake dlib
   # Then install Python package
   pip install face-recognition
   ```

2. **Face recognition not working:**
   - Ensure you have a celebrity photos directory set up
   - Follow the directory structure in README.md
   - Use high-quality photos with clear faces

3. **Port 5000 already in use:**
   - Change the port in app.py (line 308): `app.run(debug=True, host='0.0.0.0', port=5001)`

### Dependencies Status
✅ **Installed and Verified:**
- Flask 3.0.0
- Werkzeug 3.0.1  
- face-recognition 1.3.0
- opencv-python 4.8.1.78
- Pillow 10.1.0
- numpy 1.25.2
- dlib 20.0.0
- python-dotenv 1.0.0
- pathlib2 2.3.7

## System Requirements
- Python 3.8+
- macOS 10.14+ (tested on Apple Silicon)
- 4GB+ RAM recommended
- Internet connection for initial setup

## Next Steps
1. Prepare your celebrity photos directory (see main README.md)
2. Start the application
3. Access the web interface
4. Process your celebrity directory
5. Upload photos to find matches!

---
*Setup completed successfully! 🎭✨*
