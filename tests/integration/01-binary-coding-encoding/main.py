import os
import struct


if __name__ == "__main__":
    folder = "output"
    try:
        os.mkdir(folder)
    except OSError:
        pass

    with open(os.path.join(folder, "output_py"), "wb") as file:
        endianness = "<"
        file.write(
            struct.pack(
                endianness + "5c", b"\x96", b"\xFF", b"\xB0", b"\x1A", b"\x23"
            )
        )  # 5 chars
        file.write(struct.pack("3x"))  # padding with size 3
        file.write(struct.pack(endianness + "i", -1))  # signed integer
        file.write(struct.pack(endianness + "I", 2))  # unsigned integer
        file.write(struct.pack(endianness + "3s", b"abc"))  # string with size 3
        file.write(struct.pack("x"))  # padding

    with open(os.path.join(folder, "output_py"), "rb") as file:
        read_bytes = file.read()
        unpacked_bytes = struct.unpack_from("<5c3xiI3sx", read_bytes)

        assert unpacked_bytes[0] == b"\x96"
        assert unpacked_bytes[1] == b"\xFF"
        assert unpacked_bytes[2] == b"\xb0"
        assert unpacked_bytes[3] == b"\x1A"
        assert unpacked_bytes[4] == b"\x23"
        assert unpacked_bytes[5] == -1
        assert unpacked_bytes[6] == 2
        assert unpacked_bytes[7] == b"abc"
