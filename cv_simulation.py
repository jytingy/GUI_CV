
import numpy as np
import matplotlib.pyplot as plt

def simulate(E0, Da, Db, k0, alpha):
    #Parameters and Variables
    it = 100 # time steps
    ix = 50 # space steps
    DMA = 0.45 # dt/dx constant for stability must be lower than 0.5
    Ei = 0.2 # starting potential of CV
    Ef = -0.2 # final potential of CV
    a = 0.5 # transfer coefficientf
    T = 298.15 # temperature in Kelvin
    R = 8.3145 # ideal gas law constant in J/mol*K
    F = 96485 # Faraday's constant in C/mol
    f = F/(R*T) # constant 
    print ("Constant value 'f' is:", f)
    v = 0.1 # scan rate in V/s
    tk = (Ei-Ef)/v # total time to do a cathodic or anodic scan of the CV
    print ("CV's total time is:", tk)
    Eo = 0 # formal potential in V
    ko = 1e-4 # standard rate constant in m/s
    print ("Standard rate constat is:", ko)
    CA = 1 # Bulk concentration of species A in M
    CB = 0 # Bulk concentration of species B in M
    semi = it/2 # Iteration to the to final potential range
    print ("Iteration needed to get to final potential", semi)
    # Da = 1.00e-9 # diffusion coefficient of species A (assume to be the same as species B in m^2/s)
    # Db = 1.00e-9 # diffusion coefficien of species B
    psi = ko/(np.sqrt(3.1416*Da*f*v)) #check 
    print ("psi:", psi)
    dt = tk/semi # differential of time in s
    dx = np.sqrt((Da*tk)/(DMA*semi)) # differential of space in m
    print ("dt:", dt, "and dx:", dx)
    khom = 0 # check in 1/s
    T = tk*khom # check
    dT = dt*khom # check
    z = 1 # number of electrons
    A = 1 # area of electrode cm^2
    i = np.zeros(it+1) # list for current
    E = np.zeros(it+1) # list for potential
    Caa = np.zeros(ix) # Initial concentration array for a
    Cbb = np.zeros(ix) # Initial concentration array for b
    Caa_new = np.zeros(ix) # New concentration array for a
    Cbb_new = np.zeros(ix) # New concentration array for b

    #input params
    Eo = E0    
    Da = Da    
    Db = Db
    k = k0  
    a = alpha  
  

    #Initial conditions 
    Caa [:] = CA
    Cbb [:] = CB
    Caa_new[49]=CA

    #Formulas and iterations

    for ti in range(0, it + 1):
        n = (Ei-((Ei-Ef))*ti/ix)-Eo # check overpotential formula in V
        kf = ko*np.exp(-a*f*(n)) # reaction rate foward constant in m/s
        kb = ko*np.exp((1-a)*f*n) # reaction rate backward constant in m/s
        
        if ti > 50: # Reversing the potential
            n = (Ef+((Ei-Ef))*(ti-ix)/ix)-Eo # check overpotential formula in V
            kf = ko*np.exp(-a*f*(n)) # reaction rate foward constant in m/s
            kb = ko*np.exp((1-a)*f*n) # reaction rate backward constant in m/s
    
        if ti in [1, 25, 35, 50, 75, 90, 100]:  # Concentration at different time points
            plt.plot(Caa_new, label=f'Caa, t={ti}')
            plt.plot(Cbb_new, label=f'Cbb, t={ti}', linestyle='--')
            plt.title('Concentration Profiles ')
            plt.xlabel('Distance from electrode')
            plt.ylabel('Concentration / M')
            plt.legend()
            plt.grid(False)
            # plt.show()

        for x in range (0, ix-1):
            if ti < 1:  # initial conditions 
                Caa_new[x] = CA # concentration at the surface is the same in the bulk
                Cbb_new[x] = CB # concentration at the surface is the same in the bulk
            
            if ti >= 1 and x >= 1: #bulk concentration 
                Caa_new[x] = Caa[x]+DMA*(Caa[x+1]-2*Caa[x]+Caa[x-1])
                Cbb_new[x] = Cbb[x]+DMA*(Cbb[x+1]-2*Cbb[x]+Cbb[x-1])-dT*Cbb[x]
                
                
            if x < 1: # surface concentration 
                I = (kf*Caa_new[0]-kb*Cbb_new[0])/(1+(kf*dx/(2*Da))+(kb*dx/(2*Db))) # flux of mol units in mol/s*m^2
                i[ti]=I
                Caa_new[0] = Caa[0] + DMA*(Caa[1] - Caa[0]) - (dt/dx)*i[ti] 
                Cbb_new[0] = Cbb[0] + DMA*(Cbb[1] - Cbb[0]) + (dt/dx)*i[ti] - dT*Cbb[0]
                #i[ti] = I * z* F * 1000 # Converting mol*m/s*L to A/m^2
            
            
        E[ti]=n # Saving potential
        Caa [:] = Caa_new [:] # Saving concentration profile of A through space
        Cbb [:] = Cbb_new [:] # Saving concentration profile of B through space
        

    plt.plot(E, i, label='Potential Scan')
    plt.gca().invert_xaxis() #for Texas Convention
    plt.xlabel('Potential / V')
    plt.ylabel('Current / A')
    plt.title('Texas Convention CV simulator')
    #plt.legend()
    plt.grid(False)
    # plt.show()
    plt.figure()

    #Making the plot prettier

    plt.style.use('grayscale')  
    plt.figure(figsize=(8, 5))

    plt.plot(E, -i, label='CV curve', linewidth=2.5, color='green')

    plt.xlabel('Potential (V)', fontsize=16)
    plt.ylabel('Current (A)', fontsize=16)
    plt.title('Cyclic Voltammetry Simulation', fontsize=18)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)


    plt.legend(fontsize=15, loc='best')
    plt.grid(False)

    plt.tight_layout()
    plt.show()
    
    return plt.gcf()


