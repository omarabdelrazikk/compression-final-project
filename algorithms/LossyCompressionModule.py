import numpy as np
from PIL import Image
import io

class LossyCompressionAlgorithm:
    """
    Base class for lossy compression algorithms.
    """
    def compress(self, data, is_image=False):
        raise NotImplementedError("Compress method not implemented.")

    def decompress(self, data, is_image=False):
        raise NotImplementedError("Decompress method not implemented.")


class UniformQuantization(LossyCompressionAlgorithm):
    """
    Uniform Quantization for images and text.
    """
    def __init__(self, levels=16):
        self.levels = levels

    def compress(self, data, is_image=False):
        if is_image:
            arr = np.array(data)
            max_val = arr.max()
            min_val = arr.min()
            step = (max_val - min_val) / (self.levels - 1)
            quantized = np.round((arr - min_val) / step) * step + min_val
            quantized = quantized.astype(arr.dtype)
            return quantized
        else:
            # For text, treat each character's ordinal value
            arr = np.array([ord(c) for c in data])
            max_val = arr.max()
            min_val = arr.min()
            step = (max_val - min_val) / (self.levels - 1)
            quantized = np.round((arr - min_val) / step) * step + min_val
            quantized = quantized.astype(int)
            return quantized

    def decompress(self, quantized, is_image=False):
        if is_image:
            img = Image.fromarray(quantized)
            return img
        else:
            chars = [chr(val) for val in quantized]
            return ''.join(chars)


class ScalarQuantization(LossyCompressionAlgorithm):
    """
    Scalar Quantization for images and text.
    """
    def __init__(self, step=10):
        self.step = step

    def compress(self, data, is_image=False):
        if is_image:
            arr = np.array(data)
            quantized = np.round(arr / self.step) * self.step
            quantized = quantized.astype(arr.dtype)
            return quantized
        else:
            arr = np.array([ord(c) for c in data])
            quantized = np.round(arr / self.step) * self.step
            quantized = quantized.astype(int)
            return quantized

    def decompress(self, quantized, is_image=False):
        if is_image:
            img = Image.fromarray(quantized)
            return img
        else:
            chars = [chr(val) for val in quantized]
            return ''.join(chars)


class VectorQuantization(LossyCompressionAlgorithm):
    """
    Vector Quantization for images and text (simple block averaging).
    """
    def __init__(self, block_size=2):
        self.block_size = block_size

    def compress(self, data, is_image=False):
        if is_image:
            arr = np.array(data)
            h, w = arr.shape[:2]
            quantized = arr.copy()
            for i in range(0, h, self.block_size):
                for j in range(0, w, self.block_size):
                    block = arr[i:i+self.block_size, j:j+self.block_size]
                    avg = int(np.mean(block))
                    quantized[i:i+self.block_size, j:j+self.block_size] = avg
            return quantized
        else:
            arr = np.array([ord(c) for c in data])
            quantized = arr.copy()
            for i in range(0, len(arr), self.block_size):
                block = arr[i:i+self.block_size]
                avg = int(np.mean(block))
                quantized[i:i+self.block_size] = avg
            return quantized

    def decompress(self, quantized, is_image=False):
        if is_image:
            img = Image.fromarray(quantized)
            return img
        else:
            chars = [chr(val) for val in quantized]
            return ''.join(chars)


class LloydMaxQuantization(LossyCompressionAlgorithm):
    """
    Lloyd-Max Quantization for images and text (simple iterative mean).
    """
    def __init__(self, levels=8, iterations=5):
        self.levels = levels
        self.iterations = iterations

    def compress(self, data, is_image=False):
        if is_image:
            arr = np.array(data)
            min_val = arr.min()
            max_val = arr.max()
            thresholds = np.linspace(min_val, max_val, self.levels + 1)
            codebook = (thresholds[:-1] + thresholds[1:]) / 2
            quantized = arr.copy()
            for _ in range(self.iterations):
                for i in range(self.levels):
                    mask = (arr >= thresholds[i]) & (arr < thresholds[i+1])
                    quantized[mask] = codebook[i]
            quantized = quantized.astype(arr.dtype)
            return quantized
        else:
            arr = np.array([ord(c) for c in data])
            min_val = arr.min()
            max_val = arr.max()
            thresholds = np.linspace(min_val, max_val, self.levels + 1)
            codebook = (thresholds[:-1] + thresholds[1:]) / 2
            quantized = arr.copy()
            for _ in range(self.iterations):
                for i in range(self.levels):
                    mask = (arr >= thresholds[i]) & (arr < thresholds[i+1])
                    quantized[mask] = codebook[i]
            quantized = quantized.astype(int)
            return quantized

    def decompress(self, quantized, is_image=False):
        if is_image:
            img = Image.fromarray(quantized)
            return img
        else:
            chars = [chr(val) for val in quantized]
            return ''.join(chars)
