import pickle
import os
import numpy as np
import glob
import random
import math
import time
import subprocess
import socket
import ipdb

HOST='127.0.0.1'
PORT=12012
round_cnt = 0
call=subprocess.call
loc = {}


if os.path.isdir("./crashes/") == False:
    os.makedirs('./crashes')


def run_taint(file_name, loc):
    call(['/home/vagrant/vuzzer/pin/pin', '-follow_execv', '-t','/home/vagrant/vuzzer/obj-ia32/dtracker.so', '-filename' ,file_name,'-stdout' ,'0', '-maxoff', '1024', '--', '/vagrant/miniunz','-o', file_name])
    print(file_name)
    tmp = {}
    with open('cmp.out','r') as f:
        lines = f.read().splitlines()
        for line in lines:
            tokens=line.split(' ')
            addr = tokens[3]
            for token in tokens:
                if token != '':
                    if token[0] == '{':
                        for num in token[1:-1].split(','):
                            if num != '':
                                if addr not in tmp:
                                    tmp[addr]=[int(num)]
                                elif int(num) not in tmp[addr]:
                                    tmp[addr].append(int(num))
    val = []
    for i in tmp.values():
        for j in i:
            val.append(j)
    for ele in val:
        if ele not in loc:
            loc[ele] = 1
        else:
            loc[ele] = loc[ele] + 1


def gen_taint():
    edge_num = 500
    tmp_list = []
    # select seeds
    print("#######debug" + str(round_cnt))
    # seed_list = glob.glob("/home/vagrant/vuzzer/seeds/*")
    seed_list = glob.glob("./seeds/*")
    if(round_cnt == 0):
        new_seed_list = seed_list
    else:
        new_seed_list = glob.glob("./seeds/id_"+str(round_cnt-1)+"_*")
        # new_seed_list = glob.glob("/home/vagrant/vuzzer/seeds/id_"+str(round_cnt-1)+"_*")

    #for file_name in new_seed_list:
    #    run_taint(file_name, loc)
    #ipdb.set_trace()
    #idx_list = sorted(loc.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    idx_list = pickle.load(open('./pdf_taint','r'))
    idx_list = [ele[0] for ele in idx_list[:1024]]
    #ipdb.set_trace()

    if len(new_seed_list) < edge_num:
        rand_seed1 = [new_seed_list[i] for i in np.random.choice(len(new_seed_list),edge_num, replace=True)]
    else:
        rand_seed1 = [new_seed_list[i] for i in np.random.choice(len(new_seed_list),edge_num, replace=False)]
    if len(new_seed_list) < edge_num:
        rand_seed2 = [seed_list[i] for i in np.random.choice(len(seed_list),edge_num, replace=True)]
    else:
        rand_seed2 = [seed_list[i] for i in np.random.choice(len(seed_list),edge_num, replace=False)]

    with open('taint_info_p','w') as f:
        for idxx in range(edge_num):
            #fl = rand_seed[idxx*2:idxx*2+2]
            fl = [rand_seed1[idxx], rand_seed2[idxx]]
            for fl_ele in fl:
                ele0 = [str(el) for el in idx_list]
                ele1 = np.random.choice([1,-1],len(idx_list), replace=True)
                ele1 = [str(el) for el in ele1]
                ele2 = fl_ele
                f.write(",".join(ele0)+'|'+",".join(ele1)+'|'+ele2+"\n")

def gen_grad(data):
    global round_cnt
    gen_taint(data)
    round_cnt = round_cnt+1

def setup_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected by neuzz execution moduel'+str(addr))
    gen_grad('train')
    conn.sendall("start")
    while True:
        data = conn.recv(1024)
        if not data: break
        else:
            gen_grad(data)
            conn.sendall("start")
    conn.close()

gen_taint()
#setup_server()
