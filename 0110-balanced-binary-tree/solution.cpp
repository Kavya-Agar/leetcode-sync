/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isBalanced(TreeNode* root) {
        return findHeight(root) != -1;
    }

    int findHeight(TreeNode* root) {
        if (root == nullptr) return 0;

        int leftHeight = findHeight(root->left);
        if (leftHeight == -1) return -1;

        int rightHeight = findHeight(root->right);
        if (rightHeight == -1) return -1;

        if(abs(leftHeight - rightHeight) > 1) return -1;

        return (std::max(leftHeight, rightHeight)) + 1;
    }
}; 
