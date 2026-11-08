1. fix;
python3 fix.py DAP-2610-v206.mib.orig DAP-2610-v206.mib

2. build:
~/.local/bin/mibdump --mib-source ./mibs --mib-source ./mibs/mibs/  --destination-directory ./out --destination-format json   DAP-2610-v206