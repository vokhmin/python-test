# Some useful links:
# - https://carlo-hamalainen.net/2013/01/24/python-ssl-socket-echo-test-with-self-signed-certificate/
# 

import socket, ssl, pprint, struct
import hashlib, time
import XSModelMessages_External_pb2, XSMessages_External_pb2
import CommonModelMessages_External_pb2, CommonMessages_External_pb2
import XIDModelMessages_External_pb2, XIDMessages_External_pb2
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint

proxy_port = 5034
# hostname = '127.0.0.1'
hostname = 'proxy.spotware.cxchange.com'
plant_id = 'spotwarecxchange'
env_name = 'x'
# plant_id = 'local'
# env_name = 'local'

token = '86bccd86-5793-4b19-a9e7-416605518b71-1548845259789'

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ProtocolError(Error):
    """Exception raised for errors in the input."""
    def __init__(self, code, message):
        self.code = code
        self.message = message

def encode_length(data):
    """Encode a data length as Protobuf Raw Varint"""
    return _VarintBytes(len(data))

def send_data(conn, str):
    """ Send a string data to a TPC/IP socket """
    conn.sendall(str.encode('utf-8'))

def send_message(conn, msg):
    """ Send a message, prefixed with its size, to a TPC/IP socket """    
    print("Try to send the request: \n-----\n%s" % msg)
    type = _VarintBytes(msg.payloadType)
    payload = msg.SerializeToString()
    length = _VarintBytes(len(type) + len(payload))
    conn.sendall(length + type + payload)

def send_message_with_id(conn, msg, msg_id):
    """ Send a message, prefixed with its size, to a TPC/IP socket """    
    print("Try to send the request with msg-client-id(%s) :\n-----\n%s" % (msg_id, msg))
    proto = CommonMessages_External_pb2.ProtoMessage()
    proto.clientMsgId = msg_id
    proto.payloadType =  msg.payloadType
    proto.payload = msg.SerializeToString()
    proto_type = _VarintBytes(CommonModelMessages_External_pb2.PROTO_MESSAGE)
    proto_data = proto.SerializeToString()
    conn.sendall(_VarintBytes(len(proto_type) + len(proto_data)))
    conn.sendall(proto_type)
    conn.sendall(proto_data)

def decode_variant(data):
    """ Decode a protobuf varint to an int """
    return _DecodeVarint(data, 0)[0]

def recv_varint(conn):
    buf = b''
    while True:
        try:
            buf += conn.recv(1)
            val = decode_variant(buf)
            break
        except IndexError:
            pass
    return val, len(buf)

def parse_proto_message(payload, payloadType):
    if payloadType == CommonModelMessages_External_pb2.ERROR_RES:
        msg = CommonMessages_External_pb2.ProtoErrorRes()
        msg.ParseFromString(payload)
        raise ProtocolError(msg.errorCode, msg.description)
    elif payloadType == CommonModelMessages_External_pb2.PING_RES:
        msg = CommonMessages_External_pb2.ProtoPingRes()
        msg.ParseFromString(payload)
        return msg
    elif payloadType == XIDModelMessages_External_pb2.XID_MANAGER_TOKEN_AUTH_RES:
        msg = XIDMessages_External_pb2.ProtoXIDManagerTokenAuthRes()
        msg.ParseFromString(payload)
        return msg
    else:
        raise ProtocolError(None, "Couldn't parse the proto message as the payload type " + payloadType)
        

def load_message(payload, payloadType):
    if payloadType == CommonModelMessages_External_pb2.PROTO_MESSAGE:
        proto = CommonMessages_External_pb2.ProtoMessage()
        proto.ParseFromString(payload)
        return parse_proto_message(proto.payload, proto.payloadType), proto.clientMsgId
    else:
        return parse_proto_message(payload, payloadType), None

def recv_message(conn):
    """ Receive a message, prefixed with its size, from a TCP/IP socket """
    msg_size, len_size = recv_varint(conn)
    msg_type, len_type = recv_varint(conn)
    data = b''
    # Receive the message data
    print(msg_size, len_size, msg_type, len_type, msg_size - len_type)
    data = conn.recv(msg_size - len(data))
    # Decode the message
    msg = load_message(data, msg_type)
    print('Received a message:\n-----\n%s' % msg.__str__())
    return msg

ping_req = CommonMessages_External_pb2.ProtoPingReq()
ping_req.timestamp = int(round(time.time() * 1000))
ping_msg_id = "any-random-string"

print(ping_req)

auth_req = XIDMessages_External_pb2.ProtoXIDManagerTokenAuthReq()
auth_req.plantId = plant_id.encode('utf-8')
auth_req.environment = env_name.encode('utf-8')
auth_req.authToken = token
auth_msg_id = "any-random-string-2"

print(auth_req)

context = ssl.create_default_context()

handshake = """GET https://bokka1-dev.p.ctrader.com:5034/ HTTP/1.1
                Upgrade:protobuf
                Proxy-Protocol:uproxy-v1\n\n"""

with socket.create_connection((hostname, proxy_port)) as sock:
    # with ssl.wrap_socket(sock, ca_certs="certs.pem", cert_reqs=ssl.CERT_REQUIRED, server_side=False) as ssock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(repr(ssock.getpeername()))
        print(ssock.cipher())
        print(pprint.pformat(ssock.getpeercert()))
        print('Connected to RPC server', ssock.version())
        send_data(ssock, handshake)
        send_message(ssock, ping_req)
        print('\nWaiting a message ... To break press ^C\n\n')
        while True:
            res, res_msg_id = recv_message(ssock)
            print('Received the message with client-msg-id[%s] and the payload type %d:\n-----\n%s' % (res_msg_id, res.payloadType, res))
            if res.payloadType == CommonModelMessages_External_pb2.PING_RES:
               print('Received the expected Ping response: \n-----\n%s' % res)
               break
        send_message_with_id(ssock, ping_req, auth_msg_id + 'x')
        send_message_with_id(ssock, auth_req, auth_msg_id)
        while True:
            try:
                res, res_msg_id = recv_message(ssock)
            except ProtocolError as e:
                print("!During handling of the Auth request the exception occurred: \n\t%s" % e)
                break
            print('Received the message with client-msg-id[%s] and the payload type %d:\n-----\n%s' % (res_msg_id, res.payloadType, res))
            if res_msg_id == auth_msg_id:
                if res.payloadType == XIDModelMessages_External_pb2.XID_MANAGER_TOKEN_AUTH_RES:
                    print('Received the expected Auth response: \n-----\n%s' % res)
                    print('Successful authorization...')
                    break
                else:
                    print('Received an unexpected response for Auth request: \n-----\n%s' % res)
                    break
                
        print('Communication with RPC server is completed')
