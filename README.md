# 🎭 Lookalike - Celebrity Face Recognition App

A powerful local web application that identifies which celebrity you look most like using advanced face recognition technology.

![Lookalike App](https://img.shields.io/badge/Lookalike-Face%20Recognition-purple)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- **🎯 Accurate Face Recognition**: Uses state-of-the-art face recognition algorithms
- **📁 Smart Directory Processing**: Automatically discovers celebrity photos from structured directories
- **🖼️ Intuitive Upload Interface**: Drag-and-drop photo upload with preview
- **📱 Responsive Design**: Beautiful, modern UI that works on desktop and mobile
- **⚡ Fast Processing**: Optimized for quick celebrity matching
- **🔒 Privacy-First**: Runs entirely on your local machine - no data sent to external servers

## 🏗️ Directory Structure Requirements

The app expects your celebrity photo directory to follow this specific structure:

```
celebrity_photos/
├── Actor_Name_1/
│   ├── folder.jpg                    # Primary choice (if exists)
│   ├── Movie_Project_1/
│   │   ├── some-movie-poster.jpg
│   │   └── other-files...
│   └── Movie_Project_2/
│       ├── another-poster.jpg
│       └── other-files...
├── Actor_Name_2/
│   ├── folder.jpg                    # Primary choice (if exists)
│   └── TV_Show_1/
│       ├── tv-show-poster.jpg
│       └── other-files...
└── Actor_Name_3/
    ├── Movie_A/
    │   ├── movie-a-poster.jpg        # Fallback choice
    │   └── other-files...
    └── Movie_B/
        └── movie-b-poster.jpg
```

### Image Selection Logic

For each actor, the app searches for photos in this order:
1. **Primary**: `folder.jpg` directly in the actor's main folder
2. **Fallback**: First `*-poster.jpg` file found in any subfolder

This ensures only one representative photo per celebrity is used.

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **macOS, Windows, or Linux**

### Step 1: Clone or Download

```bash
# If using git
git clone <repository-url>
cd lookalike

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🍎 macOS Installation Notes (M1/M2 Chips)

If you encounter issues installing `dlib` on macOS with Apple Silicon, try these solutions:

#### Option 1: Using Homebrew (Recommended)

```bash
# Install cmake and dlib via Homebrew
brew install cmake
brew install dlib

# Then install Python packages
pip install -r requirements.txt
```

#### Option 2: Using Conda

```bash
# Install conda (if not already installed)
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create conda environment
conda create -n lookalike python=3.9
conda activate lookalike

# Install dlib via conda
conda install -c conda-forge dlib

# Install other requirements
pip install Flask face-recognition opencv-python Pillow numpy Werkzeug
```

#### Option 3: Build from Source

```bash
# Install Xcode command line tools
xcode-select --install

# Install cmake
brew install cmake

# Set environment variables for M1/M2
export CMAKE_OSX_ARCHITECTURES=arm64
export ARCHFLAGS="-arch arm64"

# Install dlib
pip install dlib

# Install other requirements
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

The app will start and display:
```
🎭 Starting Lookalike Celebrity Face Recognition App...
📍 Open your browser and go to: http://localhost:5000
🛑 Press Ctrl+C to stop the server
```

Open your web browser and navigate to `http://localhost:5000`

## 🎯 How to Use

### Step 1: Setup Celebrity Database
1. Enter the full path to your celebrity photos directory
2. Click "Process Directory"
3. Wait for processing to complete (this may take a few minutes depending on the number of celebrities)

### Step 2: Upload Your Photo
1. Drag and drop your photo or click to browse
2. Supported formats: JPG, PNG, GIF, BMP, WebP (max 16MB)
3. Preview your uploaded photo

### Step 3: Find Your Matches
1. Click "Find My Celebrity Twin"
2. View your top 10 celebrity matches with similarity scores
3. Results show celebrity names, photos, and similarity percentages

## 🔧 API Endpoints

The app provides REST API endpoints for programmatic access:

- `POST /api/process_directory` - Process celebrity directory
- `GET /api/processing_status` - Get processing status
- `POST /api/recognize_face` - Upload photo for recognition
- `GET /api/database_status` - Get celebrity database status

## 🛠️ Troubleshooting

### Common Issues

**1. "No face found in the uploaded image"**
- Ensure the photo clearly shows a face
- Try a different photo with better lighting
- Make sure the face is not too small in the image

**2. "Directory does not exist"**
- Double-check the directory path
- Use absolute paths (e.g., `/Users/username/Photos/celebrities`)
- Ensure you have read permissions for the directory

**3. Installation issues on macOS**
- Follow the macOS-specific installation instructions above
- Try using conda instead of pip for dlib installation

**4. Poor recognition results**
- Ensure celebrity photos are high quality and show clear faces
- Use frontal face photos when possible
- Verify the directory structure matches the requirements

### Performance Tips

- **CPU Usage**: Face recognition is CPU-intensive. Close other applications for faster processing
- **Memory**: Processing large celebrity databases requires significant RAM
- **Storage**: Ensure adequate free disk space for temporary files

## 📁 File Structure

```
lookalike/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface
└── uploads/              # Temporary upload folder (created automatically)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for entertainment purposes only. Face recognition results may vary based on photo quality, lighting, and other factors. The app respects privacy by running entirely on your local machine.

## 🙏 Acknowledgments

- Built with [face_recognition](https://github.com/ageitgey/face_recognition) library
- UI designed with [Tailwind CSS](https://tailwindcss.com/)
- Icons from [Font Awesome](https://fontawesome.com/)

---

**Happy face matching! 🎭✨**
