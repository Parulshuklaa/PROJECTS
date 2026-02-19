# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def rotateRight(self, head, k):
        if not head:
            return head
        
        n = 1 
        curr = head 
        while curr: 
            if curr.next == None :
                curr.next = head 
                break 
            curr = curr.next 
            n+=1 

        k = k%n  #the number of nodes that get rotated
        curr = head
        for i in range(n-k-1):
            curr = curr.next
        head = curr.next   #Assign the new head
        curr.next = None   #Break the linked list to create the new tail

        return head


