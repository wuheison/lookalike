# Sample Celebrity Directory Structure

This document shows the expected directory structure for your celebrity photos.

## Required Structure

```
celebrity_photos/                    # Your root directory
├── Tom_Hanks/                      # Actor's name (folder name becomes celebrity name)
│   ├── folder.jpg                  # Primary choice - if this exists, it will be used
│   ├── Forrest_Gump/
│   │   ├── forrest-gump-poster.jpg # Fallback choice if no folder.jpg
│   │   └── other-files...
│   └── Cast_Away/
│       ├── cast-away-poster.jpg
│       └── other-files...
├── Emma_Stone/
│   ├── folder.jpg                  # Primary choice
│   ├── La_La_Land/
│   │   ├── la-la-land-poster.jpg
│   │   └── other-files...
│   └── Easy_A/
│       ├── easy-a-poster.jpg
│       └── other-files...
└── Leonardo_DiCaprio/
    ├── Titanic/
    │   ├── titanic-poster.jpg      # Will use this (first *-poster.jpg found)
    │   └── other-files...
    ├── Inception/
    │   ├── inception-poster.jpg    # This won't be used (only first found)
    │   └── other-files...
    └── The_Wolf_of_Wall_Street/
        ├── wolf-poster.jpg
        └── other-files...
```

## Search Logic

For each actor folder, the app searches in this order:

1. **Primary Search**: Look for `folder.jpg` directly in the actor's main folder
   - If found → Use this image and stop searching for this actor
   
2. **Secondary Search**: If no `folder.jpg` found, recursively search all subfolders for files ending with `-poster.jpg`
   - Use the first `*-poster.jpg` file found
   - Stop searching once one is found

## Tips for Best Results

- **High Quality Photos**: Use clear, high-resolution images
- **Front-facing**: Photos should show the face clearly from the front
- **Good Lighting**: Avoid shadows or poor lighting
- **Single Face**: Each photo should contain only one main face
- **Proper Naming**: Use consistent naming for poster files (`name-poster.jpg`)

## Supported Image Formats

- JPG/JPEG
- PNG
- GIF
- BMP
- WebP

## Example Setup

1. Create your main directory: `mkdir ~/celebrity_photos`
2. Create actor folders: `mkdir ~/celebrity_photos/Tom_Hanks`
3. Add either:
   - `~/celebrity_photos/Tom_Hanks/folder.jpg` (preferred)
   - Or `~/celebrity_photos/Tom_Hanks/Some_Movie/movie-poster.jpg` (fallback)

The app will automatically find and use the appropriate image for each celebrity based on this structure.
