### Test-xServer-External

This project demonstrates a way to communicate with xServer by a manager protocol. The protocol based on protobuf so you need to have a specific set of the proto-files:

- XSModelMessages_External.proto
- XSMessages_External.proto
- CommonModelMessages_External.proto
- CommonMessages_External.proto
- XIDMessages_External.proto
- XIDModelMessages_External.proto

. To compile proto-files use a shell script *compile-proto.sh* where you have to define `SRC_DIR` environment variable which referes to the directory with proto-files. After successful compilation you can try python script *test-xserver-external.py* to run a test connection. You sould to define several variable in the script file, for example:

- login, password
- plant_id, env_name
- hostname, port

To start the script use python3:

```shell
    ~/python-test$ python3 test-xserver-external.py
```

the tail of the output should look like:

```
plantId: "????????????"
environmentName: "???"
login: ????
passwordHash: "????????????????????????"


('51.15.17.7', 5011)
('ECDHE-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128)
{'OCSP': ('http://ocsp.comodoca.com',),
 ... ,
 'version': 3}
Connected to RPC server TLSv1.2
Received a message:
payloadType: 990
payload: ""

Received a Hello Event:

Try to send the request:
payloadType: 301
payload: "\022\020spotwarecxchange\032\001x \277N* 39ad2a1609b0e7f7a7a6537b54aae7d9"
clientMsgId: "any-random-string"

Received a message:
payloadType: 302
payload: "\020\001\020\002\020\006\020\007\020\024\020x\020\202\001\020\214\001\020\226\001"
clientMsgId: "any-random-string"

Received a ManagerAuth Response:
permission: ROLE_TRADER_READ
permission: ROLE_TRADER_CREATE
permission: ROLE_TRADER_CHANGE_PASSWORD
permission: ROLE_TRADER_VIEWALL
permission: ROLE_GROUP_READ
permission: ROLE_JOURNAL_READ
permission: ROLE_ORDER_READ
permission: ROLE_POSITION_READ
permission: ROLE_TRADING_HISTORY_READ

Try to send the request:
payloadType: 850
payload: "\022\020spotwarecxchange\032\001x \277N* 39ad2a1609b0e7f7a7a6537b54aae7d9"
clientMsgId: "any-random-string-2"

Received a message:
payloadType: 851
payload: "\0222f85566c2-9004-40b1-96f3-f869ea94cf96-1548850137968"
clientMsgId: "any-random-string-2"

Received a ManagerAuth Response:
token: "f85566c2-9004-40b1-96f3-f869ea94cf96-1548850137968"

Communication with RPC server is completed
```

To test the token authorization to XID use python3 and `test-proxy-connect.py` script:

```shell
    ~/python-test$ python3 test-proxy-connect.py
```

the tail of the output should look like:

```
timestamp: 1548852186159

authToken: "f85566c2-9004-40b1-96f3-f869ea94cf96-1548850137968"
plantId: "????????????"
environment: "???"

('51.15.17.7', 5034)
('ECDHE-RSA-AES128-GCM-SHA256', 'TLSv1/SSLv3', 128)
{'OCSP': ('http://ocsp.comodoca.com',),
 ...,
 'version': 3}
Connected to RPC server TLSv1.2
Try to send the request:
-----
timestamp: 1548852186159


Waiting a message ... To break press ^C


8 1 53 1 7
Received a message:
-----
(timestamp: 1548852186159
, None)
Received the message with client-msg-id[None] and the payload type 53:
-----
timestamp: 1548852186159

Received the expected Ping response:
-----
timestamp: 1548852186159

Try to send the request with msg-client-id(any-random-string-2x) :
-----
timestamp: 1548852186159

Try to send the request with msg-client-id(any-random-string-2) :
-----
authToken: "b15ce89d-d198-408a-9700-24718be2e922-1548852159190"
plantId: "spotwarecxchange"
environment: "x"

36 1 5 1 35
Received a message:
-----
(timestamp: 1548852186159
, 'any-random-string-2x')
Received the message with client-msg-id[any-random-string-2x] and the payload type 53:
-----
timestamp: 1548852186159

29 1 5 1 28
Received a message:
-----
(, 'any-random-string-2')
Received the message with client-msg-id[any-random-string-2] and the payload type 2001:
-----

Received the expected Auth response:
-----

Successful authorization...
Communication with RPC server is completed
```
