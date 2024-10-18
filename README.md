# Simple RTSP Server

This is a basic RTSP (Real-Time Streaming Protocol) server implemented in Python. The main purpose of this server is to capture and log incoming client credentials via basic authentication. It listens for incoming client requests, supports basic authentication, and can handle `DESCRIBE` requests.

## Features

- **Capture Credentials**: Logs username and password sent by clients.
- **Handles DESCRIBE Requests**: Responds with an SDP (Session Description Protocol) message for valid requests.
- **Customizable Port**: Specify a custom port to listen on, or use the default (554).

## Requirements

- Python 3.x
- `colorama` library for colored terminal output

You can install the `colorama` library using pip:

```bash
pip install colorama
```

## Usage

You can run the script with the following command:

```bash
python rtsp_creds.py [--port PORT]
```

### Options

- `--port`: Specify the port number to listen on (default: 554).
  
  Example to run on port 8080:

  ```bash
  python script.py --port 8080
  ```

  If the `--port` option is not provided, the server will use the default port 554.

## ASCII Art Banner

When the script is executed, it will print an ASCII art banner in the terminal indicating that the RTSP server is running.


## Example

To start the RTSP server on the default port:

```bash
python rtsp_creds.py
```

To start the RTSP server on a custom port (e.g., 8080):

```bash
python rtsp_creds.py --port 8080
```

## Error Handling

If a script.pyclient sends an unauthorized request, the server will respond with a 401 Unauthorized status code.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- This project utilizes the `colorama` library for improved terminal output.
- Inspired by the need for a simple RTSP server for testing and educational purposes.

## Contributing

If you wish to contribute to this project, please fork the repository and create a pull request with your improvements.
