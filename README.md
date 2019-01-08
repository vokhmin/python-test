### Test-xServer-External

This project demonstrates a way to communicate with xServer by a manager protocol. The protocol based on protobuf so you need to have a specific set of the proto-files:

- XSModelMessages_External.proto
- XSMessages_External.proto
- CommonModelMessages_External.proto
- CommonMessages_External.proto

. To compile proto-files use a shell script *compile-proto.sh* where you have to define `SRC_DIR` environment variable which referes to the directory with proto-files. After successful compilation you can try python script *test-xserver-external.py* to run a test connection. You sould to define several variable in the script file, for example:

- login, password
- plant_id, env_name
- hostname, port

To start the script use python3:

    ~/python-test$ python3 test-xserver-external.py

