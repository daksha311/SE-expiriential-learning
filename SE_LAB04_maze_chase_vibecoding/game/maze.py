import random
from collections import deque

import pygame

CELL = 44
WALL_THICKNESS = 4


def generate_maze(cols, rows):
    visited = [[False]*cols for _ in range(rows)]
    walls = [[[True,True,True,True] for _ in range(cols)] for _ in range(rows)]
    def neighbors(r,c):
        dirs=[(-1,0,0,1),(1,0,1,0),(0,1,2,3),(0,-1,3,2)]
        res=[]
        for dr,dc,wd,od in dirs:
            nr,nc=r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and not visited[nr][nc]:
                res.append((nr,nc,wd,od))
        return res
    stack=[(0,0)]
    visited[0][0]=True
    while stack:
        r,c=stack[-1]
        nbrs=neighbors(r,c)
        if nbrs:
            nr,nc,wd,od=random.choice(nbrs)
            walls[r][c][wd]=False
            walls[nr][nc][od]=False
            visited[nr][nc]=True
            stack.append((nr,nc))
        else:
            stack.pop()
    return walls


def build_wall_rects(walls, rows, cols):
    """Turn the wall flags into solid rects so the player can collide with them.
    Wall order per cell: 0=top, 1=bottom, 2=right, 3=left."""
    t = WALL_THICKNESS
    h = t // 2
    rects = []
    for r in range(rows):
        for c in range(cols):
            x, y = c*CELL, r*CELL
            w = walls[r][c]
            if w[0]: rects.append(pygame.Rect(x-h, y-h, CELL+t, t))
            if w[3]: rects.append(pygame.Rect(x-h, y-h, t, CELL+t))
            if r == rows-1 and w[1]: rects.append(pygame.Rect(x-h, y+CELL-h, CELL+t, t))
            if c == cols-1 and w[2]: rects.append(pygame.Rect(x+CELL-h, y-h, t, CELL+t))
    return rects


def bfs(walls, start, goal, rows, cols):
    """Return next step direction from start toward goal using BFS."""
    sr,sc=start; gr,gc=goal
    queue=deque([(sr,sc,[])])
    visited={(sr,sc)}
    dir_map={0:(-1,0),1:(1,0),2:(0,1),3:(0,-1)}
    while queue:
        r,c,path=queue.popleft()
        if r==gr and c==gc:
            return path[0] if path else None
        for d,(dr,dc) in dir_map.items():
            if not walls[r][c][d]:
                nr,nc=r+dr,c+dc
                if (nr,nc) not in visited and 0<=nr<rows and 0<=nc<cols:
                    visited.add((nr,nc))
                    queue.append((nr,nc,path+[(dr,dc)]))
    return None