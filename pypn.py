#!/usr/bin/python

import argparse
import os
import pickle

config_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pypn.cfg")

def load_config():
    try:
        f = open(config_location, "r+")
        ret = pickle.load(f)
        f.close()
        return ret
    except:
        return {}

def save_config(cfg):
    f = open(config_location, "w+")
    pickle.dump(cfg, f)
    f.close()

def merge_config_into_args(args, cfg):
    for k in cfg:
        if not hasattr(args, k) or eval("args." + k) is None:
            setattr(args, k, cfg[k])

    return args

def create_config_from_args(args):
    cfg = {}

    for attr in dir(args):
        if not attr.startswith("_"):
            cfg[attr] = getattr(args, attr)

    return cfg

def check_for(args, field):
    if not hasattr(args, field) or getattr(args, field) is None:
        print "Must set: {field}".format(field=field)
        exit()

def check_for_musts(args):
    check_for(args, "cert")
    check_for(args, "token")

###############################################

def handle_regular(args):
    check_for_musts(args)
    check_for(args, "msg")

    os.system("apn push {token} -c {cert} -e development -m {msg}".format(token=args.token, cert=args.cert, msg=args.msg))

def handle_silent(args):
    check_for_musts(args)

    os.system("apn push {token} -c {cert} -e development -P".format(token=args.token, cert=args.cert) + """ '{"aps" : {"content-available": 1}}'""")

###############################################

push_types = {"regular": handle_regular, 
              "silent": handle_silent}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sends push notifications')
    parser.add_argument("type", type=str, choices=push_types.keys(), help="Type of push")
    parser.add_argument("--msg", "-m", type=str, help="Message to send")
    parser.add_argument("--cert", "-c", type=str, help="Certificate to use (abs path)")
    parser.add_argument("--token", "-t", type=str, help="Token to use")

    args = parser.parse_args()
    args = merge_config_into_args(args, load_config())

    save_config(create_config_from_args(args))

    push_types[args.type](args)