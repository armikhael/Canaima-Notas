#
# Regular cron jobs for the canaima-notas package
#
0 4	* * *	root	[ -x /usr/bin/canaima-notas_maintenance ] && /usr/bin/canaima-notas_maintenance
