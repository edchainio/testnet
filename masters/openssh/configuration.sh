#!/usr/bin/env bash

chown -R <username>:<username> /etc/ssh/<username>

chmod 755 /etc/ssh/<username>

chmod 644 /etc/ssh/<username>/authorized_keys

sed -i -e '/^Port/s/^.*$/Port <ssh_port>/' /etc/ssh/sshd_config

sed -i -e '/^PermitRootLogin/s/^.*$/PermitRootLogin no/' /etc/ssh/sshd_config

sed -i -e '/^#AuthorizedKeysFile/s/^.*$/AuthorizedKeysFile \/etc\/ssh\/<username>\/authorized_keys/' /etc/ssh/sshd_config

sed -i -e '/^PasswordAuthentication/s/^.*$/PasswordAuthentication no/' /etc/ssh/sshd_config

sh -c 'echo "" >> /etc/ssh/sshd_config'

sh -c 'echo "" >> /etc/ssh/sshd_config'

sh -c 'echo "AllowUsers <username>" >> /etc/ssh/sshd_config'

systemctl reload sshd