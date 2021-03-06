import numpy as np
import cv2
from utils.data import gen
from utils import cv_wrap as W
from core.calib.focal import FocalSolverStrum

def main():
    seed = np.random.randint( 65536 )
    #seed = 55507
    #seed = 34112

    print('seed', seed)
    np.random.seed( seed )

    #K = np.float32([500,0,320,0,500,240,0,0,1]).reshape(3,3)
    w = 640.0
    h = 480.0
    K = np.float32([1260,0,280,0,1260,230,0,0,1]).reshape(3,3)
    K0 = K.copy()

    s_noise = 1000.0
    K0[0,0] = np.abs( np.random.normal(K0[0,0], scale=s_noise) ) # fx
    K0[1,1] = np.abs( np.random.normal(K0[1,1], scale=s_noise) ) # fy
    K0[0,2] = np.random.normal(K0[0,2], scale=s_noise) # cx
    K0[1,2] = np.random.normal(K0[1,2], scale=s_noise) # cy

    print 'K'
    print K
    print 'K0'
    print K0

    Fs = []
    Ws = []
    print 'begin generation'
    for i in range(128):
        print '{}/{}'.format(i,128)
        p1, p2, x, P1, P2 = gen(min_n=64, w=w,h=h,K=K)
        F, msk = W.F(p1, p2,
                method=cv2.FM_RANSAC,
                ransacReprojThreshold=0.999,
                confidence=1.0
                )
        #print 'F', F
        #E, _ = cv2.findEssentialMat(p1,p2,K,
        #        cv2.FM_RANSAC,
        #        0.999,
        #        0.1)
        #        #thresh=1.0,
        #        #prob=0.999)
        #F = M.E2F(E, K=K)
        #print 'F', F / F[2,2]
        Fs.append(F)
        Ws.append( float(np.count_nonzero(msk)) / msk.size )
    Fs = np.asarray(Fs, dtype=np.float64)

    foc = FocalSolverStrum(w,h)(Fs)
    print 'computed foc', foc

if __name__ == "__main__":
    main()

