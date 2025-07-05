# Mullvad, allow K8s!
Mullvad VPN app and Kubernetes (K8s) do not play well together. This fixes the issue.

This repository consists of two nft tables inspired by [Mullvad's own split tunneling guide](https://mullvad.net/en/help/split-tunneling-with-linux-advanced), and instructions on how to install them.

## Why?

- Because Kubernetes developers want privacy and their own toy cluster on their machines. They want both, not one or the other.
- Kubernetes uses an internal CoreDNS service which, as the name suggests, uses port 53 (DNS). This is a no-no port for Mullvad. Mullvad has special rules preventing arbitrary connections to this port specifically in order to prevent DNS leakage. Connecting to your ISP:s DNS server may indeed compromise your privacy, but CoreDNS operating locally within your K8s cluster does not.
- Kubernetes uses a bridge, and any incoming external traffic to K8s will enter the bridge, and the response (SYN, ACK) will exit into the Mullvad VPN tunnel! This is bad, because its source address will no longer be the public IP address of your computer, but the IP address of the VPN. The client connected to your public IP address, not the VPN's address, so the response packet will be discarded.

## Instructions
Download this repo:
```shell
git clone https://github.com/eat-correctly/mullvad-allow-k8s.git
cd mullvad-allow-k8s
```

Set `MACHINE_ADDR` and `K8S_ADDR` to the correct addresses for your system in ./k8s_bypass_mullvad.nft.

Then run:
```shell
sudo mkdir -p /etc/nftables.d
sudo cp setup/k8s_bypass_mullvad.nft /etc/nftables.d/
sudo sh -c 'echo "#!/usr/sbin/nft -f\ninclude \"/etc/nftables.d/*\"" > /etc/nftables.conf'
sudo systemctl enable nftables --now
```

You're done!

## Test if it works
Install a dnsutils pod:
```shell
kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
```

See if the domain name `kubernetes.default` can be resolved:
```shell
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
```

You should quickly get an output like:
```
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   kubernetes.default.svc.cluster.local
Address: 10.96.0.1
```
