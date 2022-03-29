import sys
import re
sys.setrecursionlimit(40000)
from collections import deque
sozd_gr=False
tip=''
nach=0
poi=''
graf=dict()
visited_dfs=set()
visited_bfs = []
queue = deque()

for line in sys.stdin:
	ctr=line.split()
	if sozd_gr ==False:
		if (ctr[0]=='u' or 'd'):
			tip=ctr[0]
		nach=ctr[1]
		if (ctr[0]=='d' or 'b'):
			poi=ctr[2]
		sozd_gr=True

	if (sozd_gr ==True) and (len(ctr)==2):
		if tip=='u':
			key=ctr[0]
			if(key not in graf):
				graf[key]=[]
			if(ctr[1] not in graf):
				graf[ctr[1]]=[]
			graf[key].append(ctr[1])
			graf[ctr[1]].append(ctr[0])
		
		if (tip=="d"):
			key=ctr[0]
			if(key not in graf):
				graf[key]=[]
				
			if(ctr[1] not in graf):
				graf[ctr[1]]=[]
			graf[key].append(ctr[1])


for i in graf:
    graf[i].sort()


def bfs(visited, graph, start):

  visited.append(start)
  queue.append(start)

  while queue:
    s = queue.popleft() 
    print (s) 
    for sosed in graph[s]:
      if sosed not in visited:
        visited.append(sosed)
        queue.append(sosed)



def dfs(visited, graph, start):
    if start not in visited:
        print (start)
        visited.add(start)
        for sosed in graph[start]:
            dfs(visited, graph, sosed)

if poi=='d':
	dfs(visited_dfs,graf,nach )
if poi=='b':
	bfs(visited_bfs, graf, nach)