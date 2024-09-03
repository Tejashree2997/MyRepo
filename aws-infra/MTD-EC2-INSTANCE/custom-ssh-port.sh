#!/bin/bash

sestatus
getenforce
sudo setenforce 0
getenforce
sestatus
sed -i 's/^#Port 22/Port 1043/' /etc/ssh/sshd_config
systemctl restart sshd
sudo sed -i 's/^SELINUX=.*/SELINUX=permissive/' /etc/selinux/config
sestatus
sudo systemctl reload sshd