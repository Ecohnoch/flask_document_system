#!/bin/bash
mongo <<EOF
use admin;
db.auth('my_root', 'my_123456');
use dmx_aluminum;
db.createUser({user:'your_user',pwd:'your_pwd',roles:[{role:'readWrite',db:'docs'}]});
db.createCollection("user");
EOF