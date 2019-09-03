import numpy as np
import enFrame as eF
import librosa as li

path = r'''G:\RecordData\Record\speaker00001_M\audio\speaker00001_M_stn00037.wav'''

startPoint = 0
endPoint = len(audio)
windowSize = 0.025
windowShift = 0.01
fs = 16000
FrameLen = windowSize*fs			#帧长
FrameInc = windowShift*fs			#帧位移

temp1 = eF.enframe(audio[0:len(audio)-1],FrameLen,FrameInc) 
temp2 = eF.enframe(audio[1:len(audio)],FrameLen,FrameInc)

maxSilence = 20 # 
addSilence = 5
minLen = 10
status = 0
count = 0
silence = 0

#过零率
signs = np.where(temp1*temp2 > 0,0,1) 
diffs = np.where(abs(temp1-temp2)> 0.02, 1, 0)
zcr = (signs*diffs).sum(axis = 1).reshape(np.size(signs,0),1)

#短时能量
amp = abs(eF.enframe(audio,FrameLen,FrameInc)).sum(axis=1).reshape(np.size(signs,0),1)
#print(amp)
#print(amp.shape)
#设置门限值
amp1 = 10
amp2 = 2

zcr1 = 10
zcr2 = 5

speechCount = 0
endPoint =amp.shape[0]

#重新调整能量阈值
#amp1 = max(amp1,max(amp)/4)
#amp2 = min(amp2,min(amp)/8)
x1=[]
x2=[]
#短时能量:浊音>清音>静音 过零率: 清音>浊音>静音
for n in range(endPoint):
	if status in {0,1}:
		if amp[n,0] > amp1:			#确信进入语音段
			x1.append(max(n-count-1,1))	#起点
			status = 2
			silence = 0
			count = count + 1
		elif (amp[n,0]>amp2) or (zcr[n,0]>zcr2): #可能进入语音段
			status = 1
			count = count + 1
		else:
			status = 0
			count = 0
	elif status == 2:									#进入语音
		if (amp[n,0] > amp2) or (zcr[n,0] > zcr2):			#语音保持
			count = count + 1
			silence = 0
		else:		
			silence = silence+ 1
			if silence <maxSilence :							#静音时间不够长
				
				count = count + 1
			
			else:											#此段语音结束，下一段
				#status = 3
				count = count -silence+addSilence
				if count < minLen:							#序列长度不够，认为是噪音
					status = 0
					silence = 0
					count = 0
				else:
					x2.append(x1[speechCount]+count-1)
					speechCount = speechCount + 1
					status = 0
					silence = 0
					count = 0
	else :
		break
print (x1)
print (x2)
