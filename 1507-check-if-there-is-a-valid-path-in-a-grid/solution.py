from collections import deque

class Solution:
    def hasValidPath(self, grid: List[List[int]]) -> bool:
        m = len(grid)
        n = len(grid[0])

        dirs = {
            1: [(0, -1), (0, 1)],
            2: [(-1, 0), (1, 0)],
            3: [(0, -1), (1, 0)],
            4: [(0, 1), (1, 0)],
            5: [(0, -1), (-1, 0)],
            6: [(0, 1), (-1, 0)]
        }

        q = deque([(0, 0)])
        visited = set([(0, 0)])

        while q:
            x, y = q.popleft()

            if (x, y) == (m - 1, n - 1):
                return True
            
            for dx, dy in dirs[grid[x][y]]:
                nr, nc = x + dx, y + dy
            
                if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                    for bdx, bdy in dirs[grid[nr][nc]]:

                        if nr + bdx == x and nc + bdy == y:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            break
                
        return False
