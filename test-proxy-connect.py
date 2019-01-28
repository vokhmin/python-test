# Some useful links:
# - https://carlo-hamalainen.net/2013/01/24/python-ssl-socket-echo-test-with-self-signed-certificate/
# 

import socket, ssl, pprint, struct
import hashlib, time
import XSModelMessages_External_pb2, XSMessages_External_pb2
import CommonModelMessages_External_pb2, CommonMessages_External_pb2

def encode_length(data):
    """Encode a data length as int32"""
    return struct.pack('>I', len(data))

def decode_length(data):
    """ Decode a protobuf length as int32 """
    return struct.unpack('>I', data)[0]

def send_data(conn, str):
    """ Send a string data to a TPC/IP socket """
    conn.sendall(str.encode('utf-8'))

def send_message(conn, msg):
    """ Send a message, prefixed with its size, to a TPC/IP socket """
    data = msg.SerializeToString()
    size = encode_length(data)
    conn.sendall(size + data)

def recv_message(conn, msg_type, msg_type_id):
    """ Receive a message, prefixed with its size, from a TCP/IP socket """
    # Receive the size of the message data
    data = b''
    while True:
        try:
            data += conn.recv(4)
            size = decode_length(data)
            break
        except IndexError:
            pass
    # Receive the message data
    data = conn.recv(size)
    # Decode the message
    msg = CommonMessages_External_pb2.ProtoMessage()
    msg.ParseFromString(data)
    print("Received a message:")
    print(msg)
    res = msg_type()
    if msg.payloadType == msg_type_id:
        res.ParseFromString(msg.payload)
        return res
    else:
        print("Warnigin!.. Was expected a message with thre payload type", msg_type_id)
        return data

hostname = 'spotwaresandbox1.cxchange.com'
#hostname = '127.0.0.1'
proxy_port = 5034
plant_id = 'spotwaresandbox1'
env_name = 'x'

ping_req = CommonMessages_External_pb2.ProtoPingReq()
ping_req.timestamp = int(round(time.time() * 1000))

ping = CommonMessages_External_pb2.ProtoMessage()
ping.payloadType = CommonModelMessages_External_pb2.PING_REQ
ping.clientMsgId = "any-random-string"
ping.payload = ping_req.SerializeToString()

context = ssl.create_default_context()

handshake = 'Upgrade:protobuf\nProxy-Protocol:uproxy-v1\n\n'


with socket.create_connection((hostname, proxy_port)) as sock:
    #with ssl.wrap_socket(sock, ca_certs="certs.pem", cert_reqs=ssl.CERT_REQUIRED, server_side=False) as ssock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(repr(ssock.getpeername()))
        print(ssock.cipher())
        print(pprint.pformat(ssock.getpeercert()))
        print('Connected to RPC server', ssock.version())
        # res = recv_message(ssock, XSMessages_External_pb2.ProtoHelloEvent, XSModelMessages_External_pb2.PROTO_HELLO_EVENT)
        # print('Received a Hello Event: \n%s' % res)
        send_data(ssock, handshake)
        b = b''
        #print(ssock.recv(1))
        send_message(ssock, ping)
        res = recv_message(ssock, CommonMessages_External_pb2.ProtoPingRes, CommonModelMessages_External_pb2.PING_RES)
        print('Received a Ping Response: \n%s' % res)
        print('Communication with RPC server is completed')
