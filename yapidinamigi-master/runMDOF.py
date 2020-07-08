from yedi_katli_MDOF1 import *
import matplotlib.pyplot as plt


yapi=Yapi([100,100,100,100], [12800*2,30341*2,30341*2,30341*2], 4)

yapi.rigidityMatrix()
yapi.massMatrix()
yapi.naturalFrequency()
yapi.dampingRatio(0.05)
yapi.dampingMatrix()
yapi.amplitudeCalc()
yapi.generalMassMat()
yapi.generalStiffnessMat()
yapi.generalDampingMat()
yapi.modeParticipatingFactor()
yapi.effectiveParticipatingMass()
yapi.earthquakeData("depremkaydi.csv", ",")
yapi.newmark(0.01)


plt.plot(a)
ax0 = plt.gca()
ax0.grid(True)
ax0.legend()
plt.xlabel("t(s)")
plt.ylabel("a (m/s2)")
plt.title("Acceleration")
plt.show()

# =============================================================================
# V_norm_fig = np.vstack([ np.zeros(yapi.storeynumber) , yapi.amp ])
# 
# fig, axs = plt.subplots(1, yapi.storeynumber , sharey=True , figsize=(10,4))
# fig.subplots_adjust(hspace=0)
# fig.suptitle("Mod Şekilleri", fontsize=18)
# 
# for i in range(yapi.storeynumber):
#     axs[i].plot( np.zeros(yapi.storeynumber+1) , np.arange(yapi.storeynumber+1) ,"grey" , marker="o")
#     axs[i].plot( V_norm_fig[:,i], np.arange(yapi.storeynumber+1) , "r",marker = "o",
#        MS=10)
#     # axs[i].set_title(f"w = {round(yapi.wn[i],1)}Hz & T = {round(yapi.Tn[i],1)}sn")
#     axs[i].set_ylim(0)
# plt.show()
# 
# 
# =============================================================================



