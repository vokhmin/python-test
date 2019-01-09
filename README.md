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
    ...
    Connected to RPC server TLSv1.2
    Received a message:
    payloadType: 990
    payload: ""

    Received a Hello event:

    Received a message:
    payloadType: 302
    payload: "\020\001\020\002\020\003\020\004\020\005\020\006\020\007\020\010\020\t\020\013\020\014\020\r\020\016\020\024\020\025\020\026\020\027\020 \020(\020)\0202\0203\020x\020\202\001\020\214\001\020\226\001\020\227\001\020\240\001\020\241\001\020\252\001\020\264\001\020\302\001\020\303\001\020\305\001\020\306\001\020\310\001\020\311\001\020\312\001\020\313\001\020\314\001\020\315\001\020\316\001\020\317\001\020\320\001\020\321\001\020\322\001\020\323\001\020\324\001\020\325\001\020\326\001\020\327\001\020\330\001"
    clientMsgId: "any-random-string"

    Received a ManagerAuth Response:
    permission: ROLE_TRADER_READ
    permission: ROLE_TRADER_CREATE
    permission: ROLE_TRADER_EDIT
    permission: ROLE_TRADER_DELETE
    permission: ROLE_TRADER_CASHIER_FAKE
    permission: ROLE_TRADER_CHANGE_PASSWORD
    permission: ROLE_TRADER_VIEWALL
    permission: ROLE_TRADER_PHONE_TRADING
    permission: ROLE_TRADER_BONUS_CASHIER
    permission: ROLE_MANAGER_CREATE
    permission: ROLE_MANAGER_EDIT
    permission: ROLE_MANAGER_DELETE
    permission: ROLE_MANAGER_CHANGE_PASSWORD
    permission: ROLE_GROUP_READ
    permission: ROLE_GROUP_CREATE
    permission: ROLE_GROUP_EDIT
    permission: ROLE_GROUP_DELETE
    permission: ROLE_PRICE_STREAM_EDIT
    permission: ROLE_SYMBOL_READ
    permission: ROLE_SYMBOL_EDIT
    permission: ROLE_SETTINGS_READ
    permission: ROLE_SETTINGS_EDIT
    permission: ROLE_JOURNAL_READ
    permission: ROLE_ORDER_READ
    permission: ROLE_POSITION_READ
    permission: ROLE_TRADING_HISTORY_READ
    permission: ROLE_TRADING_HISTORY_EXPORT
    permission: ROLE_LIQUIDITY_READ
    permission: ROLE_LIQUIDITY_EDIT
    permission: ROLE_EXPOSURE_READ
    permission: ROLE_INTEGRATION_READ
    permission: ROLE_PRICE_FILTER_EDIT
    permission: ROLE_TRADER_INTRODUCING_BROKER
    permission: ROLE_GUI_SETTINGS_EDIT
    permission: ROLE_REPORT
    permission: ROLE_DYNAMIC_LEVERAGE_EDIT
    permission: ROLE_ENTITY_BOOK_READ
    permission: ROLE_FUNNEL_READ
    permission: ROLE_FUNNEL_EDIT
    permission: ROLE_HOOK_READ
    permission: ROLE_HOOK_EDIT
    permission: ROLE_WITHDRAWAL_REQUEST_READ
    permission: ROLE_WITHDRAWAL_REQUEST_EDIT
    permission: ROLE_KYC_READ
    permission: ROLE_KYC_EDIT
    permission: ROLE_MARKETING_LINKS_READ
    permission: ROLE_MARKETING_LINKS_EDIT
    permission: ROLE_WITHDRAWAL_APPROVE_SETTINGS_READ
    permission: ROLE_WITHDRAWAL_APPROVE_SETTINGS_EDIT
    permission: ROLE_OPERATIONAL_WALLET_READ
    permission: ROLE_OPERATIONAL_WALLET_EDIT
    permission: ROLE_TRADING_ON_BEHALF

    Communication with RPC server is completed



