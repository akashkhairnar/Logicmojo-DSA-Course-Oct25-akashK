

// Problem: 543. Diameter of Binary Tree
// Link: https://leetcode.com/problems/diameter-of-binary-tree/description/
// Notes:  calculate height of each left and right each node max dia and lh+rh is ans 
// Level: Easy
// Pattern:  DFS 
// Revisit: no




/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    int diameter = 0;

    public int diameterOfBinaryTree(TreeNode root) {
        height(root);
        return diameter;
    }

    int height(TreeNode node) {
        if (node == null)
            return 0;
        int hl = height(node.left);
        int hr = height(node.right);

        diameter = Math.max(diameter, hl + hr);
        return 1 + Math.max(hl, hr);
    }
}
