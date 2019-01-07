import socket
import ssl

hostname = 'spotwaresandbox1.cxchange.com'
context = ssl.create_default_context()

with socket.create_connection((hostname, 5034)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
