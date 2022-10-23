#!/bin/sh
sleep 2
git pull
python3.0 main.py 192.168.0.171 & #TODO: remove hard-coding of ip