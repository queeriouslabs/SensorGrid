sudo cp queirdos.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/queirdos.service
sudo systemctl daemon-reload
sudo systemctl enable queirdos
sudo systemctl start queirdos
sudo systemctl status queirdos
