# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        sp = fp = head
        while fp:
            sp = sp.next
            if fp.next == None:
                return False
            fp = fp.next.next
            if sp == fp:
                return True
        return False