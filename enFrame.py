import numpy as np

def enframe(date,size,inc):
	length = len(date)
	fCount = int(np.fix((length - size +  inc)/inc))		#帧数
	
	indf_temp = (inc * np.arange(fCount).reshape(1,fCount)).T .astype(np.int)  #每帧开头
	inds_temp = np.arange(size).reshape(1,int(size)).astype(np.int)		   #帧内位置
	indf = np.repeat(indf_temp,size,axis = 1)
	inds = np.repeat(inds_temp,fCount,axis = 0)
	f = date[indf+inds]
	
	return f
