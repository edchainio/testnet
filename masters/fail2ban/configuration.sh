#!/usr/bin/env bash

sh -c 'echo "[DEFAULT]" >> /etc/fail2ban/jail.local'

sh -c 'echo "bantime = 7200" >> /etc/fail2ban/jail.local'

sh -c 'echo "findtime = 1200" >> /etc/fail2ban/jail.local'

sh -c 'echo "maxretry = 3" >> /etc/fail2ban/jail.local'

sh -c 'echo "destemail = <email>" >> /etc/fail2ban/jail.local'

sh -c 'echo "sendername = security@<hostname>" >> /etc/fail2ban/jail.local'

sh -c 'echo "banaction = iptables-multiport" >> /etc/fail2ban/jail.local'

sh -c 'echo "mta = sendmail" >> /etc/fail2ban/jail.local'

sh -c 'echo "action = %(banaction)s[name=%(__name__)s, bantime=\"%(bantime)s\", port=\"%(port)s\", protocol=\"%(protocol)s\", chain=\"%(chain)s\"], %(mta)s-whois-lines[name=%(__name__)s, dest=\"%(destemail)s\", logpath=%(logpath)s, chain=\"%(chain)s\"]" >> /etc/fail2ban/jail.local'

sh -c 'echo "" >> /etc/fail2ban/jail.local'

sh -c 'echo "[sshd]" >> /etc/fail2ban/jail.local'

sh -c 'echo "enabled = true" >> /etc/fail2ban/jail.local'

sh -c 'echo "" >> /etc/fail2ban/jail.local'

sh -c 'echo "" >> /etc/fail2ban/jail.local'

sh -c 'echo "[sshd-ddos]" >> /etc/fail2ban/jail.local'

sh -c 'echo "enabled = true" >> /etc/fail2ban/jail.local'

sh -c 'echo "" >> /etc/fail2ban/jail.local'

sh -c 'echo "[nginx-http-auth]" >> /etc/fail2ban/jail.local'

sh -c 'echo "enabled = true" >> /etc/fail2ban/jail.local'

systemctl restart fail2ban

systemctl enable fail2ban