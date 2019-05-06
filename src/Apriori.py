from __future__ import division
import math

f=open("config.csv",'r')
data=f.read()
data=data.split('\n')
m={}
for i in range(0,5):
	d=data[i].split(',')
	m[d[0]]=d[1]
inputfile=m['input']
outputfile=m['output']
support=float(m['support'])
confidence=float(m['confidence'])
flag=int(m['flag'])
Frequent_Itemsets=[]
Association_Rules_lhs=[]
Association_Rules_rhs=[]

input_data=[]
f=open(inputfile,'r')
for line in f:
	line=(line.strip()).split(',')
	if len(line[0])!=0:
		input_data.append(line)

for i in range(0,len(input_data)):
	input_data[i].sort()

Nodes=[]
Distinct_itemsets=set()

class Node:
	Name=''
	Value=0
	Children={}

Nodes.append(Node())
Nodes[0].Name='null'
Nodes[0].Value=0
Nodes[0].Children={}

def addchild(parent_pos,child_data):
	Nodes[parent_pos].Children[child_data]=len(Nodes)
	Newnode=Node()
	Newnode.Name=child_data
	Newnode.Value=1
	Newnode.Children={}
	Nodes.append(Newnode)

def search(data,position):
	childs=Nodes[position].Children
	if len(childs)==0 or len(data)==0:
		return 0
	ans=0
	for j in childs:
		if j<data[0]:
			ans+=search(data,childs[j])
		elif j==data[0] and len(data)>1:
			ans+=search(data[1:],childs[j])
		elif j==data[0] and len(data)==1:
			ans+=Nodes[childs[j]].Value

	return ans

def insert(data):
	current_node_pos=0
	found_pos_till=0
	while found_pos_till < len(data):
		
		childs=Nodes[current_node_pos].Children
		f=0
		for j in childs:
			if j == data[found_pos_till]:
				f=1
				current_node_pos=childs[j]
				Nodes[current_node_pos].Value+=1
				break

		if f==0:
			addchild(current_node_pos,data[found_pos_till])
			current_node_pos=len(Nodes)-1

		found_pos_till+=1

def print_trie():
	for i in range(0,len(Nodes)):
		print Nodes[i].Name,Nodes[i].Value,Nodes[i].Children

def Association_Rules(data,lhs,rhs,confidence):
	# print data,lhs,rhs
	for i in range(0,len(lhs)):
		lhs[i].sort()
		rhs[i].sort()

	crossed_lhs=[]
	crossed_rhs=[]
	p=search(data,0)
	for i in range(0,len(lhs)):
		q=search(lhs[i],0)
		if p>=confidence*q:
			crossed_lhs.append(lhs[i])
			crossed_rhs.append(rhs[i])

	if len(crossed_lhs)==0 or len(lhs)==0 or len(crossed_lhs[0])==0 or len(lhs[0])==0:
		return

	global Association_Rules_lhs
	global Association_Rules_rhs

	Association_Rules_lhs= Association_Rules_lhs+crossed_lhs
	Association_Rules_rhs=Association_Rules_rhs+crossed_rhs

	pruned_lhs=[]
	pruned_rhs=[]
	for i in range(0,len(crossed_rhs)):
		for j in range(i+1,len(crossed_rhs)):
			if crossed_rhs[i][:len(crossed_rhs[i])-1] == crossed_rhs[j][:len(crossed_rhs[j])-1]:
				lis=crossed_rhs[i][:len(crossed_rhs[i])-1]
				lis.append(crossed_rhs[i][len(crossed_rhs[i])-1])
				lis.append(crossed_rhs[j][len(crossed_rhs[j])-1])
				pruned_rhs.append(lis)

	for i in range(0,len(pruned_rhs)):
		pruned_lhs.append(list(set(data).difference(pruned_rhs[i])))

	Association_Rules(data,pruned_lhs,pruned_rhs,confidence)

count_itemsets=0

def Getfreq_itemsets(data,frequency,confidence,flag):
	# print data
	for i in range(0,len(data)):
		data[i].sort()

	crossed_data=[]

	for i in range(0,len(data)):
		if search(data[i],0)>=frequency:
			crossed_data.append(data[i])

	if len(crossed_data)==0 or len(data)==0 or len(crossed_data[0])==0 or len(data[0])==0:
		return 

	global Frequent_Itemsets
	Frequent_Itemsets=Frequent_Itemsets+crossed_data

	#calling rules
	if flag==1:
		for i in range(0,len(crossed_data)):
			lhs=[]
			rhs=[]
			if len(crossed_data[i])>1:
				for j in range(0,len(crossed_data[i])):
					lhs.append(crossed_data[i][0:j]+crossed_data[i][j+1:len(crossed_data[i])])
					rhs.append([crossed_data[i][j]])
					# print rhs
				Association_Rules(crossed_data[i],lhs,rhs,confidence)

	next_level=[]
	for i in range(0,len(crossed_data)):
		for j in range(i+1,len(crossed_data)):
			if crossed_data[i][:len(crossed_data[i])-1] == crossed_data[j][:len(crossed_data[j])-1]:
				# print crossed_data[i][:len(crossed_data[i])-1]
				lis=crossed_data[i][:len(crossed_data[i])-1]
				lis.append(crossed_data[i][len(crossed_data[i])-1])
				lis.append((crossed_data[j][len(crossed_data[j])-1]))
				# print lis
				next_level.append(lis)

	Getfreq_itemsets(next_level,frequency,confidence,flag)


for i in range(0,len(input_data)):
	insert(input_data[i])
	for j in range(0,len(input_data[i])):
		Distinct_itemsets.add(input_data[i][j])

Frequency=support*len(input_data)
Distinct_itemList=list(Distinct_itemsets)

initial_input=[]
for i in range(0,len(Distinct_itemList)):
	initial_input.append([Distinct_itemList[i]])

Getfreq_itemsets(initial_input,Frequency,confidence,flag)

f=open(outputfile,'w')
f.write(str(len(Frequent_Itemsets)))
f.write('\n')
for i in range(0,len(Frequent_Itemsets)):
	 f.write(','.join(Frequent_Itemsets[i]))
	 f.write('\n')

if flag==1:
	f.write(str(len(Association_Rules_lhs)))
	f.write('\n')
	for i in range(0,len(Association_Rules_lhs)):
		f.write(','.join(Association_Rules_lhs[i])+",=>,"+','.join(Association_Rules_rhs[i]))
		f.write('\n')