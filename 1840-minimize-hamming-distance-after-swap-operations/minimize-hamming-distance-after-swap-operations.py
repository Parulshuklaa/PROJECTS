class Solution:
    def minimumHammingDistance(self, source: List[int], target: List[int], allowedSwaps: List[List[int]]) -> int:
        n = len(source)
        g = defaultdict(list)
        for u, v in allowedSwaps:
            g[u].append(v)
            g[v].append(u)
        groups = []
        vis = [False] * n
        
        def dfs(u, group):
            if vis[u]:
                return
            group.append(u)
            vis[u] = True
            for v in g[u]:
                dfs(v, group)
        
        res = 0
        for i in range(n):
            if i not in g:
                res += source[i] != target[i]
            elif not vis[i]:
                group = []
                dfs(i, group)
                groups.append(group)
        for group in groups:
            s = defaultdict(int)
            for i in group:
                s[source[i]] += 1
            for i in group:
                cur = target[i]
                if cur in s:
                    s[cur] -= 1
                    if s[cur] == 0:
                        del s[cur]
            res += sum(s.values())
        return res