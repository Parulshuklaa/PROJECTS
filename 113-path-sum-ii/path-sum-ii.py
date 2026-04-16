class Solution:
    def pathSum(self, root, targetSum):
        result = []

        def dfs(node, path, remaining):
            if not node:
                return
            
            path.append(node.val)
            remaining -= node.val

            # Check if it's a leaf and sum matches
            if not node.left and not node.right and remaining == 0:
                result.append(list(path))
            
            dfs(node.left, path, remaining)
            dfs(node.right, path, remaining)

            # Backtrack
            path.pop()

        dfs(root, [], targetSum)
        return result