import copy
import itertools
from math import comb
class SGraph_W:
        def __init__(self,p,c=1):
            #exemple of imput p=[['Pa','Va', 'Pb','Vb'],['Pb','Vb','Pa','Va']] 
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
            
            #search and tracks the the part of the programs that has the conditions while or if then else


#-------------------------------constructs the vertices and locks the capacity of each resource. If you change the capacity this needs to be reruned--------------#
#----------------------------------------------------After executing this use .returnvertices() to observer the output--------------------------------------------#

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
            
        def Maxpro(self):
            self.Max=[]
            for i in range(len(self.vertices[0])):
                self.Max.append(self.vertices[-1][i])
            return self.Max
#----------------------------------------------------After executing this use .returnvertices() to observer the output--------------------------------------------#
#-------------------------------constructs the vertices and locks the capacity of each resource. If you change the capacity this needs to be reruned--------------#
                
    
#----------------------------creates the full graph with python dictionaries use .returngraph() to observe the output after executing this function -------------#
        def KeysToList(self,dictionary):
            keys=dictionary.keys()
            ListOfKeys=[list(keys)[i].strip('][').split(', ') for i in range(len(dictionary))]
            for i in range(len(ListOfKeys)):
                for j in range(len(ListOfKeys[0])):
                    ListOfKeys[i][j]=int(ListOfKeys[i][j])
            return ListOfKeys
                
        #now we have enough to creat the edges of the graph
        def CreateGraph(self):
            self.infograph()
            self.createvertice()
            self.Maxpro()
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
            
            
        def IdentifyGraph(self,P1=True,identdict=None):
            if P1:
                identdict=self.pointers
                Klists=self.KeysToList(self.pointers)
            else:
                Klists=self.KeysToList(identdict)
            for i in range(len(Klists)):
                test=[Klists[i][k]==self.Max[k] for k in range(len(Klists[0]))]
                #print(Klists[i])
                #print(self.pointers[f'{Klists[i]}'])
                if any(test):
                    #Record_of_connections=copy.deepcopy(identdict[f'{Klists[i]}'])
                    del identdict[f'{Klists[i]}']
                    #for k in range(len(Klists[0])):
                    #    if test[k]:
                    #        Klists[i][k]=0
                    #for n in range(len(Record_of_connections)):
                    #    for k in range(len(Klists[0])):
                    #        if P1:
                    #            if Record_of_connections[n][1][k]==self.Max[k]:
                    #                Record_of_connections[n][1][k]=0
                    #        else:
                    #            if Record_of_connections[n][k]==self.Max[k]:
                    #                Record_of_connections[n][k]=0
                    #    print(Klists[i])
                    #    identdict[f'{Klists[i]}'].append(Record_of_connections[n])
                else:
                    for n in range(len(identdict[f'{Klists[i]}'])):
                        #print(n)
                        for k in range(len(Klists[0])):
                            if P1:
                                if identdict[f'{Klists[i]}'][n][1][k]==self.Max[k]:
                                    identdict[f'{Klists[i]}'][n][1][k]=0
                            else:
                                if identdict[f'{Klists[i]}'][n][k]==self.Max[k]:
                                    identdict[f'{Klists[i]}'][n][k]=0   
                #print(Klists[i])
                #print(self.pointers[f'{Klists[i]}'])
            return identdict
        
        def IdentifyPrecube(self):
            for n in range(len(self.SPC)):
                self.IdentifyGraph(False,self.SPC[n])
            
#----------------------------creates the full graph with python dictionaries use .returngraph() to observe the output after executing this function -------------#

#-------------------------------------------------------------- simple alg for only full graph precubical  ------------------------------------------------------#
                    
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
        

     
        
        def singleRemoval(self,init_vertice,ElementOfPn,n=1):
            global number_Of_Elements_of_Pn_removed
            if n<len(ElementOfPn):
                nOfPn=-n+1
                n_plus_1_Of_Pn=-n
                for i in range(len(self.vertices)):
                    test1=[ self.vertices[i][j]<=init_vertice[j]<=ElementOfPn[j] for j in range(len(ElementOfPn))]
                    if sum(ElementOfPn)-sum(self.vertices[i])<n+2 and all(test1):
                        #print(self.vertices[i])
                        original_size=len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])
                        for l in range(len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])):
                            l=l-(original_size-len(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}']))
                            test2=[ ElementOfPn[j]<=self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l][j]  for j in range(len(ElementOfPn))]
                            #print(self.vertices[i])
                            #print(init_vertice)
                            #print(ElementOfPn)
                            #print(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l])
                            #print(test2)
                            if all(test2):
                                RemoveNext=copy.deepcopy(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l])
                                #print(ElementOfPn)
                                #print(RemoveNext)
                                if ElementOfPn in self.SPC[nOfPn][f'{init_vertice}']:
                                    print(f'We are in {ElementOfPn}(P{n}) and remove {ElementOfPn} in P{n}')
                                    self.SPC[nOfPn][f'{init_vertice}'].remove(ElementOfPn)
                                    number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
                                else:
                                    pass
                                if self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l] in self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}']:
                                    print(f'we are in  ({init_vertice}){ElementOfPn}(P{n}) and remove ({self.vertices[i]}){RemoveNext} in P{n+1} ')
                                    print(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])
                                    self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'].remove(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'][l])
                                    print(self.SPC[n_plus_1_Of_Pn][f'{self.vertices[i]}'])
                                    number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
                                    self.singleRemoval(self.vertices[i],RemoveNext,n+1)
                                else:
                                    pass
                            else:
                                pass
                    else:
                        pass
                if ElementOfPn in self.SPC[nOfPn][f'{init_vertice}']:
                    print(f'we are in {ElementOfPn}(P{n}) and remove {ElementOfPn} in P{n}')
                    self.SPC[nOfPn][f'{init_vertice}'].remove(ElementOfPn)
                    number_Of_Elements_of_Pn_removed=number_Of_Elements_of_Pn_removed+1
            else:
                pass
            print(number_Of_Elements_of_Pn_removed)
    #-------------------------------------------------------------------    
        def ResourceUpdater(self,string):
            #if P of resource x then +1 to resource utilization x
            #if P of resource x then -1 to resource utilization x
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
            #Here we create a python dictonary that stores the capacity of each resource and we will be able to individually change it
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
                                #print('')
                                #print(f'vertice que n temos o res {vertices[i]}')
                                #print(resource_info)
                                #print(f'vertice que recolhemos o res {verticeteste}')
                                self.Resourcetracker[f'{vertices[i]}'][resource_info[0]]=self.Resourcetracker[f'{vertices[i]}'][resource_info[0]]+resource_info[1]
                                #print(self.Resourcetracker[f'{vertices[i]}'])
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
        
        def PrunedGraph_FP(self,halfpruned=False):
            self.fullPreCubical()
            self.Cap_vertices()
            resources=list(self.cap.keys())
            for i in range(len(self.vertices)):
                test_vertice_cap=[self.Resourcetracker[f'{self.vertices[i]}'][resources[c]]<=self.cap[resources[c]] for c in range(len(self.cap))]
                if all(test_vertice_cap):
                        pass
                else:
                    edges_to_remove=[]
                    for e in range(len(self.pointers[f'{self.vertices[i]}'])):
                        edges_to_remove.append(self.pointers[f'{self.vertices[i]}'][e][1])
                    del self.pointers[f'{self.vertices[i]}']
                    for e in range(len(edges_to_remove)):
                        self.singleRemoval(self.vertices[i],edges_to_remove[e])
            #This removes edges that point to removed vertices
            if True:
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
                    
            
            
        #está incompleto, porque não podemos tirar as vertices com os recursos dentro das capacidades         
        def ForbidenGraph_FP(self):
            self.fullPreCubical()
            self.Cap_vertices()
            resources=list(self.cap.keys())
            track_Forbiden=[]
            for i in range(len(self.vertices)):
                test_vertice_cap=[self.Resourcetracker[f'{self.vertices[i]}'][resources[c]]<=self.cap[resources[c]] for c in range(len(self.cap))]
                if not all(test_vertice_cap):
                        pass
                else:
                    edges_to_remove=[]
                    for e in range(len(self.pointers[f'{self.vertices[i]}'])):
                        edges_to_remove.append(self.pointers[f'{self.vertices[i]}'][e][1])
                    del self.pointers[f'{self.vertices[i]}']
                    for e in range(len(edges_to_remove)):
                        self.singleRemoval(self.vertices[i],edges_to_remove[e])
                
        def subgraph(self,initial,final):
            coords=[]
            for k in range(len(initial)):
                coords.append([i for i in range(initial[k],final[k]+1)])
            test_elements=self.product(coords)
            sub=True
            for i in test_elements:
                try:
                    self.pointers[f'{i}']
                except:
                    sub=False
                    break
            print(sub)
    #-------------------------------------------------------------------    
        def returnvertices(self):
            return self.vertices
        
        def returnedges(self):
            return self.edges
        
        def returngraph(self):
            return self.pointers
        
        def returncap(self):
            return self.cap
        
                
        def returnfullPreCubical(self):
            return self.SPC       
        
        def GE_info(self,pruned=True,D=True):
            self.CreateGraph()
            self.fullPreCubical()
            if pruned:
                self.PrunedGraph_FP(D)
            else:
                self.ForbidenGraph_FP()
            self.IdentifyGraph()
            self.IdentifyPrecube()
            self.SPC.append(self.pointers)
            self.SPC.append(self.vertices)
            return self.SPC
#-------------------------------------------------------------- simple alg for only full graph precubical  ------------------------------------------------------#         