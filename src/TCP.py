import socket
import threading
import sys
import time
from   IntelHexDecode import IntelHexDecoder


class TCPEchoDaemon:

    def __init__(self, host, port, scHandle, stat):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None
        self.decoder = IntelHexDecoder()
        self.scHandle = scHandle
        self.station = stat

    def start(self):
        """Start the daemon in a background thread."""
        if self.running:
            print("Server already running.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        print(f"TCP Echo Daemon started on {self.host}:{self.port}")

    def run(self):
        """Main server loop (runs in background thread)."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen(5)
                self.server_socket = s

                while self.running:
                    try:
                        s.settimeout(1.0)
                        conn, addr = s.accept()
                    except socket.timeout:
                        continue

                    print(f"Connection from {addr}")
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

        except Exception as e:
            print(f"Server error: {e}")
            self.running = False

    def receive_line(self, conn, addr):
        line_recv = conn.recv(1024)
        if not line_recv:
           return None
        return line_recv
        
    def handle_client(self, conn, addr):
        """Handle a single client connection."""
        with conn:
            while self.running:
                try:
                    line = self.receive_line(conn, addr)

                    if line != None:
                        linestr = line.decode("ascii")
                        self.station.serial.destination = linestr[0]
                        print("Dest=", self.station.serial.destination)
                        linestr = linestr[1:]
                        decoded = self.decoder.decode_line(linestr)
                        self.station.serial.scprogramstruct = decoded
                        if decoded["byte_count"] != 0:
                            if decoded["record_type"] == 0:
                                self.scHandle.scProgFlash = True
                                self.station.serial.scProgFlashResponse = False
                                while self.station.serial.scProgFlashResponse == False:
                                    pass
                            else:
                                if decoded["record_type"] == 4:
                                    self.station.serial.firstLine = True

                        conn.sendall(line)  # Echo back
                    else:
                        break
                    
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"Client error {addr}: {e}")
                    break
        print(f"Connection closed: {addr}")

    def stop(self):
        """Stop the daemon."""
        print("Stopping server...")
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        if self.thread:
            self.thread.join(timeout=2)
        print("Server stopped.")

# Example usage
if __name__ == "__main__":
    server = TCPEchoDaemon(host="127.0.0.1", port=5000, scHandle=None, stat=None)
    # server.start()

    # try:
    #     while True:
    #         cmd = input("Type 'quit' to stop: ").strip().lower()
    #         if cmd == "quit":
    #             break
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     server.stop()
    #     sys.exit(0)
    server.decoder.decode_line(":10010000214601360121470136007EFE09D2190140")
