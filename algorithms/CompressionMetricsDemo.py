import numpy as np
from PIL import Image
import sys
import os
from LossyCompressionModule import (
    UniformQuantization,
    ScalarQuantization,
    VectorQuantization,
    LloydMaxQuantization
)
from LosslessCompression import (
    RLECompression,
    HuffmanCompression,
    GolombCompression,
    LZWCompression
)

def compression_ratio(original, compressed):
    if isinstance(original, str):
        before = len(original) * 8
    elif isinstance(original, np.ndarray):
        before = original.size * original.itemsize * 8
    else:
        before = sys.getsizeof(original) * 8
    if isinstance(compressed, str):
        after = len(compressed) * 8
    elif isinstance(compressed, np.ndarray):
        after = compressed.size * compressed.itemsize * 8
    elif isinstance(compressed, list):
        after = len(compressed) * 32  # assuming 32 bits per int
    else:
        after = sys.getsizeof(compressed) * 8
    return before / after if after != 0 else 0

def entropy(data):
    if isinstance(data, str):
        symbols = set(data)
        probs = [data.count(s) / len(data) for s in symbols]
    elif isinstance(data, np.ndarray):
        flat = data.flatten()
        symbols = set(flat)
        probs = [np.count_nonzero(flat == s) / len(flat) for s in symbols]
    else:
        return 0
    return -sum(p * np.log2(p) for p in probs if p > 0)

def average_length(compressed):
    if isinstance(compressed, str):
        return len(compressed)
    elif isinstance(compressed, np.ndarray):
        return compressed.size
    elif isinstance(compressed, list):
        return len(compressed)
    else:
        return 0

def efficiency(original, compressed):
    ent = entropy(original)
    avg_len = average_length(compressed)
    return ent / avg_len if avg_len != 0 else 0

def mse(original, reconstructed):
    if isinstance(original, str):
        orig = np.array([ord(c) for c in original])
        rec = np.array([ord(c) for c in reconstructed])
    elif isinstance(original, np.ndarray):
        orig = original.astype(float)
        rec = reconstructed.astype(float)
    else:
        return 0
    return np.mean((orig - rec) ** 2)

def rmse(original, reconstructed):
    return np.sqrt(mse(original, reconstructed))

def show_image(img):
    if isinstance(img, Image.Image):
        img.show()
    elif isinstance(img, np.ndarray):
        Image.fromarray(img).show()

def main():
    # Example usage for text
    text = "aaabbbcccddeee"
    rle = RLECompression()
    compressed_text = rle.compress(text)
    decompressed_text = rle.decompress(compressed_text)
    print("RLE Compression Ratio:", compression_ratio(text, compressed_text))
    print("RLE Efficiency:", efficiency(text, compressed_text))
    print("RLE MSE:", mse(np.array([ord(c) for c in text]), np.array([ord(c) for c in decompressed_text])))
    print("RLE RMSE:", rmse(np.array([ord(c) for c in text]), np.array([ord(c) for c in decompressed_text])))

    # Example usage for image
    img_path = "example.png"
    if os.path.exists(img_path):
        img = Image.open(img_path).convert('L')
        uq = UniformQuantization(levels=8)
        compressed_img = uq.compress(img, is_image=True)
        decompressed_img = uq.decompress(compressed_img, is_image=True)
        print("Uniform Quantization Compression Ratio:", compression_ratio(np.array(img), compressed_img))
        print("Uniform Quantization Efficiency:", efficiency(np.array(img), compressed_img))
        print("Uniform Quantization MSE:", mse(np.array(img), np.array(decompressed_img)))
        print("Uniform Quantization RMSE:", rmse(np.array(img), np.array(decompressed_img)))
        show_image(decompressed_img)
    else:
        print("Image file 'example.png' not found.")

if __name__ == "__main__":
    main()
