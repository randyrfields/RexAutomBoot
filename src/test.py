
if __name__ == "__main__":
    # hex_string = "48656c6c6f20576f726c64"  # "Hello World" in hex
    hex_string = "0102030405060708090010"  # "Hello World" in hex
    byte_object = bytes.fromhex(hex_string)
    print("obj=", byte_object)

