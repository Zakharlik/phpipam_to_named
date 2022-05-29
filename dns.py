#!/usr/bin/python3
import os
import re

host_dict = {}

data_dir = 'data'
zones_dir = 'zones'
out_dir = 'out'

def push_dict(host_dict, net, host, name):
    if host_dict.get(net) != None:
        host_dict[net].append((host, name))
    else:
        host_dict[net] = [(host, name)]
    return host_dict


def get_reverse_zones(host_dict, file):
    net = re.search(r'\\(\S*)\.zone', file).group(1)
    with open(file,'r') as f:
        for line in f:
            if re.search('^\d',line):
                host, _, _, name = line.split()
                host_dict = push_dict(host_dict, net, host, name)
    print(host_dict)
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
    print(host_dict)
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
    with open('data/allip.csv', 'r', encoding='cp1251') as r:
        for line in r:
            net, host, _, _, name, *_ = line.split(';')
            host_dict = push_dict(host_dict, net, host, name)
    return host_dict


def make_zones(host_dict):
    pass

if __name__ == '__main__':
    host_dict = get_zones(host_dict, zones_dir)
    host_dict = get_csv(host_dict)

    make_zones(host_dict)
    print(host_dict)
