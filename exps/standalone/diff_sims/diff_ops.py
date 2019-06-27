import numpy as np
import sys

def int_to_bits(x):
    int_bits = np.zeros(32, dtype=np.float32)
    for i in range(32):
        int_bits[31-i] = x & 0x1
        x = x >> 1;
        
    return int_bits

def bits_to_int(x_bits):
    x = int(0)
    for i in range(32):
        x += x_bits[31-i]<<i
    return x

def itob(x):
    return int_to_bits(x)

def btoi(x):
    return bits_to_int(x)

def bit_noise():
    return np.random.uniform(-0.3, 0.3, (32))

def pd(y):
    y = y.astype(np.int64)
    dy = np.zeros(y.shape)
    dy1 = y[1:] - y[:-1]
    dy2 = (dy1[:-1] + dy1[1:])/2
    dy[1:-1] = dy2
    dy[0] = dy1[0]
    dy[-1] = dy1[-1]
    return dy


def pa(lb, arr):
    sys.stdout.write(lb+': ')
    sys.stdout.write('[')
    for a in arr:
        sys.stdout.write('{:0.2E} '.format(a))
    print(']')
    

def pad(lb, arr):
    sys.stdout.write(lb+': ')
    sys.stdout.write('[')
    for a in arr:
        sys.stdout.write('({:0.2E}, {:0.2E}), '.format(a[0], a[1]))
    print(']')
    
    
def pi(lb, *ints):
    sys.stdout.write(lb+': ')
    for i in ints:        
        sys.stdout.write('{:0.2E} '.format(i))
    print()

class Mod2():
    
    def __init__(self):
        pass
    
    def forward(self, x):
        self.x = x%2
        return self.x

    
    def backward(self, grad):
#         x1_bits = int_to_bits(self.x)

        grad_x1 = 1/2 * np.pi * np.sin(np.pi * 
                                       (self.x + np.random.uniform(-0.3, 0.3))) * grad
#         grad_x2 = grad_x1

#         return (grad_x1, grad_x2)
        return grad_x1
    

class ShiftRight():
    
    def __init__(self, shift):
        self.shift = shift
        
    def forward(self, x):
        return x>>self.shift
    
    def backward(self, grad):
        # grad is float
        return 1/2**self.shift * grad
    
def dbtoi(grad):
    grad_out = np.zeros(32, dtype=np.float32)
        
    for i in range(32):
        grad_out[31-i] = 2.0**i * grad
    return grad_out
        

class FromBits():
    
    def __init__(self):
        pass
    
    def forward(self, xbits):
        # xbits is int[32]
#         x = 0
#         for i in range(32):
#             x += xbits[i]<<i
#         return x

        # xbits is int, only handle this for backprop
        return xbits
    
    def backward(self, grad):
        # grad is float
        grad_out = np.zeros(32, dtype=np.float32)
        
        for i in range(32):
            grad_out[31-i] = 2.0**i * grad
        return grad_out

def ditob(grad):
    # IGNORING MODULO APPROXIMATION HERE!!!!
    
    grad_out = 0
    for i in range(32):
#         grad_out += 1/2**i * self.mod[i].backward(grad[31-i])
        grad_out += 1/2**i * grad[31-i]
    return grad_out

class ToBits():
    
    def __init__(self):
        self.mod = []
        for i in range(32):
            self.mod.append(Mod2())
    
    def forward(self, x):
        int_bits = np.zeros(32, dtype=np.float32)
        xshift = np.copy(x)
        for i in range(32):
            int_bits[31-i] = self.mod[i].forward(xshift)
            xshift = xshift >> 1;

#         return int_bits
        # only approx on backward, id on forward
        return x
    
    def backward(self, grad):
        # grad is float[32]
#         grad_out = np.zeros(32)
#         for i in range(32):
#             grad_out[31-i] = 1/2**i * self.mod[i].backward(grad[31-i])
#         return grad_out

        grad_out = 0
        for i in range(32):
            grad_out += 1/2**i * self.mod[i].backward(grad[31-i])
#         print('mod', self.mod[i].backward(grad[31-i]))
#         print('tobit back ', grad_out)
        return grad_out


def dirdreadin(A, ind, didin, v=False):
    samples = [-1, 1]
    N = len(A)
    
    
    dydi = []
    for i, s in enumerate(samples):
        # ASSUMPTION: wrap mem if beyond bounds (specific to crc)
        xs = int(ind + s*didin[i])
        xs = xs % N

        dydi.append((int(A[xs]) - int(A[ind]))/s)

    # pi('DREAD: dydi didxin', dydi, didxin)

    return dydi


def dreadb(A, x, v=False):
    N = len(A)

    xb = itob(x)
    dydx = np.zeros((32, 32), dtype=np.int)

    for i in range(32):
        if (x & 1<<i): # bit is 1
            s = -1
            sx = x - (1<<i)
            sx = sx % N
        else: # bit is 0
            s = 1
            sx = x + (1<<i)
            sx = sx % N

        sy = A[sx]
        dydxbi = (itob(sy) - itob(A[x]))/s
        dydx[31-i,:] = dydxbi

    return dydx


def dirdandin(y, x1, x2, dx1din, dx2din, v=False):
    if v:
        print('dirdand')
    
    # samples = [-2, -1, 1, 2]
    samples = [-1, 1]
    
    dydx1s = []
    dydx2s = []
    for i, s in enumerate(samples):
        dydx1s.append(((int(x1 + s*dx1din[i]) & x2) - y)/s)
        dydx2s.append(((x1 & int(x2 + s*dx2din[i])) - y)/s)
        if v:
            pi(str(s), int(x1 + s*dx1din), x2, (int(x1 + s*dx1din) & x2), y, (int(x1 + s*dx1din) & x2) - y, s*dx1din)
            pi(str(s), (x1 & int(x2 + s*dx2din)) - y, (s*dx2din))

    if v:
        pa('dydx1s', dydx1s)

    dydin = (dydx1s[0] + dydx2s[0], dydx1s[1] + dydx2s[1])
    if v:
        pa('dydx1', dydx1)
        print()

    return dydin


def dand(y, x1, x2, dx1din, dx2din, v=False):
    if v:
        print('dand')
    
    # samples = [-2, -1, 1, 2]
    samples = [-1, 1]
    
    dydx1s = []
    dydx2s = []
    for i, s in enumerate(samples):
#         if (
        if (dx1din != 0):
            dydx1s.append(((int(x1 + s*dx1din) & x2) - y)/(s*dx1din))
        else:
            dydx1s.append(0)
        if (dx2din != 0):
            dydx2s.append(((x1 & int(x2 + s*dx2din)) - y)/(s*dx2din))
        else:
            dydx2s.append(0)
        if v:
            pi('1',(int(x1 + s*dx1din) & x2) - y, s*dx1din)
            pi('2', (x1 & int(x2 + s*dx2din)) - y, (s*dx2din))

    if v:
        pa('dydx1s', dydx1s)

    dydx1 = weighted_avg(dydx1s)
    dydx2 = weighted_avg(dydx2s)
    if v:
        pi('dydx1', dydx1)
        print()

    return dydx1, dydx2


def dandb(x1, x2, v=False):
	if v:
		print('dandb')
	dx2 = int_to_bits(x1)
	dx1 = int_to_bits(x2)

	return (dx1, dx2)


class And():
    
    def __init__(self):
        pass
    
    def forward(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
        return x1 & x2
    
    def backward(self, grad):
        x1_bits = int_to_bits(self.x1)
        x2_bits = int_to_bits(self.x2)

        # bit wise multiply
        grad_x1 = np.multiply(x2_bits, grad)
        grad_x2 = np.multiply(x1_bits, grad)

        return (grad_x1, grad_x2)
    
def dxorin(y, x1, x2, dx1din, dx2din, v=False):
    
    samples = [-2, -1, 1, 2]
    
    dydx1s = []
    dydx2s = []
    for i, s in enumerate(samples):
#         if (
        if (dx1din != 0):
            dydx1s.append(((int(x1 + s*dx1din) ^ x2) - y)/(s*dx1din))
        else:
            dydx1s.append(0)
        if (dx2din != 0):
            dydx2s.append(((x1 ^ int(x2 + s*dx2din)) - y)/(s*dx2din))
        else:
            dydx2s.append(0)
        if v:
            pi('1',(int(x1 + s*dx1din) ^ x2) - y, s*dx1din)
            pi('2', (x1 ^ int(x2 + s*dx2din)) - y, (s*dx2din))

    if v:
        pa('dydx1s', dydx1s)

    dydx1 = weighted_avg(dydx1s)
    dydx2 = weighted_avg(dydx2s)
    if v:
        pi('dydx1', dydx1)
        print()

    return dydx1 + dydx2


 
def dirdxorin(y, x1, x2, dx1din, dx2din, v=False):
    if v:
        print('dirdxorin')
    
    samples = [-1, 1]
    
    dydx1 = []
    dydx2 = []
    for i, s in enumerate(samples):
#         if (
        # dydx1.append(((int(x1 + s*dx1din) ^ x2) - y)/(s*dx1din))
        dydx1.append(((int(x1 + s*dx1din[i]) ^ x2) - y)/s)
        dydx2.append(((x1 ^ int(x2 + s*dx2din[i])) - y)/s)
        # dydx2.append(((x1 ^ int(x2 + s*dx2din)) - y)/(s*dx2din))
        if v:
            pi('1',(int(x1 + s*dx1din[i]) ^ x2) - y, s*dx1din[i])
            pi('2', (x1 ^ int(x2 + s*dx2din[i])) - y, (s*dx2din[i]))


    dydin = (dydx1[0] + dydx2[0], dydx1[1] + dydx2[1])
    if v:
        pa('dydx1', dydx1)
        print()

    return dydin
    
    
    
def dxor(y, x1, x2, dx1din, dx2din, v=False):
    if v:
        print('dxor')
    
    samples = [-2, -1, 1, 2]
    
    dydx1s = []
    dydx2s = []
    for i, s in enumerate(samples):
#         if (
        if (dx1din != 0):
            dydx1s.append(((int(x1 + s*dx1din) ^ x2) - y)/(s*dx1din))
        else:
            dydx1s.append(0)
        if (dx2din != 0):
            dydx2s.append(((x1 ^ int(x2 + s*dx2din)) - y)/(s*dx2din))
        else:
            dydx2s.append(0)
        if v:
            pi('1',(int(x1 + s*dx1din) ^ x2) - y, s*dx1din)
            pi('2', (x1 ^ int(x2 + s*dx2din)) - y, (s*dx2din))

    if v:
        pa('dydx1s', dydx1s)

    dydx1 = weighted_avg(dydx1s)
    dydx2 = weighted_avg(dydx2s)
    if v:
        pi('dydx1', dydx1)
        print()

    return dydx1, dydx2
        
    
def dxorb(x1, x2):
    x1b = int_to_bits(x1)
    x2b = int_to_bits(x2)
    dx1 = np.zeros(32)
    dx2 = np.zeros(32)
    
    for i in range(32):
    	dx1[i] = -1 if x2b[i] == 1 else 1
    	dx2[i] = -1 if x1b[i] == 1 else 1

    return (dx1, dx2)


def mergedxor(y, dx1, dx2, v=False):

    def mvecs(y, v1, v2):
        vout = np.zeros(32)
        vsum = v1 + v2
        for i in range(32):
            if y[i] == 0:
                # sum in [-2, -1, 0, 1, 2]
                vout[i] = np.abs(vsum[i]) % 2
            else: # y[i] == 1
                # sum should only be [-1, 0, 1]
                vout[i] = -np.abs(vsum[i])
        return vout


    if (dx1.ndim == 1 and dx2.ndim == 1):
        # vec vec
        out = mvecs(y, dx1, dx2)

    elif (dx1.ndim == 2 and dx2.ndim == 2):
        # mat mat
        out = np.zeros((32, 32))
        for i in range(32):
            out[i, :] = mvecs(y, dx1[i,:], dx2[i,:])
    else:
        # vec mat
        out = np.zeros((32, 32))
        if dx1.ndim == 1:
            dx1 = np.diag(dx1)
        else:
            dx2 = np.diag(dx2)
        for i in range(32):
            out[i, :] = mvecs(y, dx1[i,:], dx2[i,:])
    return out


def bmult(bits1, bits2):
    if (bits1.ndim == 1 and bits2.ndim == 1):
        # vec vec
        out = np.multiply(bits1, bits2)

    elif (bits1.ndim == 2 and bits2.ndim == 2):
        # mat mat
        out = np.multiply(bits1, bits2)
    elif (bits1.ndim == 1 and bits2.ndim == 2):
        out = np.multiply(bits1[np.newaxis, :], bits2)
    elif (bits1.ndim == 2 and bits2.ndim == 1):
        out = np.multiply(bits1, bits2[:, np.newaxis])
    else:
        raise ValueError('Unexpected bitderiv dimensions {} {}'.format(bits1.ndim, bits2.ndim))
    # else:
        # vec mat
        # out = np.zeros((32, 32))
        # if bits1.ndim == 1:
        #     vec = bits1
        #     mat = bits2
        # else:
        #     vec = bits2
        #     mat = bits1
        # for i in range(32):
        #     out[i, :] = np.multiply(vec, mat[i,:])
    return out


def dxorbin(y, x1, x2, dx1din, dx2din, v=False):
    x1b = int_to_bits(x1)
    x2b = int_to_bits(x2)
    dx1 = np.zeros(32)
    dx2 = np.zeros(32)
    
    for i in range(32):
        dx1[i] = -1 if x2b[i] == 1 else 1
        dx2[i] = -1 if x1b[i] == 1 else 1

    if v:
        print('y')
        print(itob(y))
        print()
        print('dx1')
        print(dx1)
        print(dx1din)
        print(bmult(dx1, dx1din))
        print()
        print('dx2')
        print(dx2)
        print(dx2din)
        print(bmult(dx2, dx2din))
        print()
        print(mergedxor(itob(y), bmult(dx1, dx1din), bmult(dx2, dx2din), v) )
        print()
        print()

    return mergedxor(itob(y), bmult(dx1, dx1din), bmult(dx2, dx2din), v) 


def weighted_avg(arr):
    weights = np.hamming(len(arr))
    return np.sum(np.multiply(np.array(arr), weights/np.sum(weights)))
    

    
class Xor():
    
    def __init__(self):
        self.x1s = []
        self.x2s = []
        self.samples = []
        pass
    
    def calc(self, x1, x2, sample=None, v=False):
        y = x1 ^ x2
        
        if sample:
            self.x1s.append(int(x1))
            self.x2s.append(int(x2))
            self.samples.append(sample)
        else:
            self.x1 = x1
            self.x2 = x2
            self.y = y
        return y
            
    
    def grad_xsampling(self, v=False):
        # estimate grad for each x
        # assume samples go -2, -1, 1, 2 ... symmetric around x
        
        if v:
            pi('grad x', self.x1)
        
        xins = []
        dx1s = []
        dx2s = []
        for i, sample in enumerate(self.samples):
            if v:
#                 print('OVER')
#                 print(type(self.x1s[i]), type(self.x1), type(sample))
                pi('dx s',self.x1s[i], self.x1, sample)
            dx1s.append((self.x1s[i] - self.x1)/sample)
            dx2s.append((self.x2s[i] - self.x2)/sample)
        if v:
            pa('dx1s', dx1s)
        
        # weight closer samples more heavily and est grad x1 and x2
        dx1 = weighted_avg(dx1s)
        dx2 = weighted_avg(dx2s)
        if v:
            pi('x, dx1', self.x1, dx1)
        
        # now use estimate x gradient to sample y 
        # (use same samples used to calc x, may want to set this to something custom later)
        dydx1s = []
        dydx2s = []
        for i, s in enumerate(self.samples):
            dydx1s.append(((int(self.x1 + s*dx1) ^ self.x2) - self.y)/(s*dx1))
            dydx2s.append(((self.x1 ^ int(self.x2 + s*dx2)) - self.y)/(s*dx2))
            if v:
#                 pi('s1', self.y, self.x1, s*dx1, self.x2, s)
                print(type(self.x1), type(s), type(dx1))
                pi('s x y', int(self.x1 + s*dx1), int(self.x1 + s*dx1) ^ self.x2)
#                 pi('s3', (self.y - (int(self.x1 + s*dx1) ^ self.x2)), s)

        if v:
            pa('dydx1s', dydx1s)
            
        dydx1 = weighted_avg(dydx1s)
        dydx2 = weighted_avg(dydx2s)
        if v:
            pi('dydx1', dydx1)
            print()
            print()
        
        # reset samples
        self.x1s = []
        self.x2s = []
        self.samples = []
        
        return dydx1, dydx2

    
    
    
        # take samples using gradient
        
#         sampsize = 4
#         x1samp = np.zeros(sampsize+1, dtype=np.int)
#         x2samp = np.zeros(sampsize+1, dtype=np.int)

#         for i in range(sampsize+1):
#             x1samp[i] = (x1 - sampsize//2 + i) ^ x2
#             x2samp[i] = (x2 - sampsize//2 + i) ^ x1

#             dx1samp = x1samp[1:] - x1samp[:-1]
#             dx2samp = x2samp[1:] - x2samp[:-1]

#             dx1est = np.sum(np.multiply(dx1samp, np.hamming(sampsize)/np.sum(np.hamming(sampsize))))
#             dx2est = np.sum(np.multiply(dx2samp, np.hamming(sampsize)/np.sum(np.hamming(sampsize))))

#             return (dx1est, dx2est)
