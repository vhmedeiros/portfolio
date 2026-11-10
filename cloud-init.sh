#!/bin/bash
# Script de inicialização da VM (Oracle Cloud). Nunca coloque senhas ou chaves aqui:
# este arquivo é público no GitHub.

# ─── Usuário victor (acesso só por chave SSH) ───────────────────────────────
useradd -m -s /bin/bash victor
usermod -aG sudo victor

# Reaproveita a chave pública cadastrada na criação da instância (usuário ubuntu)
mkdir -p /home/victor/.ssh
cp /home/ubuntu/.ssh/authorized_keys /home/victor/.ssh/authorized_keys
chown -R victor:victor /home/victor/.ssh
chmod 700 /home/victor/.ssh
chmod 600 /home/victor/.ssh/authorized_keys

# A senha do victor (usada pelo sudo) é definida manualmente após o primeiro login,
# entrando como ubuntu:  sudo passwd victor
# O login SSH por senha continua desabilitado (padrão da imagem).

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
