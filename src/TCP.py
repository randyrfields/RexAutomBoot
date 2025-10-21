import socket
import threading
import sys

class TCPEchoDaemon:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None

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

    def handle_client(self, conn, addr):
        """Handle a single client connection."""
        with conn:
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received from {addr}: {data.decode().strip()}")
                    print("length = ", len(data))
                    conn.sendall(data)  # Echo back
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
    server = TCPEchoDaemon(host="127.0.0.1", port=5000)
    server.start()

    try:
        while True:
            cmd = input("Type 'quit' to stop: ").strip().lower()
            if cmd == "quit":
                break
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        sys.exit(0)
