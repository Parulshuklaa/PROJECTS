class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        routes = path.split('/')
        # if path = "/.../a/../b/c/../d/./"
        # then routes = ['', '...', 'a', '..', 'b', 'c', '..', 'd', '.', '']
        for route in routes:
            if route == "" or route == ".":
                continue
            elif route == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(route)
        
        return "/" + "/".join(stack)