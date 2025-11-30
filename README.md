# 🗜️ Compression Application

A comprehensive web-based compression tool that implements both **lossy** and **lossless** compression algorithms with real-time metrics calculation and visualization.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 📋 Table of Contents

- [Features](#features)
- [Algorithms Implemented](#algorithms-implemented)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Metrics](#metrics)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Dual Compression Modes**: Switch between Lossy and Lossless compression
- **Multiple Algorithms**: 8 different compression algorithms to choose from
- **Image & Text Support**: Compress both images (.jpg, .png, .jpeg) and text data
- **Real-time Decompression**: Instantly decompress and view results
- **Performance Metrics**: Calculate compression ratio, efficiency, entropy, MSE, and RMSE
- **Interactive UI**: Clean, responsive Bootstrap interface with dynamic form switching
- **Visual Results**: Display decompressed images directly in the browser

## 🔧 Algorithms Implemented

### Lossy Compression (Images & Text)
- **Uniform Quantization** - Divides data into uniform levels
- **Scalar Quantization** - Quantizes individual values
- **Vector Quantization** - Block-based averaging
- **Lloyd-Max Quantization** - Iterative optimization

### Lossless Compression (Text)
- **LZW (Lempel-Ziv-Welch)** - Dictionary-based compression
- **Golomb Coding** - Optimal for geometric distributions
- **Huffman Coding** - Variable-length prefix codes
- **RLE (Run-Length Encoding)** - Encodes consecutive repeating values

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/compression-app.git
cd compression-app
```

2. **Create a virtual environment**
```bash
python -m venv .venv
```

3. **Activate the virtual environment**

Windows:
```bash
.venv\Scripts\activate
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
cd app
flask run
```

6. **Open your browser**
Navigate to `http://127.0.0.1:5000`

## 📖 Usage

### Compressing Data

1. **Select Compression Mode**
   - Toggle the switch to choose between Lossy or Lossless compression

2. **Choose Input Type** (Lossy only)
   - Select "File" to upload an image
   - Select "Text" to enter text directly

3. **Select Algorithm**
   - Pick from the dropdown menu based on your needs

4. **Submit**
   - Click "Compress File" or "Compress Text"

### Viewing Results

After compression, you can:
- **Decompress**: Click to restore the original data
- **Calculate Metrics**: View detailed compression performance statistics
- **View Decompressed Image**: Images are displayed directly in the browser

## 📁 Project Structure

```
compression-app/
├── app/
│   ├── algorithms/
│   │   ├── LosslessCompression.py      # Lossless algorithms
│   │   ├── LossyCompressionModule.py   # Lossy algorithms
│   │   └── CompressionMetricsDemo.py   # Metrics calculation
│   ├── templates/
│   │   └── index.html                  # Main UI
│   ├── static/                         # Static files (images)
│   └── app.py                          # Flask application
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## 📊 Metrics

The application calculates the following metrics:

| Metric | Description |
|--------|-------------|
| **Compression Ratio** | Original size / Compressed size |
| **Efficiency** | Entropy / Average code length |
| **Entropy** | Measure of data randomness |
| **MSE** | Mean Squared Error (lossy only) |
| **RMSE** | Root Mean Squared Error (lossy only) |

## 🖼️ Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)

### Compression Results
![Results](screenshots/results.png)

### Metrics Display
![Metrics](screenshots/metrics.png)

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Image Processing**: Pillow (PIL)
- **Numerical Computing**: NumPy
- **Algorithms**: Custom implementations of compression algorithms

## 📦 Dependencies

```txt
Flask>=3.0.0
Pillow>=10.0.0
numpy>=1.24.0
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Compression algorithms based on standard implementations
- UI design inspired by modern web applications
- Bootstrap for responsive design

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/compression-app](https://github.com/yourusername/compression-app)

---

⭐ **Star this repo if you find it helpful!**
