# phpIPAM to Bind converter

Automatically make bind config files:
reverse zone files
one forward zone file
config files with list of reverse zones for master and slave Bind DNS servers.

# Usage:

Before first run please check setup.py file. Py default it point to real bind file location. Possible you should change pointers to temporary file locations.

In phpIPAM:
Go to Administration / "Import / Export"
Press "Prepare XLS dump"
Open downloaded file
Save file as CSV file. Do not rename file. Only change extension.
Delimeter can be changed in setup.py. By default is semicolon (;).

Format of required CSV file:

<ip_address>;[some_other_field];[some_other_field];<host_name>[;[some_other_fields]]

For example:

8.8.4.4;;;dns.google.com
8.8.8.8;;;dns2.google.com;Google DNS Server