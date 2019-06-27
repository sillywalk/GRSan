import binascii
import numpy as np
import binascii
from collections import defaultdict
from diff_ops import pi

import diff_ops as do
import mem_ops as mo

from importlib import reload

reload(mo)
reload(do)

# crc32 imp from https://stackoverflow.com/questions/41564890/crc32-calculation-in-python-without-using-libraries


poly = 0xEDB88320

# table = array('L')
table = np.zeros(256, dtype=np.uint32)
for byte, i in enumerate(range(256)):
    crc = 0
    for bit in range(8):
        if (byte ^ crc) & 1:
            crc = (crc >> 1) ^ poly
        else:
            crc >>= 1
        byte >>= 1
    table[i] = crc
#     table.append(crc)

def crc_table():
    poly = 0xEDB88320

    # table = array('L')
    table = np.zeros(256, dtype=np.uint32)
    for byte, i in enumerate(range(256)):
        crc = 0
        for bit in range(8):
            if (byte ^ crc) & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            byte >>= 1
        table[i] = crc
    return table

def crc32(string):
    value = 0xffffffff
    for ch in string:
        v1 = ord(ch)
        v2 = v1 ^ value
        v3 = v2 & 0xff
        v4 = table[v3]
        v5 = value >> 8
        value = v4 ^ v5
#         value = table[(ord(ch) ^ value) & 0xff] ^ (value >> 8)

    return -1 - value

def crc32_byte_unsigned_ref(x_in):
    value = 0xffffffff

    v1 = x_in
    v2 = v1 ^ value
    v3 = v2 & 0xff
    v4 = table[v3]
    v5 = value >> 8
    
    value = v4 ^ v5

    return value

def crc32_byte(x_in, sigma = 0.6, v=False):
    value = 0xffffffff
#     for ch in string:
#     v1 = ord(ch)
    v1 = x_in
    v2 = v1 ^ value

    v3 = v2 & 0xff
    dv3dv2, _ = do.dand(v2, 0xff)
    v4 = table[v3]
    dv4dv3 = mo.dyidi(table, v3, d_filt=mo.get_d_gauss_di(sigma))
    v5 = value >> 8
    dv5dval = 1/2**8
    
    value = v4 ^ v5
    dvaldv4, dvaldv5 = do.dxor(value, v4, v5, dv4dv3*dv3dv2*dv2dv1, dv5dval)
    dvaldv4 = 1.0 # corrected for large scale behavior, locally is -1 but globally is 1

    return -1 - value, -dvaldv4*dv4dv3*dv3dv2*dv2dv1

def crc32_bytes_ref(byte_arr):
    value = 0xffffffff
#     for ch in string:
#     v1 = ord(ch)
    for b in byte_arr:
        v1 = b
        v2 = v1 ^ value
        v3 = v2 & 0xff
        v4 = table[v3]
        v5 = value >> 8
        value = v4 ^ v5
#         value = table[(ord(ch) ^ value) & 0xff] ^ (value >> 8)

    return -1 - value

# OLD USING FULL (incorrect) chaining
poly = 0xEDB88320

table = np.zeros(256, dtype=np.uint32)
for byte, i in enumerate(range(256)):
    crc = 0
    for bit in range(8):
        if (byte ^ crc) & 1:
            crc = (crc >> 1) ^ poly
        else:
            crc >>= 1
        byte >>= 1
    table[i] = crc

def crc32_bytes_x_mem_chaining(x_bytes, sigma = 0.6, v=False, sim=False):
    value = np.uint32(0xffffffff)
    
    dv2dv1s = []
    dv2dvals = []
    dv3dv2s = []
    dv4dv3s = []
    dv5dvals = []
    dvaldv4s = []
    dvaldv5s = []
    dvaldxin0s = []
    
    v1s = []
    v2s = []
    v3s = []
    v4s = []
    v5s = []
    vals = []
    
    rec = defaultdict(list)
    
    dvaldxin0 = 0 # initially val not effected by x_in
    dvaldxin0s.append(dvaldxin0)
    
    input_len = len(x_bytes)
    for i, xin in enumerate(x_bytes):
        if v:
            print()
            print('i xin', i, xin)
        
        # input
        v1 = np.uint32(xin)
        dv1dxin0 = int(i==0)
        v1s.append(v1)

        
        # xor 1
        v2 = v1 ^ value
        v2s.append(v2)
        dv2dv1, dv2dval = do.dxor(v2, v1, value, dv1dxin0, dvaldxin0)
        dv2dv1s.append(dv2dv1)
        dv2dvals.append(dv2dval)
        if v:
            pi('xor1: v1 val dv1dxin0 dvaldxin0', v1, value, dv1dxin0, dvaldxin0)
            pi('xor1 out: v2 dv2dv1 dv2dval',v2, dv2dv1, dv2dval)
            print()

        
        # and 1
        v3 = v2 & 0xff
        v3s.append(v3)
        dv3dv2, _ = do.dand(v2, 0xff)
        dv3dv2s.append(dv3dv2)
        if v:
            pi('and1: v2', v2)
            pi('and1 out: v3 dv3dv2',v3, dv3dv2)
            print()
        
        # read 1
        v4 = table[v3]
        v4s.append(v4)
#         dv4dv3 = mo.dyidi(table, v3, d_filt=mo.get_d_gauss_di(sigma))
        if v:
            pi('dread in', dv3dv2*dv2dv1*dv1dxin0 +
                                            dv3dv2*dv2dval*dvaldxin0)
        dv4dxin0 = mo.dreadxin(table, v3, dv3dv2*dv2dv1*dv1dxin0 +
                                        dv3dv2*dv2dval*dvaldxin0, v=v)
        
        if (i==1 and sim):
            dv4dxin0 = mo.dreadxin_sim(table, v3, x_bytes, v=v)
            if v:
                pi('read sim ', dv4dxin0)
        # TEST try setting to 0 if 2nd round
#         if (i>0):
#             dv4dv3 = 0
        
        dv4dv3s.append(dv4dxin0)
        
        if v:
            pi('read1: v3, dv3dv2*dv2dv1*dv1dxin0 + dv3dv2*dv2dval*dvaldxin0',
                    v3, dv3dv2*dv2dv1*dv1dxin0 + dv3dv2*dv2dval*dvaldxin0)
            pi('read1 out: v4 dv4dxin', v4, dv4dxin0)
            print()
        
        # shift 1
        v5 = np.uint32(value >> 8)
        v5s.append(v5)
        dv5dval = 1/2**8
        dv5dvals.append(dv5dval)
        
        if v:
            pi('shift1: val', value)
            pi('shift1 out: v5 dv5dval', v5, dv5dval)
            print()
        
        # xor 2
        value = v4 ^ v5
        vals.append(value)
        dvaldv4, dvaldv5 = do.dxor(value, v4, v5, 
                                   dv4dxin0, 
                                   dv5dval*dvaldxin0, v)
        dvaldv4s.append(dvaldv4)
        dvaldv5s.append(dvaldv5)
        
        if v:
            pi('xor2: v4 v5 ', v4, v5, dv4dxin0,
              dv5dval*dvaldxin0)
            pi('xor2 out: dvaldv4 dvaldv5', dvaldv4, dvaldv5)
            print()
        
        # calc dvaldxin0
        dvaldxin0 = dvaldv4*dv4dxin0 +\
                    dvaldv5*dv5dval*dvaldxin0
        dvaldxin0s.append(dvaldxin0)
        
        if v:
            pi('dvaldxin0 dvaldv4*dv4dxin0 dvaldv5*dv5dval*dvaldxin0s[i]', dvaldv4*dv4dxin0,
              dvaldv5*dv5dval*dvaldxin0s[i])
            pi('dvaldxin0 dvaldv4, dv4dxin0', dvaldv4, dv4dxin0)
            pi('dvaldxin0 dvaldv5, dv5dval, dvaldxin0s[i]', dvaldv5, dv5dval, dvaldxin0s[i])
            pi('dvaldxin0', dvaldxin0)
        

    
    
    return -1 - value, dvaldxin0s, v1s, v2s, v3s, v4s, v5s, vals,\
            dv2dv1s,dv2dvals,dv3dv2s,dv4dv3s,dv5dvals,\
            dvaldv4s,dvaldv5s,dvaldxin0s#-dvaldv4*dv4dv3*dv3dv2*dv2dv1

    
def crc32_bytes_full_mem_chaining(x_bytes, v=False):
    value = np.uint32(0xffffffff)
    
    dv2dv1s = []
    dv2dvals = []
    dv3dv2s = []
    dv4dv3s = []
    dv5dvals = []
    dvaldv4s = []
    dvaldv5s = []
    dvaldxin0s = []
    
    v1s = []
    v2s = []
    v3s = []
    v4s = []
    v5s = []
    vals = []
    
    rec = defaultdict(list)
    
    dvaldxin0 = 0 # initially val not effected by x_in
    dvaldxin0s.append(dvaldxin0)
    
    input_len = len(x_bytes)
    for i, xin in enumerate(x_bytes):
        if v:
            print()
            print('i xin', i, xin)
        
        # input
        v1 = np.uint32(xin)
        dv1dxin0 = int(i==0)
        v1s.append(v1)

        
        # xor 1
        v2 = v1 ^ value
        v2s.append(v2)
        dv2dv1, dv2dval = do.dxor(v2, v1, value, dv1dxin0, dvaldxin0)
        dv2dv1s.append(dv2dv1)
        dv2dvals.append(dv2dval)
        if v:
            pi('xor1: v1 val dv1dxin0 dvaldxin0', v1, value, dv1dxin0, dvaldxin0)
            pi('xor1 out: v2 dv2dv1 dv2dval',v2, dv2dv1, dv2dval)
            print()

        
        # and 1
        v3 = v2 & 0xff
        v3s.append(v3)
        dv3dv2, _ = do.dand(v2, 0xff)
        dv3dv2s.append(dv3dv2)
        if v:
            pi('and1: v2', v2)
            pi('and1 out: v3 dv3dv2',v3, dv3dv2)
            print()
        
        # read 1
        v4 = table[v3]
        v4s.append(v4)
#         dv4dv3 = mo.dyidi(table, v3, d_filt=mo.get_d_gauss_di(sigma))
        if v:
            pi('dread in', dv3dv2*dv2dv1*dv1dxin0 +
                                            dv3dv2*dv2dval*dvaldxin0)
        dv4dv3 = mo.dread(table, v3, dv3dv2*dv2dv1*dv1dxin0 +
                                        dv3dv2*dv2dval*dvaldxin0)
        # TEST try setting to 0 if 2nd round
#         if (i>0):
#             dv4dv3 = 0
        
        dv4dv3s.append(dv4dv3)
        
        if v:
            pi('read1: v3', v3)
            pi('read1 out: v4 dv4dv3', v4, dv4dv3)
            print()
        
        # shift 1
        v5 = np.uint32(value >> 8)
        v5s.append(v5)
        dv5dval = 1/2**8
        dv5dvals.append(dv5dval)
        
        if v:
            pi('shift1: val', value)
            pi('shift1 out: v5 dv5dval', v5, dv5dval)
            print()
        
        # xor 2
        value = v4 ^ v5
        vals.append(value)
        dvaldv4, dvaldv5 = do.dxor(value, v4, v5, 
                                   dv4dv3*dv3dv2*dv2dv1*dv1dxin0 +\
                                           dv4dv3*dv3dv2*dv2dval*dvaldxin0, 
                                   dv5dval*dvaldxin0, v=False)
        dvaldv4s.append(dvaldv4)
        dvaldv5s.append(dvaldv5)
        
        if v:
            pi('xor2: v4 v5 ', v4, v5, dv4dv3*dv3dv2*dv2dv1*dv1dxin0 +\
                                           dv4dv3*dv3dv2*dv2dval*dvaldxin0,
              dv5dval*dvaldxin0)
            pi('xor2 out: dvaldv4 dvaldv5', dvaldv4, dvaldv5)
            print()
        
        # calc dvaldxin0
        dvaldxin0 = dv4dv3*dv3dv2*dv2dv1*dv1dxin0 +\
                dv4dv3*dv3dv2*dv2dval*dvaldxin0 +\
                    dvaldv5*dv5dval*dvaldxin0
        dvaldxin0s.append(dvaldxin0)
        
        if v:
            print('dvaldxin0 = dv4dv3*dv3dv2*dv2dv1*dv1dxin0 + dv4dv3*dv3dv2*dv2dval*dvaldxin0 + dvaldv5*dv5dval*dvaldxin0')
            pi('dvaldxin0 parts', dv4dv3*dv3dv2*dv2dv1*dv1dxin0,
                    dv4dv3*dv3dv2*dv2dval*dvaldxin0,
                    dvaldv5*dv5dval*dvaldxin0s[i])
            pi('dvaldxin0 part dv4dv3,dv3dv2,dv2dv1,dv1dxin0',dv4dv3,dv3dv2,dv2dv1,dv1dxin0)
            pi('dvaldxin0 part dv4dv3,dv3dv2,dv2dval,dvaldxin0',dv4dv3,dv3dv2,dv2dval,dvaldxin0)
            pi('dvaldxin0 part dvaldv5 dv5dval dvaldxin0s', dvaldv5, dv5dval, dvaldxin0s[i])
            pi('dvaldxin0', dvaldxin0)
        

    
    
    return -1 - value, dvaldxin0s, v1s, v2s, v3s, v4s, v5s, vals,\
            dv2dv1s,dv2dvals,dv3dv2s,dv4dv3s,dv5dvals,\
            dvaldv4s,dvaldv5s,dvaldxin0s#-dvaldv4*dv4dv3*dv3dv2*dv2dv1


def crc32_bytes_dird(x_bytes, v=False):
    value = np.uint32(0xffffffff)
    
    dv1dins = []
    dv2dins = []
    dv3dins = []
    dv4dins = []
    dv5dins = []
    dvaldins = []
    
    v1s = []
    v2s = []
    v3s = []
    v4s = []
    v5s = []
    vals = []
    
    rec = defaultdict(list)
    
    dvaldin = (0, 0) # initially val not effected by x_in
    # dvaldins.append(dvaldin)
    
    input_len = len(x_bytes)
    for i, xin in enumerate(x_bytes):
        if v:
            print()
            print('i xin', i, xin)
        
        # input
        v1 = np.uint32(xin)
        dv1dxin0 = (int(i==0), int(i==0))
        v1s.append(v1)
        dv1dins.append(dv1dxin0)

        
        # xor 1
        v2 = v1 ^ value
        v2s.append(v2)
        dv2din = do.dirdxorin(v2, v1, value, dv1dxin0, dvaldin)
        dv2dins.append(dv2din)
        if v:
            pi('xor1: v1 val dv1dxin0 dvaldin', v1, value, dv1dxin0[0], dv1dxin0[1], dvaldin[0], dvaldin[1])
            pi('xor1 out: v2 dv2dv1',v2, dv2din[0], dv2din[1])
            print()

        
        # and 1
        v3 = v2 & 0xff
        v3s.append(v3)
        dv3din = do.dirdandin(v3, v2, 0xff, dv2din, (0, 0))
        dv3dins.append(dv3din)
        if v:
            pi('and1: v2', v2)
            pi('and1 out: v3 dv3din',v3, dv3din[0], dv3din[1])
            print()
        
        # read 1
        v4 = table[v3]
        v4s.append(v4)
        dv4din = do.dirdreadin(table, v3, dv3din, v=v)
        dv4dins.append(dv4din)
        
        if v:
            # pi('read1: v3, dv3din',
                    # v3, dv3din)
            pi('read1 out: v4 dv4dxin', v4, dv4din[0], dv4din[1])
            print()
        
        # shift 1
        v5 = np.uint32(value >> 8)
        v5s.append(v5)
        dv5din = ((1/2**8) * dvaldin[0], (1/2**8) * dvaldin[1])
        dv5dins.append(dv5din)
        
        if v:
            pi('shift1: val', value)
            pi('shift1 out: v5 dv5din', v5, dv5din[0], dv5din[1])
            print()
        
        # xor 2
        value = v4 ^ v5
        vals.append(value)
        dvaldin = do.dirdxorin(value, v4, v5, 
                                   dv4din, 
                                   dv5din, v)
        
        if v:
            # pi('xor2: v4 v5 ', v4, v5, dv4din,
              # dv5din)
            # pi('xor2 out: dvaldin', dvaldin[0], dvalin[1])
            print()
        
        # calc dvaldin
        dvaldins.append(dvaldin)
        
        if v:
            pass
            # pi('dvaldin', dvaldin)
        

    
    
    return -1 - value, dvaldins, (v1s[0], v2s[0], v3s[0], v4s[0], v5s[0], vals[0], v1s[1], v2s[1], v3s[1], v4s[1], v5s[1], vals[1]),\
            (dv1dins[0], dv2dins[0], dv3dins[0], dv4dins[0], dv5dins[0], dvaldins[0], dv1dins[1], dv2dins[1], dv3dins[1], dv4dins[1], dv5dins[1], dvaldins[1])


def crc32_bytes_dird_seedd(x_bytes, dxins, v=False):
    
    vs = []
    dvs = []
        
    value = np.uint32(0xffffffff)
    dval = (0, 0) # initially val not effected by x_in
    
    for i, (xin, dxin) in enumerate(zip(x_bytes, dxins)):
        if v:
            print()
            print('i xin', i, xin, dxin)
        
        # input
        v1 = np.uint32(xin)
        vs.append(v1)
        dvs.append(dxin)

        
        # xor 1
        v2 = v1 ^ value
        vs.append(v2)
        dv2 = do.dirdxorin(v2, v1, value, dxin, dval)
        dvs.append(dv2)
        if v:
            pi('xor1: v1 val dv1dxin0 dval', v1, value, dxin[0], dxin[1], dval[0], dval[1])
            pi('xor1 out: v2 dv2dv1',v2, dv2[0], dv2[1])
            print()

        
        # and 1
        v3 = v2 & 0xff
        vs.append(v3)
        dv3din = do.dirdandin(v3, v2, 0xff, dv2, (0, 0))
        dvs.append(dv3din)
        if v:
            pi('and1: v2', v2)
            pi('and1 out: v3 dv3din',v3, dv3din[0], dv3din[1])
            print()
        
        # read 1
        v4 = table[v3]
        vs.append(v4)
        dv4din = do.dirdreadin(table, v3, dv3din, v=v)
        dvs.append(dv4din)

        if v:
            # pi('read1: v3, dv3din',
                    # v3, dv3din)
            pi('read1 out: v4 dv4dxin', v4, dv4din[0], dv4din[1])
            print()
        
        # shift 1
        v5 = np.uint32(value >> 8)
        vs.append(v5)
        dv5din = ((1/2**8) * dval[0], (1/2**8) * dval[1])
        dvs.append(dv5din)
        
        if v:
            pi('shift1: val', value)
            pi('shift1 out: v5 dv5din', v5, dv5din[0], dv5din[1])
            print()
        
        # xor 2
        value = v4 ^ v5
        vs.append(value)
        dval = do.dirdxorin(value, v4, v5, 
                                   dv4din, 
                                   dv5din, v)
        
        if v:
            # pi('xor2: v4 v5 ', v4, v5, dv4din,
              # dv5din)
            # pi('xor2 out: dval', dval[0], dvalin[1])
            print()
        
        # calc dval
        dvs.append(dval)
        
        if v:
            pass
     
    return -1 - value, -np.array(dval), vs, dvs


def crc32_multibits(xs, dxs, v=False):
    vs = []
    dvs = []
    
    value = 0xffffffff
    dvaldxin = np.zeros(32)
    
    
    for x, dx in zip(xs, dxs):
        v1 = x
        vs.append(v1)
        dvs.append(dx)

        v2 = v1 ^ value
        dv2dxin = do.dxorbin(v2, v1, value, dx, dvaldxin)
        vs.append(v2)
        dvs.append(dv2dxin)

        v3 = v2 & 0xff
        dv3dv2, _ = do.dandb(v2, 0xff)
        dv3dxin = do.bmult(dv3dv2, dv2dxin)
        vs.append(v3)
        dvs.append(dv3dxin)

        v4 = table[v3]
        dv4dv3 = do.dreadb(table, v3) 
        dv4dxin = do.bmult(dv4dv3, dv3dxin)
        vs.append(v4)
        dvs.append(dv4dxin)

        if v:
            if dv3dxin.ndim > 1:
                print('dv4')
                print(dv3dxin[31, :])
                print(dv4dv3[31,:])
                print(dv4dxin[31,:])
                print()
                print()

        v5 = value >> 8
        dv5dx = np.zeros(dvaldxin.shape)
        if (dv5dx.ndim == 1):
            dv5dx[8:] = dvaldxin[:-8]
        else:
            dv5dx[8:, :] = dvaldxin[:-8, :]

        value = v4 ^ v5
        dvaldxin = do.dxorbin(value, v4, v5, dv4dxin, dv5dx)
        vs.append(value)
        dvs.append(dvaldxin)

    return -1 - value, -dvaldxin, vs, dvs


if __name__=='__main__':
    # crcr, dx00r = crc32_byte(10)
    crc, dcrc, vs, dvs = crc32_bytes_dird_seedd(b'\x0A\x08', [(0,0), (1,1)], v=True)
    refcrc = binascii.crc32(b'\x0A\x08')

    print()
    print('ref', refcrc -0x100000000 , type(refcrc))
    print('out', crc, type(crc))
    # print('dxref', dx00r, 'dx', dxs)
    do.pi('dcrc', dcrc[0], dcrc[1])



    
