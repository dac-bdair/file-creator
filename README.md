 Script Features Random Data Files

    If you don’t specify --bmp, the script creates standard binary files of the requested size filled with random bytes from os.urandom().

BMP Mode

    If you provide --bmp WIDTH HEIGHT, the script ignores the size_in_bytes parameter and instead creates valid 24-bit BMP files of the given dimensions, each filled with random pixel data.

    BMP files will have the .bmp extension (overriding the normal extension).

Zero-Padding

    You can specify a fifth argument to pad the numeric index to a certain width (e.g., 3 for 001, 002, 003, …).

Performance

    Writing random data in chunks prevents issues with very large files.

    
    With this single script, you can generate either:

    Large sets of random binary files for testing, or

    Actual bitmap images (24-bit BMP) that contain random pixels.
