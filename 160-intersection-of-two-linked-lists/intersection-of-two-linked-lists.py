# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        d = {}

        # Store all nodes from list A
        while headA:
            d[headA] = True
            headA = headA.next

        # Check nodes from list B
        while headB:
            if headB in d:
                return headB
            headB = headB.next

        return None
