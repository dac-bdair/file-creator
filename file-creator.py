#!/usr/bin/env python3

import argparse
import os
import random
import struct

def create_random_file(filename: str, size: int):
    """
    Create a file with 'size' bytes of random data.
    """
    with open(filename, "wb") as f:
        # Write random bytes in reasonable chunks
        chunk_size = 65536  # 64 KB
        bytes_written = 0
        while bytes_written < size:
            to_write = min(chunk_size, size - bytes_written)
            f.write(os.urandom(to_write))
            bytes_written += to_write

def create_bmp_file(filename: str, width: int, height: int):
    """
    Create a 24-bit BMP file of the specified width and height,
    with random pixel data.
    """
    # Each row in a 24-bit BMP is padded to a multiple of 4 bytes in size.
    # For 24-bit, each pixel = 3 bytes (B, G, R).
    # Calculate row size in bytes (with padding to 4-byte boundary).
    row_bytes = (width * 3 + 3) & ~3  # round up to the next multiple of 4
    
    # Total pixel data
    pixel_data_size = row_bytes * height
    
    # BMP file header size is 14 bytes + DIB header (BITMAPINFOHEADER) is 40 bytes = 54 bytes
    header_size = 54
    file_size = header_size + pixel_data_size
    
    # Create the file
    with open(filename, "wb") as f:
        # -- BMP Header (14 bytes) --
        # Signature "BM" (2 bytes)
        f.write(b"BM")
        # File size (4 bytes, little-endian)
        f.write(struct.pack("<I", file_size))
        # Reserved (4 bytes: 2 bytes + 2 bytes)
        f.write(b"\x00\x00\x00\x00")
        # Offset to start of pixel data (4 bytes). It's 54.
        f.write(struct.pack("<I", header_size))
        
        # -- DIB Header: BITMAPINFOHEADER (40 bytes) --
        # DIB header size (4 bytes)
        f.write(struct.pack("<I", 40))
        # Width (4 bytes, little-endian)
        f.write(struct.pack("<i", width))
        # Height (4 bytes, little-endian)
        f.write(struct.pack("<i", height))
        # Planes (2 bytes)
        f.write(struct.pack("<H", 1))
        # Bits per pixel (2 bytes) => 24-bit
        f.write(struct.pack("<H", 24))
        # Compression (4 bytes) => 0 (BI_RGB)
        f.write(struct.pack("<I", 0))
        # Image size (4 bytes) => can be 0 for BI_RGB or the raw data size
        f.write(struct.pack("<I", pixel_data_size))
        # X pixels per meter (4 bytes)
        f.write(struct.pack("<I", 2835))  # ~ 72 DPI
        # Y pixels per meter (4 bytes)
        f.write(struct.pack("<I", 2835))  # ~ 72 DPI
        # Total colors (4 bytes) => 0 = default
        f.write(struct.pack("<I", 0))
        # Important colors (4 bytes) => 0 = all
        f.write(struct.pack("<I", 0))
        
        # -- Pixel Data --
        # Fill each row with random bytes; the row includes padding if needed.
        for _ in range(height):
            row_data = os.urandom(width * 3)  # actual pixel data
            # pad to a multiple of 4 if necessary
            padding = row_bytes - (width * 3)
            row_data += b"\x00" * padding
            f.write(row_data)

def main():
    parser = argparse.ArgumentParser(
        description="Create random files or BMP files with random image data."
    )
    parser.add_argument("prefix", help="Prefix for the output file name.")
    parser.add_argument("extension", help="Extension for the file(s). Ignored if using --bmp (will use .bmp).")
    parser.add_argument("size_in_bytes", type=int, help="File size in bytes (for random files). Ignored if using --bmp.")
    parser.add_argument("count", type=int, help="Number of files to create.")
    parser.add_argument("zero_pad", type=int, nargs="?", default=0,
                        help="Optional zero-padding width for file numbering. Default=0 (no padding).")
    
    parser.add_argument("--bmp", nargs=2, metavar=("WIDTH", "HEIGHT"), type=int,
                        help="Create a BMP file of given WIDTH and HEIGHT (24-bit). This overrides random file mode.")
    
    args = parser.parse_args()
    
    # Determine if we're in BMP mode
    bmp_mode = args.bmp is not None
    
    for i in range(1, args.count + 1):
        # Prepare zero-padded index
        if args.zero_pad > 0:
            index_str = str(i).zfill(args.zero_pad)
        else:
            index_str = str(i)
        
        if bmp_mode:
            # In BMP mode, extension will be .bmp
            filename = f"{args.prefix}_{index_str}.bmp"
            width, height = args.bmp
            print(f"Creating BMP file: {filename} ({width}x{height}) with random pixels")
            create_bmp_file(filename, width, height)
        else:
            # Create raw random data file
            filename = f"{args.prefix}_{index_str}.{args.extension}"
            size = args.size_in_bytes
            print(f"Creating random file: {filename} ({size} bytes)")
            create_random_file(filename, size)
    
    print("Done.")

if __name__ == "__main__":
    main()

     """
    Script Features
    Random Data Files

    If you don’t specify --bmp, the script creates standard binary files of the requested size filled with random bytes from os.urandom().

    ------------------------BMP Mode------------------------

    If you provide --bmp WIDTH HEIGHT, the script ignores the size_in_bytes parameter and instead creates valid 24-bit BMP files of the given dimensions, each filled with random pixel data.

    BMP files will have the .bmp extension (overriding the normal extension).

   ------------------------ Zero-Padding------------------------

    You can specify a fifth argument to pad the numeric index to a certain width (e.g., 3 for 001, 002, 003, …).

    ------------------------Performance------------------------

    Writing random data in chunks prevents issues with very large files.

    With this single script, you can generate either:

    Large sets of random binary files for testing, or

    Actual bitmap images (24-bit BMP) that contain random pixels.
     """