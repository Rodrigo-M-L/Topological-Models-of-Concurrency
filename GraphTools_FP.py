import copy
import itertools
import numpy as np
class SGraph_FP:
    def __init__(self,p,c=1):
        #exemple of imput p=[['Pa','Pb','Va','Vb'],['Pb','Vb','Pa','Va']]
        #c is the capacity of each resouce. By default we assume the resources are mutex, but we can change this for each individual resource with a function
        self.dim=len(p)
        self.p=p
        self.c=c
        self.cap=dict()
        for i in range(self.dim):
            for j in range(len(p[i])):
                self.cap[(self.p[i][j][1])]=c
        global MemoryOfPath
        global number_Of_Elements_of_Pn_removed
        number_Of_Elements_of_Pn_removed=0
        MemoryOfPath=[] #used in recursive functions that need to know what coordenates they went.
            
    #-- alg 1 start --#        
    #-- change capacity of each resource before build graph with this function. By default every resource is a mutex --#    

    def changecap(self,resource,capacity):
        self.cap[resource]=capacity
        print(self.cap)
            
    #-- change capacity of each resource before build graph with this function. By default every resource is a mutex --#



    #-- constructs the vertices and locks the capacity of each resource. If you change the capacity this needs to be reruned --#
    #-- After executing this use .returnvertices() to observer the output --#

    def product(self,*args, repeat=1):
    #modified from https://docs.python.org/3/library/itertools.html to have a input list instead of lists (i.e. original input l1,l2,l3.... now [l1,l2,l3....])
        pools = [tuple(pool) for pool in args[0]] * repeat
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield list(prod)
    #this produces the product of the coordenates that are going to be the vertices of the graph


    def infograph(self):
        #We create a list such that we have the position of the vertice of a graph,the capacity of the resources and the resource that are being used
        self.res=copy.deepcopy(self.cap)
        self.coordinates=[]
        for i in range(len(self.p)):
            self.coordinates.append([k for k in range(len(self.p[i])+1)])
        for i in self.res:
            self.res[i]=0
            #Reset the values of the dictionary to 0. This because in the initial state the resource consumption is 0

        print(self.cap)
        print(self.res)
        #now we have enough to define the information need to generate the vertices of the graph


    def createvertice(self):
        self.vertices=[]
        for v in self.product(self.coordinates):
            self.vertices.append(v)
        self.init=self.vertices[0]
        self.end=self.vertices[-1]
            

    #-- After executing this use .returnvertices() to observer the output --#
    #-- constructs the vertices and locks the capacity of each resource. If you change the capacity this needs to be reruned --#
                
    
    #-- creates the full graph with python dictionaries use .returngraph() to observe the output after executing this function --#

                
    #now we have enough to creat the edges of the graph
    def CreateGraph(self):
        self.infograph()
        self.createvertice()
        print(self.vertices)
        edge=[]
        edges=[]
        for ed in range(len(self.vertices)):
            for i in range(len(self.p)):
                edg=copy.deepcopy(self.vertices[ed])
                resource=edg[i]
                edg[i]=edg[i]+1
                if edg[i]<len(self.p[i])+1:
                    #for vertice (i1,i2,...,in), we create k<=n valid connections that for position i we have [(i1,i2,.,ii,..,in), '__',(i1,i2,.,ii+1,..,in)]
                    edges.append([self.vertices[ed],self.p[i][resource],edg])
                else:
                    pass
        self.edges=edges

        newedges=dict()

        #We can now compress the information such that we have a dictionary where dict[vertice]=[valid conections]
        #with this we will be able to call the connections from the vertices, this will help later to prune the graph
        for ed in range(len(self.vertices)):
            newedges[f'{self.vertices[ed]}']=copy.deepcopy([])
            for i in range(len(self.edges)):
                tempedg=copy.deepcopy(self.edges[i])
                tempedg1=[tempedg[1],tempedg[2]]
                if self.vertices[ed]==self.edges[i][0]:
                    #for i(<=k valid connections) vertices that are being pointed by a fixed vertice we get dict[vertice]=[connection_1,...,connection_i-1,[edge, vertice that is being pointed to]]
                    newedges[f'{self.vertices[ed]}'].append(tempedg1)
                else:
                    pass
        #we have enough to build the graph, because for each vertice we know were to point to


        self.pointers=newedges
        self.fullPreCubical()

    #-- creates the full graph with python dictionaries use .returngraph() to observe the output after executing this function --#

    #-- simple alg for only full graph precubical --#
                    
    def fullPreCubical(self):
        dim=len(self.vertices[0])
        self.SPC=[]
        for n in range(dim-1):
            Pn=dim-n
            dictPn=dict()
            for i in range(len(self.vertices)):
                dictPn[f'{self.vertices[i]}']=[]
                for j in range(len(self.vertices)):
                    test1=[self.vertices[i][k]!=self.vertices[j][k] for k in range(dim)]
                    test2=[self.vertices[j][k]-self.vertices[i][k]==1 for k in range(dim)]
                    if sum(test1)==Pn and sum(test2)==Pn:
                        dictPn[f'{self.vertices[i]}'].append(self.vertices[j])
                    else:
                        pass
            self.SPC.append(dictPn)
        return self.SPC
        #to add P1 and P0 we can just fullPreCubical.append(self.pointers);fullPreCubical.append(self.vertices)
        #we dont do this because we want to visualiza P2...Pn with this set


    #-- alg 1 end --# 
    
    #-- alg 2&3 start --# 

    def singleRemoval(self,init_vertice,ElementOfPn,n=1):
        global number_Of_Elements_of_Pn_removed
        if n<len(ElementOfPn):
            nOfPn=-n+1
            n_plus_1_Of_Pn=-n
            for i in range(len(self.vertices)):
                test1=[ self.vertices[i][j]<=init_vertice[j]<=ElementOfPn[j] for j in range(len(ElementOfPn))]
                if sum(ElementOfPn)-sum(self.vertices[i])<n+2 and all(test1):
                    original_size=len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])
                    for l in range(len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])):
                        l=l-(original_size-len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}']))
                        test2=[ ElementOfPn[j]<=self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l][j]  for j in range(len(ElementOfPn))]
                        if all(test2):
                            RemoveNext=copy.deepcopy(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l])
                            if ElementOfPn in self.SPC[nOfPn][f'{init_vertice}']:
                                print(f'We are in {ElementOfPn} (P{n}) and remove {ElementOfPn} (P{n})')
                                self.SPC[nOfPn][f'{init_vertice}'].remove(ElementOfPn)
                                number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
                            else:
                                pass
                            if self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l] in self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}']:
                                print(f'we are in {init_vertice}:{ElementOfPn} (P{n}) and remove {self.vertices[i]}:{RemoveNext}  (P{n+1}) ')
                                self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'].remove(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l])
                                number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
                                self.singleRemoval(self.vertices[i],RemoveNext,n+1)
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
            if ElementOfPn in self.SPC[nOfPn][f'{init_vertice}']:
                print(f'we are in {ElementOfPn} (P{n}) and remove {ElementOfPn} (P{n})')
                self.SPC[nOfPn][f'{init_vertice}'].remove(ElementOfPn)
                number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
        else:
            pass

       
    def ResourceUpdater(self,string):
        #if P of resource x then +1 to resource utilization x
        #if V of resource x then -1 to resource utilization x
        if string[0]=='P':
            return [string[1],1]
        elif string[0]=='V':
            return [string[1],-1]
        else:
            print('error')

    def getdirection(self,vertice1,vertice2):
        for i in range(len(vertice1)):
            if vertice2[i]-vertice1[i]!=0:
                return i
            else:
                pass


    def Cap_vertices(self):
        self.capproblems=[]
        vertices=copy.deepcopy(self.vertices)
        #Here we create a python dictonary that stores the capacity of each resource and we will be able to individually change it, i.e., cv_a^p(v)
        self.Resourcetracker=dict()
        self.Resourcetracker[f'{vertices[0]}']=copy.deepcopy(self.res)
        for i in range(1,len(vertices)):
            for k in range(1,len(vertices[i])+1):
                if vertices[i][-k]-1>=0:
                    verticeteste=copy.deepcopy(vertices[i])
                    verticeteste[-k]=verticeteste[-k]-1
                    self.Resourcetracker[f'{vertices[i]}']=copy.deepcopy(self.Resourcetracker[f'{verticeteste}'])
                    for l in range(len(self.pointers[f'{verticeteste}'])):
                        if self.pointers[f'{verticeteste}'][l][1]==vertices[i]:
                            resource_info=self.ResourceUpdater(self.pointers[f'{verticeteste}'][l][0])
                            self.Resourcetracker[f'{vertices[i]}'][resource_info[0]]=self.Resourcetracker[f'{vertices[i]}'][resource_info[0]]+resource_info[1]
                            break
                        else:
                            pass
                    break


    def KeysToList(self,dictionary):
        keys=dictionary.keys()
        ListOfKeys=[list(keys)[i].strip('][').split(', ') for i in range(len(dictionary))]
        for i in range(len(ListOfKeys)):
            for j in range(len(ListOfKeys[0])):
                ListOfKeys[i][j]=int(ListOfKeys[i][j])
        return ListOfKeys
      
    def PrunedGraph_FP(self,halfpruned=False): #Warning do not run this twice!
        self.Forbidden_vertices=[]
        self.Cap_vertices()
        resources=list(self.cap.keys())
        for i in range(len(self.vertices)):
            test_vertice_cap=[self.Resourcetracker[f'{self.vertices[i]}'][resources[c]]<=self.cap[resources[c]] for c in range(len(self.cap))] #v in \check{V}
            if all(test_vertice_cap):
                    pass
            else:
                self.Forbidden_vertices.append(self.vertices[i])
                edges_to_remove=[]
                for e in range(len(self.pointers[f'{self.vertices[i]}'])):
                    edges_to_remove.append(self.pointers[f'{self.vertices[i]}'][e][1])
                del self.pointers[f'{self.vertices[i]}']
                for e in range(len(edges_to_remove)):

                    self.singleRemoval(self.vertices[i],edges_to_remove[e])

        #This removes edges that point to removed vertices.
        if not halfpruned:
            Point_keys=list(self.pointers.keys())
            Point_ver=self.KeysToList(self.pointers)
            keys_removed=0
            for i in range(len(Point_keys)):
                edge_removed=0
                i-keys_removed
                for j in range(len(self.pointers[Point_keys[i]])):
                    j=j-edge_removed
                    if self.pointers[Point_keys[i]][j][1] in Point_ver:
                        pass
                    else:
                        self.singleRemoval(Point_ver[i],self.pointers[Point_keys[i]][j][1])
                        self.pointers[Point_keys[i]].remove(self.pointers[Point_keys[i]][j])
                        keys_removed+=1
                        edge_removed+=1
        else:
            pass
        print(f'number of elements removed {number_Of_Elements_of_Pn_removed}')   
        
    #-- alg 2&3 end --#    
        
    #-- alg 4 start --#
    def alg4(self,v,w,i,a): #d_i^a([v,w])
        c1=0
        c2=0
        while c1!=i:
            c2+=1
            if w[c1+c2]!=v[c1+c2]:
                c1+=1
        if a==0:
            w[c2]=v[c2]
        else:
            v[c2]=w[c2]
        return [v,w]
    #-- alg 4 end --# 
    
    #-- alg 7 start --#   
    
    #-- W_delta_plus --# 
    def Delta_plus(self,dictionary):
        listofvalues=[]
        Values=list(dictionary.values())
        for i in range(len(Values)):
            for j in range(len(Values[i])):
                if Values[i][j][1] not in listofvalues:
                    listofvalues.append(Values[i][j][1])    
        return listofvalues
    
    #-- W_delta_minus --#
    def Delta_minus(self,dictionary):
        keys=dictionary.keys()
        ListOfKeys=[list(keys)[i].strip('][').split(', ') for i in range(len(dictionary))]
        for i in range(len(ListOfKeys)):
            for j in range(len(ListOfKeys[0])):
                ListOfKeys[i][j]=int(ListOfKeys[i][j])
        for x in ListOfKeys:
            if len(self.pointers[f'{x}'])==0:
                ListOfKeys.remove(x)
        return ListOfKeys
    
    def alg7(self):
        V_delta_plus=self.Delta_plus(self.pointers)
        V_delta_minus=self.Delta_minus(self.pointers)
        DV_check=self.KeysToList(self.pointers)
        for x in V_delta_plus:
            if x not in DV_check:
                DV_check.append(x)
        UV_check=copy.deepcopy(DV_check)

        s_p=self.vertices[0]
        t_p=self.vertices[-1]
        
        self.forbidenD=[]
        self.forbidenU=[]
        
        D=[x for x in DV_check if (x!=t_p and x not in V_delta_minus)]
        U=[x for x in UV_check if (x!=s_p and x not in V_delta_plus)]
        
        for d in D:
            self.forbidenD.append(d)
            
        for u in U:
            self.forbidenU.append(u) 

        DG=copy.deepcopy(self.pointers)
        UG=copy.deepcopy(self.pointers)

        while len(D)!=0:
            for vertices in D:
                del DG[f'{vertices}']
            V_delta_minus=self.Delta_minus(DG)
            DV_check=self.KeysToList(DG)
            D=[x for x in DV_check if (x!=t_p and x not in V_delta_minus)]
            for d in D:
                self.forbidenD.append(d)

        while len(U)!=0:
            for vertices in U:
                del UG[f'{vertices}']
            V_delta_plus=self.Delta_plus(UG)
            UV_check=self.KeysToList(UG)
            U=[x for x in UV_check if (x!=s_p and x not in V_delta_plus)]
            for u in U:
                self.forbidenU.append(u) 
        self.DG=DG
        self.UG=UG
        for v in self.Forbidden_vertices:
            self.forbidenD.append(v)
        for v in self.Forbidden_vertices:
            self.forbidenU.append(v)
            
        return [DG,UG]

    #-- alg 7 end --#  


    def returnvertices(self):
        return self.vertices

    def returnFvertices(self):
        return self.Forbidden_vertices
    
    def returnDFvertices(self):
        return self.forbidenD
    
    def returnUFvertices(self):
        return self.forbidenU
    
    def returnedges(self):
        return self.edges

    def returngraph(self):
        return self.pointers

    def returncap(self):
        return self.cap

    def returnDG(self):
        return self.DG

    def returnDG(self):
        return self.UG

    def returnfullPreCubical(self):
        return self.SPC       

    def GE_info(self,halfpruned=False):
        self.CreateGraph()
        self.fullPreCubical()
        self.PrunedGraph_FP(halfpruned)
        #appends P0 and P1 to P
        self.SPC.append(self.pointers)
        self.SPC.append(self.vertices)
        return self.SPC
        