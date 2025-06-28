# mullvad-allow-coredns
Mullvad VPN app and Kubernetes CoreDNS do not play well together. This fixes the issue.

This light service prevents the Mullvad VPN app from interfering with Kubernetes' CoreDNS by adding a few firewall rules whenever Mullvad reconnects. 
Mullvad will clear firewall rules when reconnecting, so it's important to monitor Mullvad and re-apply these rules whenever that happens.

## Instructions
Set `ALLOWED_ADDRESSES` in ./mullvad-allow-coredns.py to those that fit the service and pod networks on your Kubernetes cluster.

Then run:
```shell
sudo install -o root -g root -m 755 \
  mullvad-allow-coredns.py \
  /usr/local/bin/mullvad-allow-coredns
sudo install -o root -g root -m 755 \
  mullvad-allow-coredns.service \
  /etc/systemd/user/mullvad-allow-coredns.service
sudo systemctl enable \
  /etc/systemd/user/mullvad-allow-coredns.service --now
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
