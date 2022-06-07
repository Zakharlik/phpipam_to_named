# DNS file maker

Gets csv file for phpipam, compiles it with old dns reverse zone files.
Makes new reverse zones files and named config file for that zones.



# Usage:

Go to Administration / "Import / Export"
Press "Prepare XLS dump"
Open downloaded file
Save file as CSV file. Do not rename file. Only change extention.
Delimeter must be semicolon (;). Comma delimeter will be added in next versions.

Format of required CSV file:

<ip_address>;;;<host_name>[;[some_other_fields]]

For example:

8.8.4.4;;;dns.google.com
8.8.8.8;;;dns2.google.com;Google DNS Server

