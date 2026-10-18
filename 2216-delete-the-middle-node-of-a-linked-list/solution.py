# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def deleteMiddle(self, head: ListNode | None) -> ListNode | None:
        if head.next == None:
            return None
        slow, fast = head, head.next.next

        while fast != None and fast.next != None:
            prev = slow
            slow = slow.next
            fast = fast.next.next

        slow.next = slow.next.next

        return head
