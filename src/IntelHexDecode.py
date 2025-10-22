class IntelHexDecoder:
    
    def __init__(self):
        pass

    def decode_line(self, line: str):
        """
        Decode one line of Intel HEX format.
        Example line: ":10010000214601360121470136007EFE09D2190140"
        """

        line = line.strip()

        if not line.startswith(':'):
            raise ValueError("Invalid Intel HEX line (missing ':').")

        # Remove the starting colon
        line = line[1:]

        # Convert hex string to bytes
        try:
            raw_bytes = bytes.fromhex(line)
        except ValueError:
            raise ValueError("Invalid hex data in line.")

        # Extract fields
        if len(raw_bytes) < 5:
            raise ValueError("Not enough characters")

        byte_count = raw_bytes[0]
        address = (raw_bytes[1] << 8) | raw_bytes[2]
        record_type = raw_bytes[3]
        data = raw_bytes[4:-1]
        checksum = raw_bytes[-1]

        # Validate byte count
        if byte_count != len(data):
            raise ValueError("Byte count does not match data length.")

        # Validate checksum
        total = sum(raw_bytes) & 0xFF
        if total != 0:
            raise ValueError(f"Checksum error (computed sum = {total:#04x}).")

        elements = {"byte_count": byte_count,
                    "address": address,
                    "record_type": record_type,
                    "data": data,
                    "checksum": checksum,}
        
        return elements

    def sc_format(self, ):


# Example usage:
if __name__ == "__main__":
    decoder = IntelHexDecoder()

    line = ":10010000214601360121470136007EFE09D2190140"
    result = decoder.decode_line(line)

    print(f"Decoded line: {result}")
    # Output example:
    # {
    #   'byte_count': 16,
    #   'address': 0x0100,
    #   'record_type': 0,
    #   'data': b'!F\x016\x01!G\x016\x00~\xfe\t\xd2\x19\x01',
    #   'checksum': 0x40
    # }
