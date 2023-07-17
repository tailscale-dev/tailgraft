# tailgraft

Grafting Tailscale into your Raspberry Pi!

## Usage

On a macOS system, run `sudo python3 tailgraft.py` with a SD card flashed with Ubuntu Server plugged in. The script will customize the cloud-init configuration and enable Tailscale on first boot.

On Linux, run `sudo python3 tailgraft.py /path/to/system-boot` instead. The system-boot partition will be mounted somewhere by your desktop environment and distribution of choice. You will need to figure out what folder this is with the `mount` command.