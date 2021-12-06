from __future__ import division
import numpy as np
cimport numpy as np

DTYPE = np.float64
ctypedef np.float64 DTYPE_t

def loop_cloud_life(np.ndarray[DTYPE_t, ndim=3] w, np.ndarray[DTYPE_t, ndim=2] z):
    assert w.dtype == DTYPE and z.dtype == DTYPE

    cdef int idx_z = w.shape[0]
    cdef int idx_lat = w.shape[1]
    cdef int idx_lon = w.shape[2]

    cdef np.ndarray[DTYPE_t, ndim=2] life_up = np.zeros([idx_lat,idx_lon], dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] life_dw = np.zeros([idx_lat,idx_lon], dtype=DTYPE)

    cdef int i,k,j
    w_max = 1.0
    w_min = -0.5
  
    for i in xrange(idx_lat):
        for j in xrange(idx_lon):
            bot_up = 0
            bot_dw = 0
            top_up = 0
            top_dw = 0
            for k in xrange(idx_z-1):
                if w[k,i,j]>=w_max:
                    if w[k+1,i,j]<w_max:
                        top_up=k
                elif w[k+1,i,j]>=w_max:
                    bot_up=k+1
                if w[k,i,j]<=w_min:
                    if w[k+1,i,j]>w_max:
                        top_dw=k
                elif w[k+1,i,j]<=w_min:
                    bot_dw=k+1
      
                if z[top_up]-z[bot_up]>1.5:
                    np.put(life_up, [i,j], 1)
                if z[top_dw]-z[bot_dw]>1.5:
                    np.put(life_dw, [i,j], 1)
    return life_up, life_dw 
