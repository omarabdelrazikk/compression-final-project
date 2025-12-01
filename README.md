# Compression Application - Updates

## Recent Changes

### 1. Text File Upload Support
- **Lossless Compression**: Users can upload `.txt` files for lossless compression instead of typing text manually
- **Lossy Compression**: Users can now also upload `.txt` files for lossy compression
- The application reads the file content and compresses it using the selected algorithm
- Three input options for lossy compression:
  - Image File upload
  - Text File upload
  - Direct text input (for quick testing)

### 2. Image Compression Support for Lossless Algorithms
- **New Feature**: Lossless compression algorithms (RLE, Huffman, LZW, Golomb) now support image compression
- Images are converted to grayscale and then transformed into a string representation
- Format: `"width,height:pixel1,pixel2,pixel3,..."`
- During decompression, the image is reconstructed from this string representation

## How to Use

### Lossy Compression
1. Toggle the switch to "Lossy Compression" (default)
2. Choose between:
   - **Image File**: Upload an image file (.jpg, .png, .jpeg)
   - **Text File**: Upload a text file (.txt) for lossy compression
   - **Direct Text**: Enter text directly (for quick testing)
3. Select a compression algorithm (Uniform, Scalar, Vector, or Lloyd-Max Quantization)
4. Click the corresponding compress button

### Lossless Compression
1. Toggle the switch to "Lossless Compression"
2. Choose between:
   - **Text File**: Upload a `.txt` file
   - **Image**: Upload an image file (.jpg, .png, .jpeg)
3. Select a compression algorithm (LZW, Golomb, Huffman, or RLE)
4. Click the corresponding compress button

### After Compression
- Click **Decompress** to see the decompressed content
- Click **Calculate Metrics** to view compression statistics:
  - Compression Ratio
  - Efficiency
  - Entropy
  - MSE (Mean Squared Error)
  - RMSE (Root Mean Squared Error)

## Technical Details

### Image to String Conversion (Lossless)
For lossless compression of images:
1. Image is converted to grayscale (8-bit per pixel)
2. Pixel values are flattened and converted to a comma-separated string
3. Header contains image dimensions: `width,height:`
4. During decompression, the string is parsed and reshaped back to the original image

### File Structure
```
compression-final-project/
├── app.py                          # Main Flask application
├── templates/
│   └── index.html                  # Web interface
├── algorithms/
│   ├── LosslessCompression.py      # Lossless algorithms
│   ├── LossyCompressionModule.py   # Lossy algorithms
│   └── CompressionMetricsDemo.py   # Metrics calculation
├── static/                         # Generated decompressed images
└── test_file.txt                   # Sample test file
```

## Running the Application

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

## Notes
- All images are converted to grayscale for consistency
- Lossless compression preserves exact pixel values
- Lossy compression may reduce image quality but achieves higher compression ratios
- Text files must be UTF-8 encoded
