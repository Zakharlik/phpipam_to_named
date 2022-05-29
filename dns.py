#!/usr/bin/python3
import os
import re
import datetime

host_dict = {}

data_dir = 'data'
zones_dir = 'zones'
out_dir = 'zones'
conf_dir = 'data'
# todo: Make near real file structure

# TODO: Make forward zone

def push_dict(host_dict, net, host, name):
    if host_dict.get(net) != None:
        host_dict[net].add((host, name.strip('.')))
    else:
        host_dict[net] = {(host, name.strip('.'))}
    return host_dict


def get_reverse_zones(host_dict, file):
    net = re.search(r'\\(\S*)\.zone', file).group(1)
    with open(file,'r') as f:
        for line in f:
            if re.search('^\d',line):
                host, _, _, name = line.split()
                host_dict = push_dict(host_dict, net, host, name)
    return host_dict


def get_zone(host_dict, file):
    netl = ['','','']
    with open(file, 'r') as f:
        for line in f:
            if re.search(r'^[a-zA-Z]', line):
                name, _, _, ip = line.split()
                netl[0], netl[1], netl[2], host = ip.split('.')
                net = '.'.join(netl)
                host_dict = push_dict(host_dict, net, host, name)
    return host_dict


def get_zones(host_dict, dir):
    files = os.listdir(dir)
    for file in files:
        if re.search(r"^\d.*\.zone$", file):
            host_dict = get_reverse_zones(host_dict, os.path.join(dir, file))
        elif re.search(r".*\.zone$", file):
            host_dict = get_zone(host_dict, os.path.join(dir, file))
    return host_dict


def get_csv(host_dict):
    # TODO: make check for non latin characters

    with open('data/allip.csv', 'r', encoding='cp1251') as r:
        for line in r:
            net, host, _, _, name, *_ = line.split(';')
            host_dict = push_dict(host_dict, net, host, name)
    return host_dict


def make_zones(host_dict):
    for zone in host_dict:
        ver = 1
        filename = os.path.join(out_dir, zone + '.zone')
        if os.path.exists(filename):
            with open(filename, 'r') as r:
                for line in r:
                    version = re.search(r'(\d+).*serial', line)
                    if version:
                        version = version.group(1)
                        if version[:8] == datetime.datetime.now().strftime('%Y%m%d'):
                            ver = int(version[8:])+1
                        break

        version = '{}{:0>2}'.format(datetime.datetime.now().strftime('%Y%m%d'), ver)
        with open(filename, 'w') as w:
            w.write(f'$TTL 3H\n'
                    f'@	IN SOA	@ ns1.ats. (\n'
                    f'					{version}	; serial\n'
                    f'					1D	; refresh\n'
                    f'					1H	; retry\n'
                    f'					1W	; expire\n'
                    f'					3H )	; minimum\n'
                    f'@		IN	NS	ns1.ats.\n'
                    f')\n')
            line = list(host_dict[zone])
            line.sort(key = lambda x: int(x[0]))
            for host, name in line:
                w.write(f'{host}	IN	PTR	{name + "."}\n')


def make_reverse_conf(conf_dir, rzones_dir):
    files = os.listdir(rzones_dir)
    with open(os.path.join(conf_dir, 'reverse'), 'w') as w:
        for filename in files:
            print(filename)
            reverse_name = '.'.join(reversed(filename.split('.')[:3]))
            w.write(f'zone "{reverse_name}.in-addr.arpa" {{\n'
                    f'        type master;\n'
                    f'        file "reverse/{filename}";\n'
                    f'}};\n\n')

if __name__ == '__main__':
    host_dict = get_zones(host_dict, zones_dir)
    host_dict = get_csv(host_dict)

    make_zones(host_dict)
    make_reverse_conf(conf_dir, zones_dir)