# tailgraft

Graft Tailscale onto your Raspberry Pi's SD card and join it to your tailnet automatically on its very first boot. More background and details in the [blog post announcing this project][blog].

## Usage

This script is designed to be run after you've flashed an operating system onto an SD card but before you've booted it in a Raspberry Pi for the first time. It assumes you are using Linux or macOS and have `python3` installed but otherwise has no external dependencies.

1. Clone this repository or download the `tailgraft.py` script.
1. Once the operating system is flashed, run the script with `sudo python3 tailgraft.py`.
1. Answer the prompts to configure Tailscale on your Raspberry Pi. One of the prompts will request an auth key, which you can generate from your [Tailscale admin console](https://login.tailscale.com/admin/settings/keys).

When your Rasbperry Pi boots up, you should see it in your Admin console's [**Machines**](https://login.tailscale.com/admin/machines) page and you should be able to use to [Tailscale SSH](https://tailscale.com/tailscale-ssh/) to connect to it.

```
tailscale ssh ubuntu@<hostname>
```

Depending on your ACL configuration, you may be prompted to authenticate with Tailscale.

## How it works

More details about how this script uses `cloud-init` can be found in the [companion blog post][blog].

[blog]: https://tailscale.dev/blog/tailgraft

## Contributing

Issues and pull requests welcome!
