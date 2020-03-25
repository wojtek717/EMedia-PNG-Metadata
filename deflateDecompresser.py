import zlib

# Function that decompress given compressed text with Deflate alghoritm
# https://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations
# http://www.libpng.org/pub/png/spec/1.2/PNG-Compression.html
def decompress_text(compressedText):
    compressedByteArray = bytearray(compressedText)
    # Ignore two first bytes
    compressedByteArray.pop(0)
    compressedByteArray.pop(0)
    # Decompress and provide window size
    byteArray = zlib.decompress(compressedByteArray, -15)
    return byteArray