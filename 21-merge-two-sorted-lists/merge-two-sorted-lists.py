# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        h = p = None
        
        while l1 and l2:
            if l1.val < l2.val:
                temp = l1
                l1 = l1.next
            else:
                temp = l2
                l2 = l2.next
            
            temp.next = None
            
            if h is None:
                h = p = temp
            else:
                p.next = temp
                p = temp
        
        # attach remaining nodes
        remaining = l1 if l1 else l2
        
        if h is None:
            return remaining
        
        p.next = remaining
        return h