#!/bin/bash
mongo -u my_root -p my_123456 <<EOF
use docs;
db.createUser({user:'your_user',pwd:'your_pwd',roles:[{role:'readWrite',db:'docs'}]});
EOF