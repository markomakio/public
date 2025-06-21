#!/bin/bash
/usr/sbin/aide -u
CODE=$?
if [[ ${CODE} -gt 0 ]] && [[ ${CODE} -le 7 ]] ; then
	/bin/mv /var/lib/aide/aide.db.gz /var/lib/aide/aide.db.gz-$(date +"%Y%m%d_%H%M%S") && /bin/mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
fi
echo "aide exit code: ${CODE}"
/bin/ls -l /var/lib/aide/
