import numpy
cimport numpy as np
DTYPE = np.float
ctypedef np.float_t DTYPE_t
def loop_cloud_life(np.ndarray w):

    cdef int idx_z=w.shape[0]
    cdef int idx_lat=w.shape[1]
    cdef int idx_lon=w.shape[2]

    cdef np.ndarray[numpy.int_t, ndim=2] life_up=np.zeros((idx_lat,idx_lon))
    cdef np.ndarray[numpy.int_t, ndim=2] life_dw=np.zeros((idx_lat,idx_lon))

    cdef int bot_up=0
    cdef int bot_dw=0
    cdef int top_up=0
    cdef int top_dw=0
    for i in range(idx_lat):
        for j in range(idx_lon):
            bot_up=0
            bot_dw=0
            top_up=0
            top_dw=0
            for k in range(idx_eta-1):
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
