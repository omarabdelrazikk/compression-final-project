class CompressionAlgorithm:
    """
    Base class for compression algorithms.
    """
    def compress(self, data):
        raise NotImplementedError("Compress method not implemented.")

    def decompress(self, data):
        raise NotImplementedError("Decompress method not implemented.")


class RLECompression(CompressionAlgorithm):
    """
    Run-Length Encoding (RLE) implementation.
    """
    def compress(self, data):
        if not data:
            return ''
        result = []
        count = 1
        prev = data[0]
        for char in data[1:]:
            if char == prev:
                count += 1
            else:
                result.append(f"{prev}{count}")
                prev = char
                count = 1
        result.append(f"{prev}{count}")
        return ''.join(result)

    def decompress(self, data):
        result = []
        i = 0
        while i < len(data):
            char = data[i]
            i += 1
            count_str = ''
            while i < len(data) and data[i].isdigit():
                count_str += data[i]
                i += 1
            count = int(count_str) if count_str else 1
            result.append(char * count)
        return ''.join(result)


class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

class HuffmanCompression(CompressionAlgorithm):
    """
    Huffman Coding implementation.
    """
    def build_tree(self, freq):
        nodes = [HuffmanNode(symbol=s, freq=f) for s, f in freq.items()]
        while len(nodes) > 1:
            nodes.sort(key=lambda node: node.freq)
            left = nodes.pop(0)
            right = nodes.pop(0)
            parent = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
            nodes.append(parent)
        return nodes[0]

    def build_codes(self, node, prefix='', codebook=None):
        if codebook is None:
            codebook = {}
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        else:
            if node.left:
                self.build_codes(node.left, prefix + '0', codebook)
            if node.right:
                self.build_codes(node.right, prefix + '1', codebook)
        return codebook

    def compress(self, data):
        if not data:
            return '', {}
        freq = {}
        for char in data:
            freq[char] = freq.get(char, 0) + 1
        tree = self.build_tree(freq)
        codebook = self.build_codes(tree)
        encoded = ''.join(codebook[char] for char in data)
        return encoded, codebook

    def decompress(self, encoded, codebook):
        reverse_codebook = {v: k for k, v in codebook.items()}
        result = []
        code = ''
        for bit in encoded:
            code += bit
            if code in reverse_codebook:
                result.append(reverse_codebook[code])
                code = ''
        return ''.join(result)


class GolombCompression(CompressionAlgorithm):
    """
    Golomb Coding implementation (parameter m must be set).
    """
    def __init__(self, m=4):
        self.m = m

    def compress(self, data):
        result = []
        for num in data:
            q = num // self.m
            r = num % self.m
            unary = '1' * q + '0'
            binary = format(r, f'0{self.m.bit_length()-1}b')
            result.append(unary + binary)
        return ' '.join(result)

    def decompress(self, data):
        result = []
        items = data.split()
        for item in items:
            q = 0
            i = 0
            while i < len(item) and item[i] == '1':
                q += 1
                i += 1
            i += 1  # skip '0'
            r_bits = item[i:]
            r = int(r_bits, 2) if r_bits else 0
            num = q * self.m + r
            result.append(num)
        return result


class LZWCompression(CompressionAlgorithm):
    """
    Lempel–Ziv–Welch (LZW) implementation.
    """
    def compress(self, data):
        dictionary = {chr(i): i for i in range(256)}
        result = []
        w = ''
        next_code = 256
        for c in data:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = next_code
                next_code += 1
                w = c
        if w:
            result.append(dictionary[w])
        return result

    def decompress(self, compressed):
        dictionary = {i: chr(i) for i in range(256)}
        result = []
        w = chr(compressed[0])
        result.append(w)
        next_code = 256
        for k in compressed[1:]:
            if k in dictionary:
                entry = dictionary[k]
            elif k == next_code:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.append(entry)
            dictionary[next_code] = w + entry[0]
            next_code += 1
            w = entry
        return ''.join(result)
