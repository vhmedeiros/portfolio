#!/bin/bash

# ─── Usuário victor com senha ───────────────────────────────────────────────
useradd -m -s /bin/bash victor
echo "victor:Med@2021" | chpasswd
usermod -aG sudo victor

# Permite login por senha via SSH
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
systemctl restart ssh

# ─── Atualizações básicas ────────────────────────────────────────────────────
apt-get update -y
apt-get install -y curl git nano

# ─── Docker ─────────────────────────────────────────────────────────────────
curl -fsSL https://get.docker.com | sh
usermod -aG docker victor
usermod -aG docker ubuntu
systemctl enable docker
systemctl start docker

# ─── Docker Compose plugin ───────────────────────────────────────────────────
apt-get install -y docker-compose-plugin

# ─── Firewall: libera portas 80 e 443 ───────────────────────────────────────
iptables -I INPUT -p tcp --dport 80 -j ACCEPT
iptables -I INPUT -p tcp --dport 443 -j ACCEPT
iptables -I INPUT -p tcp --dport 22 -j ACCEPT

# Persiste as regras do iptables
apt-get install -y iptables-persistent
netfilter-persistent save

# ─── Pasta do projeto ────────────────────────────────────────────────────────
mkdir -p /home/victor/portfolio
chown victor:victor /home/victor/portfolio

echo "✅ Setup concluído!" >> /var/log/cloud-init-setup.log