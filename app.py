import os
import sys
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

# Add algorithms folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from LosslessCompression import (
    RLECompression, HuffmanCompression, GolombCompression, LZWCompression
)
from LossyCompressionModule import (
    UniformQuantization, ScalarQuantization, VectorQuantization, LloydMaxQuantization
)
from CompressionMetricsDemo import (
    compression_ratio, efficiency, mse, rmse, entropy
)

app = Flask(__name__)

# Global context to store session data (for demo purposes)
CONTEXT = {
    "original": None,
    "compressed": None,
    "algo_instance": None,
    "is_image": False,
    "algo_name": "",
    "extra_data": {} # For things like Huffman codebook
}

def get_lossy_algo(name):
    if name == "Uniform": return UniformQuantization()
    if name == "Scalar": return ScalarQuantization()
    if name == "Vector": return VectorQuantization()
    if name == "LloydMax": return LloydMaxQuantization()
    return UniformQuantization()

def get_lossless_algo(name):
    if name == "LZW": return LZWCompression()
    if name == "Golomb": return GolombCompression()
    if name == "Huffman": return HuffmanCompression()
    if name == "RLE": return RLECompression()
    return RLECompression()

@app.route("/", methods=["GET", "POST"])
def index():
    global CONTEXT
    result_message = None
    decompressed_content = None
    metrics = None
    is_image = False

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "lossy_file":
            file = request.files.get("file")
            algo_name = request.form.get("algo")
            if file:
                img = Image.open(file).convert('L') # Convert to grayscale for simplicity as per algos
                original_data = np.array(img)
                algo = get_lossy_algo(algo_name)
                compressed_data = algo.compress(original_data, is_image=True)
                
                CONTEXT = {
                    "original": original_data,
                    "compressed": compressed_data,
                    "algo_instance": algo,
                    "is_image": True,
                    "algo_name": algo_name,
                    "extra_data": {}
                }
                result_message = f"Image compressed using {algo_name}. Size: {compressed_data.nbytes} bytes."

        elif action == "lossy_text":
            text = request.form.get("text")
            algo_name = request.form.get("algo")
            algo = get_lossy_algo(algo_name)
            compressed_data = algo.compress(text, is_image=False)
            
            CONTEXT = {
                "original": text,
                "compressed": compressed_data,
                "algo_instance": algo,
                "is_image": False,
                "algo_name": algo_name,
                "extra_data": {}
            }
            result_message = f"Text compressed using {algo_name}."

        elif action == "lossless_text":
            text = request.form.get("text")
            algo_name = request.form.get("algo")
            algo = get_lossless_algo(algo_name)
            
            if algo_name == "Huffman":
                compressed_data, codebook = algo.compress(text)
                extra = {"codebook": codebook}
            else:
                compressed_data = algo.compress(text)
                extra = {}
                
            CONTEXT = {
                "original": text,
                "compressed": compressed_data,
                "algo_instance": algo,
                "is_image": False,
                "algo_name": algo_name,
                "extra_data": extra
            }
            result_message = f"Text compressed using {algo_name}."

        elif action == "decompress":
            if CONTEXT["algo_instance"]:
                algo = CONTEXT["algo_instance"]
                data = CONTEXT["compressed"]
                is_img = CONTEXT["is_image"]
                
                if CONTEXT["algo_name"] == "Huffman":
                    decompressed = algo.decompress(data, CONTEXT["extra_data"]["codebook"])
                else:
                    # Lossy algos need is_image flag
                    if hasattr(algo, 'decompress') and 'is_image' in algo.decompress.__code__.co_varnames:
                         decompressed = algo.decompress(data, is_image=is_img)
                    else:
                         decompressed = algo.decompress(data)
                
                if is_img:
                    # Save for display
                    static_dir = os.path.join(app.root_path, 'static')
                    os.makedirs(static_dir, exist_ok=True)
                    if isinstance(decompressed, Image.Image):
                        decompressed.save(os.path.join(static_dir, 'decompressed.png'))
                    else:
                        # Ensure it's an image object if numpy array
                        Image.fromarray(decompressed).save(os.path.join(static_dir, 'decompressed.png'))
                    decompressed_content = "Image saved to static/decompressed.png"
                    is_image = True
                else:
                    decompressed_content = decompressed
                    is_image = False
                
                result_message = "Decompression successful."

        elif action == "metrics":
            if CONTEXT["original"] is not None:
                orig = CONTEXT["original"]
                comp = CONTEXT["compressed"]
                
                # For metrics, we need decompressed version for MSE/RMSE
                # Re-run decompression
                algo = CONTEXT["algo_instance"]
                is_img = CONTEXT["is_image"]
                
                if CONTEXT["algo_name"] == "Huffman":
                    decomp = algo.decompress(comp, CONTEXT["extra_data"]["codebook"])
                else:
                    if hasattr(algo, 'decompress') and 'is_image' in algo.decompress.__code__.co_varnames:
                         decomp = algo.decompress(comp, is_image=is_img)
                    else:
                         decomp = algo.decompress(comp)

                # Prepare data for metrics (convert to numpy/arrays if needed)
                if is_img:
                    orig_for_metric = np.array(orig)
                    if isinstance(decomp, Image.Image):
                        decomp_for_metric = np.array(decomp)
                    else:
                        decomp_for_metric = np.array(decomp)
                else:
                    orig_for_metric = orig
                    decomp_for_metric = decomp

                metrics = {
                    "Compression Ratio": compression_ratio(orig, comp),
                    "Efficiency": efficiency(orig, comp),
                    "Entropy": entropy(orig)
                }
                
                # MSE/RMSE only make sense if dimensions match or can be compared
                try:
                    metrics["MSE"] = mse(orig_for_metric, decomp_for_metric)
                    metrics["RMSE"] = rmse(orig_for_metric, decomp_for_metric)
                except Exception as e:
                    metrics["MSE"] = "N/A"
                    metrics["RMSE"] = "N/A"
                
                result_message = "Metrics calculated."

    return render_template("index.html", result_message=result_message, decompressed_content=decompressed_content, metrics=metrics, is_image=is_image)