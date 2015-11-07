import networkx as nx 
import numpy as np
from scipy import linalg as LA
"""
def create_graph(infile1):
	with open(infile1,'r+') as f:
		AdjMatrix = f.readlines() ;
	AdjMatrix=[ [int(s) for s in row.rstrip("\n").split()] for row in AdjMatrix ];
	G=nx.Graph()
	for i in range(0,len(AdjMatrix)):
		for j in range(0,len(AdjMatrix[i])):
			if i < j and AdjMatrix[i][j]==1 :	
				G.add_edge(i,j)
	return G
"""
def to_file(data,outFile):
	with open(outFile,'w') as f :
		for row in data:
	  		f.write("%s\n" %row)

def get_nodes(infile):
	with open(infile,'r+') as f:
		AdjMatrix = f.readlines() ;
	EdgeList=[]
	for row in AdjMatrix :
		EdgeList.extend(row.rstrip("\n").split())
	return list(set(EdgeList))
	
def create_graph(infile1):
	with open(infile1,'r+') as f:
		AdjMatrix = f.readlines() ;
	EdgeList=[ [s for s in row.rstrip("\n").split()] for row in AdjMatrix ];
	G=nx.Graph()
	for i in range(0,len(EdgeList)):
		for j in range(1,len(EdgeList[i])):
			G.add_edge(EdgeList[i][0],EdgeList[i][j])
	return G


def ele_matrix_multiply(infile1,AdjMat,outFileMult,outFileEigVal,outFileEigVec):
	with open(infile1,'r+') as f:
		matrix1 = f.readlines() ;
	matrix1=[ row.rstrip("\n").split() for row in matrix1 ];
	
	nmatrix=[[float(matrix1[i][j])*float(AdjMat[i][j]) for j in range(0,len(matrix1[i]))] for i in range(0,len(matrix1))];
	e_vals, e_vecs = LA.eig(A)
	to_file(nmatrix,outFileMult)
	to_file(e_vals,outFileEigVal)
	to_file(e_vecs,outFileEigVec)
	
def get_HM(a,b):
	if a+b==0 :
		return 0.00;
	else :
		return float(2*a*b/(a+b));

def get_weight(val,outFile):
	WeightMatrix= [[get_HM(val[i],val[j]) for j in range(0,len(val))] for i in range(0,len(val))]
	with open(outFile,'w') as f :
		for row in WeightMatrix:
			for j in range(0,len(row)):
	  			f.write("%0.03f " %row[j])
			f.write("\n")


"""
def get_DCweight(infile1):
	with open(infile1,'r+') as f:
		AdjMatrix = f.readlines() ;
	AdjMatrix=[ [int(s) for s in row.rstrip("\n").split()] for row in AdjMatrix ];
	degree=[ sum(row) for row in AdjMatrix];
	WeightMatrix= [[get_HM(degree[i],degree[j]) for j in range(0,len(degree))] for i in range(0,len(degree))]
	with open("weight.txt",'w') as f :
		for row in WeightMatrix:
			for j in range(0,len(row)):
	  			f.write("%0.03f " %row[j])
			f.write("\n")
"""			
def ndegree(k,v,d2,nodelist):
	if k in nodelist :
		return d2[k];
	else :
		return 0;
	
def intersect(d1,d2,nodelist):
	a=[ ndegree(k,v,d2,nodelist) for k,v in d1.iteritems() ]
	return a;

nodelist=get_nodes("btp1.csv")
G=create_graph("btp.csv")
G1=G.subgraph(nodelist)
subdegree=intersect(nx.degree(G),nx.degree(G1),nodelist)
subbc=intersect(nx.betweenness_centrality(G),nx.betweenness_centrality(G1),nodelist)	
get_weight(nx.degree(G).values(),"dc_weight.txt")
get_weight(subdegree,"dc_recent_weight.txt")
get_weight(nx.betweenness_centrality(G).values(),"bc_recent_weight.txt")
A = nx.to_numpy_matrix(G)
AdjMat=A.tolist()
ele_matrix_multiply("dc_weight.txt",AdjMat,"DCwmatrix.txt","DCEigVal.txt","DCEigVec.txt")
ele_matrix_multiply("dc_recent_weight.txt",AdjMat,"DCwrecentmatrix.txt","DCrecentEigVal.txt","DCrecentEigVec.txt")
ele_matrix_multiply("bc_weight.txt",AdjMat,"BCwmatrix.txt","BCEigVal.txt","BCEigVec.txt")
ele_matrix_multiply("bc_recent_weight.txt",AdjMat,"BCwrecentmatrix.txt","BCrecentEigVal.txt","BCrecentEigVec.txt")

