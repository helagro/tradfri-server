
sleep 2
git pull

pkill -f "python3 tradfri_server.py"
nohup python3 tradfri_server.py &