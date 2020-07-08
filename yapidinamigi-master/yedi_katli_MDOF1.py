import math
import numpy as np
from scipy.linalg import eigh

class Yapi:

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
            
        print(self.m_matrix)
            
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
            
        print(self.k_matrix)
        
        return
    
    def naturalFrequency(self):
        
        self.wn_matrix, self.v_amplitude = eigh(self.k_matrix,self.m_matrix, eigvals_only=False)

        self.wn=np.zeros((self.storeynumber,1))
        self.Tn=np.zeros((self.storeynumber,1))
        
        for i in range(0,len(self.wn_matrix)):
            self.wn[i]=math.sqrt(self.wn_matrix[i])
            self.Tn[i]=2*math.pi/self.wn[i]
            
    
        print("wn={}".format(self.wn))
        print("Tn={}".format(self.Tn))

        return

    def dampingRatio(self,ksi):
        
        self.ksi=0
        self.c=np.zeros((self.storeynumber,1))
        for i in range(0,len(self.c)):
            self.c[i]=2*ksi*self.wn[i]*self.m_matrix[i][i]
        print("c={}".format(self.c))

        return
    
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
        
        print("c matrix={}".format(self.c_matrix))        
    
    def amplitudeCalc(self):

        self.amp = np.zeros(self.v_amplitude.shape)

        for i in range(0,self.storeynumber):
            self.amp[i]=self.v_amplitude[:,i]/self.v_amplitude[0][i]
        
            print("amplitude{}={}".format(i+1,self.amp[i]))
            

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
        print(self.t_amount)

    def newmark(self, dt):
        
         self.dt=dt
         self.t_amount=len(self.ags)
         self.beta=1/4
         self.gamma=1/2
         x0=0
         v0=0
         
         for i in range(0,self.storeynumber):
             
             p= -self.M_Generalized[i][i] * self.ags * 9.806
             
             khat= self.K_Generalized[i][i] + self.gamma/(self.beta*self.dt)*self.c + 1/(self.beta*(self.dt**2))*self.M_Generalized[i][i]
             const1=1/(self.beta*self.dt)*self.M_Generalized[i][i] + self.gamma/self.beta*122.80505021
             const2=self.M_Generalized[i][i]/(2*self.beta)+self.dt*(self.gamma/(2*self.beta)-1)*122.80505021
            
             x=list()
             v=list()
             a=list()
             x[i]=list(np.zeros(self.t_amount))
             v[i]=list(np.zeros(self.t_amount))
             a[i]=list(np.zeros(self.t_amount))
             
             x[0]=x0
             v[0]=v0
             a[0]=(p[0]-122.80505021*v[0]-self.K_Generalized[i][i]*x[0])/self.M_Generalized[i][i]
            
             index_array=np.arange(1,self.t_amount)
        
             for j in index_array:
                 delta_p=p[j]-p[j-1]
                
                 delta_phat=delta_p+const1*v[j-1]+const2*a[j-1]
                
                 delta_x=delta_phat/khat
                
                 delta_v=(self.gamma/(self.beta*dt))*delta_x - self.gamma/self.beta*v[j-1]+self.dt*(1-self.gamma/(2*self.beta))*a[j-1]
                
                 delta_a=delta_x/(self.beta*self.dt**2)-v[j-1]/(self.beta*self.dt)-a[j-1]/(2*self.beta)
                
                 x[j]=x[j-1]+delta_x
                 v[j]=v[j-1]+delta_v
                 a[j]=a[j-1]+delta_a
    
         return x,v,a

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
    
    
            
        



    

    
    
        
        
        
        
        
            
        
            
    
        


            
    
                
            
            
        
        
            
            
        
            
        
            

    