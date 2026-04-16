# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        def countAllNodes(temp):
            if not temp:
                return 0
            def countLeft(node):
                h = 0
                while node:
                    h += 1
                    node = node.left
                return h
            def countRight(node):
                h = 0
                while node:
                    h += 1
                    node = node.right
                return h
            left = countLeft(temp)
            right = countRight(temp)
            if left == right:
                return (1 << left) - 1 # equals  to 2 ** left
            return 1 + countAllNodes(temp.left) + countAllNodes(temp.right)
        return countAllNodes(root)