#!/usr/bin/python3

import json

host_dict = {}
with open('allip.csv', 'r', encoding='cp1251') as r:
  for line in r:
    net, host, _, _, name, *_ = line.split(';')
    if host_dict.get(net) != None:
      host_dict[net].append((host, name))
    else:
      host_dict[net] = [(host, name)]
print(host_dict)
#print(json.dumps(host_dict, sort_keys=True, indent=4))

	
