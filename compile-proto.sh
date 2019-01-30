#!/bin/sh

export SRC_DIR=~/projects/spotware/xserver/cs-doc/src/main/external/proto/
export DST_DIR=~/projects/sandbox/python-test

protoc -I=$SRC_DIR --python_out=$DST_DIR \
    $SRC_DIR/CommonMessages_External.proto \
    $SRC_DIR/CommonModelMessages_External.proto \
    $SRC_DIR/XSMessages_External.proto \
    $SRC_DIR/XSModelMessages_External.proto \
    $SRC_DIR/XIDMessages_External.proto \
    $SRC_DIR/XIDModelMessages_External.proto
