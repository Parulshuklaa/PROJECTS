class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        target = len(graph) - 1
        res = [] 
        stack = [(0, [0])]
        while stack :
            node , path = stack.pop()
            if node == target : 
                res.append(path)
            for side in graph[node]: 
                stack.append((side, path + [side]))
        return res 



