import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys


def pa(lb, arr):
    sys.stdout.write(lb+': ')
    sys.stdout.write('[')
    for a in arr:
        sys.stdout.write('{:0.2E} '.format(a))
    print(']')
    
    
def pi(lb, *ints):
    sys.stdout.write(lb+': ')
    for i in ints:        
        sys.stdout.write('{:0.2E} '.format(i))
    print()


def weighted_avg(arr):
    weights = np.hamming(len(arr))
    return np.sum(np.multiply(np.array(arr), weights/np.sum(weights)))

def get_gauss(sigma):
    def gaussian(x_j, i, j):
        return x_j / (np.sqrt(2*np.pi*sigma**2)) *\
                    np.exp(-(i - j)**2/(2*sigma**2))
    return gaussian

def get_d_gauss_di(sigma):
    def d_gauss_di(x_j, i, j):
        return - x_j / (np.sqrt(2*np.pi*sigma**6)) *\
                np.exp(-(i - j)**2/(2*sigma**2)) *\
                (i - j)
    return d_gauss_di

def get_d_gauss_dj(sigma):
    def d_gauss_dj(x_j, i, j):
        return - x_j / (np.sqrt(2*np.pi*sigma**6)) *\
                np.exp(-(i - j)**2/(2*sigma**2)) *\
                (i - j)
    return d_gauss_dj

def abs_exp(x_j, i, j):
    return x_j * np.exp(-np.abs(i - j))

def d_abs_exp(x_j, i, j):
    return -x_j * np.exp(-np.abs(i - j)) * (i - j) / np.abs(i - j)

def sim_read(A, i, filt, use_log=False):
    if (use_log):
        print(max(A)*0.000001)
        A = np.log(A+max(A)*0.000001)
    y = np.zeros(len(i))
    for j in range(len(A)):
        y += filt(A[j], i, j)
    return y


def dyidi(A, i, d_filt = get_d_gauss_di(1.0), use_log=False):
    if (use_log):
        A = np.log(A + max(A)*0.000001)
    if (getattr(i, "len", False)):
        dy = np.zeros(len(i))
        for j in range(len(A)):
            dy += d_filt(A[j], i, j)
        return dy
#     if (type(i) == int):
        
    else:
        dy = 0.0
        for j in range(len(A)):
            dy += d_filt(A[j], i, j)
        return dy

 
def dread(A, ind, didxin, v=False):
    samples = [-1, 1]
    N = len(A)

    dydis = []
    for i, s in enumerate(samples):
        if (didxin != 0):
            # ASSUMPTION: wrap mem if beyond bounds (specific to crc)
            xs = int(ind + s*didxin)
            # valid index in 0:N
            modxs = xs % N

            # valid dind within -N:N
            boundedxs = modxs
            if (xs < 0):
                boundedxs -= N

            dydis.append((int(A[modxs]) - int(A[ind]))/(s*boundedxs))
        else:
            dydis.append(0)

    dydi = weighted_avg(dydis)

    return dydi


    
def dreadxin(A, ind, didxin, v=False):
    samples = [-1, 1]
    N = len(A)
    
    
    dydis = []
    for i, s in enumerate(samples):
        if (didxin != 0):
            # ASSUMPTION: wrap mem if beyond bounds (specific to crc)
            xs = int(ind + s*didxin)
            xs = xs % N

            # FIX: need to set s*didxin so derivative is wrt input not xin
            # currently inconsistent with other diff ops
            dydis.append((int(A[xs]) - int(A[ind]))/s)
        else:
            dydis.append(0)

    dydi = weighted_avg(dydis)

    # pi('DREAD: dydi didxin', dydi, didxin)

    return dydi


def dreadxin_sim(A, ind, xin_bytes, v=False):
    def sim_crc_read2(byte_arr):
        value = 0xffffffff
        for b in byte_arr:
            v1 = b
            v2 = v1 ^ value
            v3 = v2 & 0xff
            v4 = A[v3]
            v5 = value >> 8
            value = v4 ^ v5
    #         value = table[(ord(ch) ^ value) & 0xff] ^ (value >> 8)

        return v3, v4

    # sim with xin0-1, xin0+1
    xins1 = int.to_bytes(int.from_bytes(xin_bytes, 'big') - 256, 2, 'big')
    xins2 = int.to_bytes(int.from_bytes(xin_bytes, 'big') + 256, 2, 'big')

    simx1, simy1 = sim_crc_read2(xins1)
    simx2, simy2 = sim_crc_read2(xins2)
    
    if v:
        pi('sr1', simx1, simy1)
        pi('sr2', simx2, simy2)

    x = ind
    y = A[ind]

    dydi1 = (int(simy1) - int(y))/-1
    dydi2 = (int(simy2) - int(y))/1

    dydi = (dydi1 + dydi2) / 2

    if v:
        print()

    return dydi


def viz_read(A, filt, d_filt):
    plt.figure(figsize=(16,4))
    plt.subplot(1,2,1)
    plt.bar(np.arange(len(A)), np.log(A+max(A)*0.000001), width=0.25)
    plt.axhline(linewidth=1,color='gray')
    plt.title('Memory & Approximation:')
    
    all_i = np.linspace(0, len(A)-1, len(A)*25)
    y = sim_read(A, all_i, filt)
    plt.plot(all_i, y, 'r', linewidth=2)
    plt.xlabel('memory index')
    
    plt.subplot(1,2,2)
    plt.plot(all_i, dyidi(A, all_i, d_filt),
            linewidth=2)
    plt.axhline(linewidth=1,color='gray')
    plt.title('dydi')
    plt.xlabel('i')
    plt.ylabel('dydi')
    

def get_d_gauss_dj(sigma):
    def d_gauss_dj(x_j, i, j):
        return x_j / (np.sqrt(2*np.pi*sigma**6)) *\
                np.exp(-(i - j)**2/(2*sigma**2)) *\
                (i - j)
    return d_gauss_dj

def sim_write(x_j, i, j, filt):
    return filt(x_j, i, j)


def dyidj(x_j, i, j, d_filt):
    return d_filt(np.log(x_j), i, j)
#     return x_j / (np.sqrt(2*np.pi*sigma**6)) *\
#                 np.exp(-(i - j)**2/(2*sigma**2)) *\
#                 (i - j)

def viz_write(A, i, j, filt, d_filt):
    
    plt.figure(figsize=(16,4))
    plt.subplot(1,2,1)
    plt.bar(np.arange(len(A)), A, width=0.25)
    plt.axhline(linewidth=1,color='gray')
    plt.title('Memory & Approximation:')
    
    all_j = np.linspace(0, len(A)-1, len(A)*25)
    y = sim_write(A[j], i, all_j, filt)
    plt.plot(all_j, y, 'r', linewidth=2)
    plt.xlabel('memory index')
    
    plt.subplot(1,2,2)
    plt.plot(all_j, dyidj(A[j], i, all_j, d_filt),
            linewidth=2)
    plt.axhline(linewidth=1,color='gray')
    plt.title('dyidj')
    plt.xlabel('j')
    plt.ylabel('dyidj')
