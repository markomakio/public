# Ansible playbook for setting basic hardened Linux desktop environment
Created to help possible reinstall configuration. Tested to work with RHEL 10. Roles are used for easy skipping and/or modifying order.

## Hardening
2025-06-22 DRAFT - CIS Red Hat Enterprise Linux 10 Benchmark for Level 2 - Workstation gave score `91.22%`. For failed ones, some configurations I didn't find meaningful to implement for my environment and many failed ones are false positives.

Evaluated with:
```
$ sudo oscap xccdf eval --report report.html --profile xccdf_org.ssgproject.content_profile_cis_workstation_l2 /usr/share/xml/scap/ssg/content/ssg-rhel10-ds.xml
```

## Other info
* Bash prompt and history are customized.
* Bash commands are also logged by rsyslog.
* umask is 027
* Sshd is disabled by default but can be enabled by changing `sshd_enabled` variable.
* Sshd listen port can also be defined by `sshd_port` variable. SELinux is modified if needed.
* Firewalld rules for sshd are created if necessary. Default firewalld zone is `drop`.
* EPEL repository is enabled
* Basic sysctl hardening.
* Audit ruleset should be ok. Made for 2GiB /var/log/audit partition.
* Aide is installed and database init done.

### Aide
Aide can report changes of thousands of files at once after dnf updates. For that reason, I use it the following way:
```
# Before changes I verify no unexpected changes are found.
$ /usr/bin/sudo /usr/sbin/aide --check

# I update the system or whatever changes.
$ /usr/bin/sudo /usr/bin/dnf update

# I update aide database by using script.
$ /usr/bin/sudo /root/bin/update-aide.sh
```

