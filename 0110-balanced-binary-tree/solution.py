# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        balancedCheck = True
        def dfs(node):
            nonlocal balancedCheck
            if not node:
                return 0
            leftHeight,rightHeight = dfs(node.left)+1, dfs(node.right)+1
            if abs(leftHeight-rightHeight) > 1:
                balancedCheck = False
            return max(leftHeight,rightHeight)
        dfs(root)
        return balancedCheck
            

            
        
