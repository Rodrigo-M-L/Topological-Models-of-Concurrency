import matplotlib.pyplot as plt
import numpy as np
def showsquares(li,I):
    White=np.zeros(li)
    Lb=I[0]
    Ub=I[1]
    check=[Lb[j]==Ub[j] for j in range(len(Lb))]
    if sum(check)<1:
        for i in range(li[0]):
            for j in range(li[1]):
                if I[0][0]<=i<I[1][0] and I[0][1]<=j<I[1][1]:
                    White[i][j]=1
                else:
                    pass
        White=np.rot90(White)        
        im = plt.imshow(White, cmap='Blues',extent =[0,li[0],0,li[1]])
        plt.show()
        return White
    else:
        pass
    

def overlap(li,PrunnedSpace):
    Finalsquare=[]
    Allsquares=[]
    for I in PrunnedSpace:
        Finalsquare.append(showsquares(li,I))
    for x in Finalsquare:
        if type(x)==type(None):
            pass
        else:
            Allsquares.append(x)
    Final=Allsquares[0]
    for i in range(len(Allsquares)-1):
        Final=Final+Allsquares[i+1]
    for i in range(len(Final)):
        for j in range(len(Final[0])):
            if Final[i][j]!=0:
                Final[i][j]=1
            else:
                pass
    im = plt.imshow(Final, cmap='Blues', extent =[0,li[0],0,li[1]])
    plt.show()