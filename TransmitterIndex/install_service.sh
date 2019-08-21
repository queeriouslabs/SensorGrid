sudo cp shodan_say.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/transmitter_index.service
sudo systemctl daemon-reload
sudo systemctl enable transmitter_index
sudo systemctl start transmitter_index
sudo systemctl status transmitter_index
