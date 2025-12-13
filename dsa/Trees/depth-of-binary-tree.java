// Problem: 104. Maximum Depth of Binary Tree
// Link: https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
// Notes:  height of BST = 1 + Math.max( height(root.left),height(root.right))  (DFS)
// Level: Easy
// Pattern: DFS
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
    public int maxDepth(TreeNode root) {
         if(root==null)
          return 0;

       return 1+ Math.max(maxDepth(root.left),maxDepth(root.right));
    }
}
