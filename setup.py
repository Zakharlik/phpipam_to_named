###
# Setup.py - config file

# Master zone. Name of forward zone.
master_zone = 'ats'

# IP address of master DNS. Need by config for slave DNS
master_ip = '10.40.1.9'

cvs_file = 'data/allip.csv'  # Filtered CVS file in format <zone>;<last_octet>;IN;PTR;<hostname>;[any_other_fields]
zones_dir = 'data/zones'  # Named zones. Usually /var/named
reverse_zones_dir = 'data/zones/reverse'  # Reverse zones. Usually /var/named/reverse
conf_dir = 'data/config'  # Config files directory. Usually /etc/named/
cvs_dir = 'data'  # Phpipam files
delimiter = ';'  # Delimiter used in CSV file
forward_zone_name = 'ats.zone'  # Forward zone file to modify. Usually in /var/named
