import math
import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

class Yapi():
    m=[]
    k=[]
    storeynumber=0
    
    def __init__(self,m,k,storeynumber):
        
        self.m=m
        self.k=k
        self.storeynumber=storeynumber
        # self.massMatrix()
        # self.rigidityMatrix()
        #self.naturalFrequency()
        # self.beginingValues()

        
    def massMatrix(self):
            
        self.m_matrix=np.zeros((self.storeynumber,self.storeynumber))
        for i in range(0,len(self.m)):
            self.m_matrix[i][i]=self.m[i]    
            
        # print(self.m_matrix)
            
        return
    
    def rigidityMatrix(self):
        
        self.k_matrix=np.zeros((self.storeynumber,self.storeynumber))
        
        for i in range(0,len(self.k)):
            if i != (len(self.k)-1):
                self.k_matrix[i][i]=self.k[i]+self.k[i+1]
                
            else:
                self.k_matrix[i][i]=self.k[i]
                
            if i < len(self.k)-1:
                self.k_matrix[i][i+1]=-1*self.k[i+1]
                self.k_matrix[i+1][i]=-1*self.k[i+1]
            
        # print(self.k_matrix)
        
        return
    
    def naturalFrequency(self):
        
        self.wn_matrix, self.v_amplitude = eigh(self.k_matrix,self.m_matrix, eigvals_only=False)

        self.wn=np.zeros((self.storeynumber,1))
        self.Tn=np.zeros((self.storeynumber,1))
        
        for i in range(0,len(self.wn_matrix)):
            self.wn[i]=math.sqrt(self.wn_matrix[i])
            self.Tn[i]=2*math.pi/self.wn[i]
            
    
#        print("wn={}".format(self.wn))
#        print("Tn={}".format(self.Tn))

        return 

    def dampingRatio(self,ksi):
        
        self.ksi=ksi
        self.c=np.zeros((self.storeynumber,1))
        for i in range(0,len(self.c)):
            self.c[i]=2*ksi*self.wn[i]*self.m_matrix[i][i]
        

        return ksi
    
    def dampingMatrix(self):
        self.c_matrix=np.zeros((self.storeynumber,self.storeynumber))
        for i in range(0,self.storeynumber):
            if i != (len(self.c)-1):
                self.c_matrix[i][i]=self.c[i]+self.c[i+1]
                
            else:
                self.c_matrix[i][i]=self.c[i]
                
            if i < len(self.k)-1:
                self.c_matrix[i][i+1]=-1*self.c[i+1]
                self.c_matrix[i+1][i]=-1*self.c[i+1]
        
        # print("c matrix={}".format(self.c_matrix))        
    
    def amplitudeCalc(self):

        self.amp = np.zeros(self.v_amplitude.shape)

        for i in range(0,self.storeynumber):
            self.amp[i]=self.v_amplitude[:,i]/self.v_amplitude[0][i]
        
            # print("amplitude{}={}".format(i+1,self.amp[i]))
            

        return 

    def generalMassMat(self):
        self.M_Generalized=np.zeros((self.storeynumber, self.storeynumber))
        for i in range(0,self.storeynumber):
            self.M_Generalized[i][i] =np.dot(np.dot(self.amp[i], self.m_matrix) ,self.amp[i].reshape(self.storeynumber,1))
        print("M Generalized=\n{}".format(self.M_Generalized))
     
        return
    def generalStiffnessMat(self):
        self.K_Generalized=np.zeros((self.storeynumber,self.storeynumber))
        for i in range(0,self.storeynumber):
            self.K_Generalized[i][i]=self.wn_matrix[i]*self.M_Generalized[i][i]
        print("K Generalized=\n{}".format(self.K_Generalized))
        return

    def generalDampingMat(self):
        self.C_Generalized=np.zeros((self.storeynumber,self.storeynumber))
        for i in range(0,self.storeynumber):
            self.C_Generalized[i][i]=np.dot(np.dot(self.amp[i], self.c_matrix),self.amp[i].reshape(self.storeynumber,1))
        print("C Generalized=\n{}".format(self.C_Generalized))
        return
    
    def earthquakeData(self,file_use_nail,delimiter_use_nail):
        
        ag_txt = np.loadtxt(file_use_nail, delimiter=delimiter_use_nail)
        groundacc=ag_txt[:,1]
        self.ags=groundacc.flatten("C")
        self.t_amount = len(self.ags)
        return

    def newmark(self, m, c, k, dt, p, beta, gamma, x0, v0):
        
        t_amount1 = len(p)
        
        khat= k + gamma/(beta*dt)*c + 1/(beta*(dt**2))*m
        const1=1/(beta*dt)*m + gamma/beta*c
        const2=m/(2*beta)+dt*(gamma/(2*beta)-1)*c
    
        
        x=np.zeros(t_amount1)
        v=np.zeros(t_amount1)
        a=np.zeros(t_amount1)
        
        x[0]=x0
        v[0]=v0
        a[0]=(p[0]-c*v[0]-k*x[0])/m
    
        index_array=np.arange(1,t_amount1)
    
        for j in index_array:
            delta_p=p[j]-p[j-1]
        
            delta_phat=delta_p+const1*v[j-1]+const2*a[j-1]
        
            delta_x=delta_phat/khat
        
            delta_v=(gamma/(beta*dt))*delta_x - gamma/beta*v[j-1]+dt*(1-gamma/(2*beta))*a[j-1]
        
            delta_a=delta_x/(beta*dt**2)-v[j-1]/(beta*dt)-a[j-1]/(2*beta)
        
            x[j]=x[j-1]+delta_x
            v[j]=v[j-1]+delta_v
            a[j]=a[j-1]+delta_a

        return x,v,a
    
    def spectra(self,T):
        
        dt=0.01
        pi = np.pi
        m=1             #kg
        ksi=Yapi.dampingRatio(self,0.05)        #ksi
        p = -m * self.ags
        x0 = 0
        v0 = 0
        beta = 1/4
        gamma = 1/2
        
        f=1/T
        wn=2 * pi * f   #rad/sec
        k=m*wn**2       #N/m
        c=2*ksi*wn*m    #unitless
        x, v, a = Yapi.newmark(self,m, c, k, dt, p, beta, gamma, x0, v0)
        return max(abs(x)), max(abs(v)), max(abs(a))
    
    def spectra1(self):
        
        Sd, Sv, Sa=[], [], []

        for i,j in enumerate(self.Tn):
            sd , sv , sa= Yapi.spectra(self,j)
            Sd.append(sd)
            Sv.append(sv)
            Sa.append(sa)

#            print("Sd{}={}".format(j,Sd[i]))
        
        return Sd
    
    def psuedoAcceleration(self):
        
        self.Sae=[]
        
        for i in range(0,self.storeynumber):
            sae=Yapi.spectra1(self)[i]*self.wn[i]**2
            self.Sae.append(sae)
            
        
        return

    def modeParticipatingFactor(self):
        self.lx=np.zeros((self.storeynumber,1))
        for i in range(0,self.storeynumber):
            self.lx[i]=np.dot(self.amp[i].reshape(1,self.storeynumber),self.m_matrix).dot(np.ones(self.storeynumber))
        
        self.lam=np.zeros((self.storeynumber,1))
        for i in range(0,self.storeynumber):
            self.lam[i]=self.lx[i]/self.M_Generalized[i][i]
        
        print(self.lam)        
        return
    
    def effectiveParticipatingMass(self):
        self.M_eff=np.zeros((self.storeynumber,1))
        
        for i in range(0,self.storeynumber):
            self.M_eff[i]=self.lx[i]**2/self.M_Generalized[i][i]
        
            print("Mx{}={}".format(i,self.M_eff[i]))
            
    
    def baseShear(self):
        
        Ft=[]
        
        for i in range(0,self.storeynumber):
            ft=self.M_eff[i]*9.81* self.Sae[i]
            Ft.append(ft)
        
        return Ft
    
    def baseShearSRSS(self):
        
        squareFt=[x**2 for x in Yapi.baseShear(self)]
        
        sumsquareFt=sum(squareFt)
        
        totalFt=sumsquareFt**0.5
        
        print(totalFt)

    def ModalShapes(self):
        self.amp_fig = np.vstack([ np.zeros(self.storeynumber) , self.amp.T ])
        fig, axs = plt.subplots(1, self.storeynumber , sharey=True , figsize=(10,5))
        fig.subplots_adjust(hspace=0)
        fig.suptitle("Mode Shapes", fontsize=18)
        
        for i in range(self.storeynumber):
            axs[i].plot( np.zeros(self.storeynumber+1) , np.arange(self.storeynumber+1) ,"grey" , marker="o")
            axs[i].plot( self.amp_fig[:,i], np.arange(self.storeynumber+1) , "r",marker = "o",MS=10)
            #axs[i].set_title(f"$wn$ = {round(self.wn_matrix[i],2)}Hz & $wd$={wd_matrix[i]}\nT = {round(T[i],2)}sn")
            axs[i].set_ylim(0)
            axs[i].grid()
            axs[i].title.set_text("Mode" + " " +str(i+1))
        
        

        