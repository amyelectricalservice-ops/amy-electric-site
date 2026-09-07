#!/usr/bin/env bash
# Simple static server for local testing
cd "$(dirname "$0")/.."
python3 -m http.server 8000 &
SERVER_PID=$!
echo $SERVER_PID > .server_pid
