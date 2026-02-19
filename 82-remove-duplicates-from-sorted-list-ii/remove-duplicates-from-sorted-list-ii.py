class Solution:
    def deleteDuplicates(self, head):
        dummy = ListNode(0)
        dummy.next = head
        
        prev = dummy
        curr = head
        
        while curr:
             
            # Case 1: duplicate found
            if curr.next and curr.val == curr.next.val:
                
                # move curr until value changes
                while curr.next and curr.val == curr.next.val:
                    curr = curr.next
                
                # skip all duplicates
                prev.next = curr.next
            
            else:
                # value is unique, move prev
                prev = prev.next
            
            curr = curr.next
        
        return dummy.next
