class Solution: 
    def sortedArrayToBST(self, n: list[int]) -> TreeNode:

        if not n: return None                                           # <-- base case: leaf
        m = len(n)//2

        return TreeNode(n[m],self.sortedArrayToBST(n[:m]),              # <-- left  subtree
                             self.sortedArrayToBST(n[m+1:]))            # <-- right subtree