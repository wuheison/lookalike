#!/usr/bin/env python3
"""
Lookalike - Celebrity Face Recognition App
A Flask web application that identifies which celebrity a person looks most like.
"""

import os
import json
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import face_recognition
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Global variables to store celebrity embeddings
celebrity_database = {}
processing_status = {"is_processing": False, "message": ""}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file is allowed."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_actor_image(actor_path: Path) -> Optional[Path]:
    """
    Find the representative image for an actor following the specified search order:
    1. Check for folder.jpg in the actor's main folder
    2. If not found, recursively search for *-poster.jpg files
    
    Returns the path to the image file or None if not found.
    """
    # Primary search: folder.jpg in actor's main folder
    folder_jpg = actor_path / "folder.jpg"
    if folder_jpg.exists() and folder_jpg.is_file():
        logger.info(f"Found folder.jpg for {actor_path.name}")
        return folder_jpg
    
    # Secondary search: *-poster.jpg in subfolders
    for root, dirs, files in os.walk(actor_path):
        for file in files:
            if file.endswith('-poster.jpg'):
                poster_path = Path(root) / file
                logger.info(f"Found poster file {file} for {actor_path.name}")
                return poster_path
    
    logger.warning(f"No suitable image found for actor: {actor_path.name}")
    return None

def extract_face_embedding(image_path: Path) -> Optional[np.ndarray]:
    """
    Extract face embedding from an image file.
    Returns the embedding array or None if no face is found.
    """
    try:
        # Load image
        image = face_recognition.load_image_file(str(image_path))
        
        # Find face encodings
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) > 0:
            # Return the first face encoding found
            return face_encodings[0]
        else:
            logger.warning(f"No face found in image: {image_path}")
            return None
            
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        return None

def process_celebrity_directory(directory_path: str) -> Dict[str, str]:
    """
    Process the celebrity directory and build the face embeddings database.
    Returns a status dictionary with success/error information.
    """
    global celebrity_database, processing_status
    
    try:
        processing_status["is_processing"] = True
        processing_status["message"] = "Starting directory processing..."
        
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            return {"success": False, "error": "Directory does not exist"}
        
        if not directory_path.is_dir():
            return {"success": False, "error": "Path is not a directory"}
        
        celebrity_database.clear()
        processed_count = 0
        skipped_count = 0
        
        # Iterate through actor directories
        for actor_folder in directory_path.iterdir():
            if not actor_folder.is_dir():
                continue
                
            actor_name = actor_folder.name
            processing_status["message"] = f"Processing {actor_name}..."
            
            # Find the representative image for this actor
            image_path = find_actor_image(actor_folder)
            
            if image_path is None:
                logger.warning(f"No image found for actor: {actor_name}")
                skipped_count += 1
                continue
            
            # Extract face embedding
            embedding = extract_face_embedding(image_path)
            
            if embedding is not None:
                celebrity_database[actor_name] = {
                    "embedding": embedding,
                    "image_path": str(image_path)
                }
                processed_count += 1
                logger.info(f"Successfully processed {actor_name}")
            else:
                logger.warning(f"Failed to extract face embedding for {actor_name}")
                skipped_count += 1
        
        processing_status["is_processing"] = False
        processing_status["message"] = f"Processing complete! {processed_count} celebrities processed, {skipped_count} skipped."
        
        return {
            "success": True, 
            "processed_count": processed_count,
            "skipped_count": skipped_count,
            "total_celebrities": len(celebrity_database)
        }
        
    except Exception as e:
        processing_status["is_processing"] = False
        processing_status["message"] = f"Error: {str(e)}"
        logger.error(f"Error processing directory: {str(e)}")
        logger.error(traceback.format_exc())
        return {"success": False, "error": str(e)}

def find_celebrity_matches(target_image_path: str, top_k: int = 10) -> List[Dict]:
    """
    Find the top K celebrity matches for a target image.
    Returns a list of dictionaries with celebrity info and similarity scores.
    """
    if not celebrity_database:
        raise ValueError("Celebrity database is empty. Please process a directory first.")
    
    # Extract face embedding from target image
    target_embedding = extract_face_embedding(Path(target_image_path))
    
    if target_embedding is None:
        raise ValueError("No face found in the uploaded image.")
    
    # Calculate distances to all celebrities
    similarities = []
    
    for celebrity_name, celebrity_data in celebrity_database.items():
        celebrity_embedding = celebrity_data["embedding"]
        
        # Calculate Euclidean distance (lower = more similar)
        distance = np.linalg.norm(target_embedding - celebrity_embedding)
        
        similarities.append({
            "name": celebrity_name,
            "distance": float(distance),
            "similarity_score": max(0, 100 - (distance * 100)),  # Convert to percentage
            "image_path": celebrity_data["image_path"]
        })
    
    # Sort by distance (ascending) and return top K
    similarities.sort(key=lambda x: x["distance"])
    return similarities[:top_k]

# Routes
@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')

@app.route('/api/process_directory', methods=['POST'])
def api_process_directory():
    """API endpoint to process celebrity directory."""
    try:
        data = request.get_json()
        
        if not data or 'directory_path' not in data:
            return jsonify({"success": False, "error": "Directory path is required"}), 400
        
        directory_path = data['directory_path'].strip()
        
        if not directory_path:
            return jsonify({"success": False, "error": "Directory path cannot be empty"}), 400
        
        result = process_celebrity_directory(directory_path)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in process_directory endpoint: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/processing_status', methods=['GET'])
def api_processing_status():
    """Get the current processing status."""
    return jsonify(processing_status)

@app.route('/api/recognize_face', methods=['POST'])
def api_recognize_face():
    """API endpoint to recognize a face in an uploaded image."""
    try:
        if 'photo' not in request.files:
            return jsonify({"success": False, "error": "No photo uploaded"}), 400
        
        file = request.files['photo']
        
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Find celebrity matches
            matches = find_celebrity_matches(filepath, top_k=10)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                "success": True,
                "matches": matches
            })
            
        except ValueError as e:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"success": False, "error": str(e)}), 400
        
    except Exception as e:
        logger.error(f"Error in recognize_face endpoint: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/database_status', methods=['GET'])
def api_database_status():
    """Get the current celebrity database status."""
    return jsonify({
        "is_loaded": len(celebrity_database) > 0,
        "celebrity_count": len(celebrity_database),
        "celebrities": list(celebrity_database.keys()) if celebrity_database else []
    })

@app.route('/celebrity_image/<path:filename>')
def celebrity_image(filename):
    """Serve celebrity images."""
    try:
        # Security check - ensure the path exists in our database
        image_found = False
        for celebrity_data in celebrity_database.values():
            if celebrity_data["image_path"].endswith(filename):
                image_found = True
                break
        
        if not image_found:
            return "Image not found", 404
        
        # Find the full path
        for celebrity_data in celebrity_database.values():
            if celebrity_data["image_path"].endswith(filename):
                full_path = Path(celebrity_data["image_path"])
                return send_from_directory(str(full_path.parent), full_path.name)
        
        return "Image not found", 404
        
    except Exception as e:
        logger.error(f"Error serving celebrity image: {str(e)}")
        return "Error serving image", 500

if __name__ == '__main__':
    print("🎭 Starting Lookalike Celebrity Face Recognition App...")
    print("📍 Open your browser and go to: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5001)
