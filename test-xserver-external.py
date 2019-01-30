# Some useful links:
# - https://carlo-hamalainen.net/2013/01/24/python-ssl-socket-echo-test-with-self-signed-certificate/
# 

import socket, ssl, pprint, struct
import hashlib
import XSModelMessages_External_pb2, XSMessages_External_pb2
import CommonModelMessages_External_pb2, CommonMessages_External_pb2

def encode_length(data):
    """Encode a data length as int32"""
    return struct.pack('>I', len(data))

def decode_length(data):
    """ Decode a protobuf length as int32 """
    return struct.unpack('>I', data)[0]

def send_message(conn, msg):
    """ Send a message, prefixed with its size, to a TPC/IP socket """
    print("Try to send the request: \n%s" % msg)
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

port = 5011
hostname = '127.0.0.1'
plant_id = 'local'
env_name = 'local'
login = 1000
password = '1'

auth_req = XSMessages_External_pb2.ProtoManagerAuthReq()
auth_req.login = login
auth_req.passwordHash = hashlib.md5(password.encode('utf-8')).hexdigest()
auth_req.plantId = plant_id.encode('utf-8')
auth_req.environmentName = env_name.encode('utf-8')

print(auth_req)

token_req = XSMessages_External_pb2.ProtoManagerGetAuthTokenReq()

print(token_req)

context = ssl.create_default_context()

with socket.create_connection((hostname, port)) as sock:
    with ssl.wrap_socket(sock, ca_certs="certs.pem", cert_reqs=ssl.CERT_REQUIRED, server_side=False) as ssock:
    # with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(repr(ssock.getpeername()))
        print(ssock.cipher())
        print(pprint.pformat(ssock.getpeercert()))
        print('Connected to RPC server', ssock.version())
        res = recv_message(ssock, XSMessages_External_pb2.ProtoHelloEvent, XSModelMessages_External_pb2.PROTO_HELLO_EVENT)
        print('Received a Hello Event: \n%s' % res)

        msg = CommonMessages_External_pb2.ProtoMessage()
        msg.payloadType = XSModelMessages_External_pb2.PROTO_MANAGER_AUTH_REQ
        msg.clientMsgId = "any-random-string"
        msg.payload = auth_req.SerializeToString()
        send_message(ssock, msg)
        res = recv_message(ssock, XSMessages_External_pb2.ProtoManagerAuthRes, XSModelMessages_External_pb2.PROTO_MANAGER_AUTH_RES)
        print('Received a ManagerAuth Response: \n%s' % res)

        msg = CommonMessages_External_pb2.ProtoMessage()
        msg.payloadType = XSModelMessages_External_pb2.PROTO_MANAGER_GET_AUTH_TOKEN_REQ
        msg.clientMsgId = "any-random-string-2"
        msg.payload = auth_req.SerializeToString()
        send_message(ssock, msg)
        res = recv_message(ssock, XSMessages_External_pb2.ProtoManagerGetAuthTokenRes, XSModelMessages_External_pb2.PROTO_MANAGER_GET_AUTH_TOKEN_RES)
        print('Received a ManagerAuth Response: \n%s' % res)

        print('Communication with RPC server is completed')
