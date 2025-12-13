// Problem: 226. Invert Binary Tree
// Link: https://leetcode.com/problems/invert-binary-tree/description/
// Notes:  Swap left child and right child if current node is not null
// Level: Easy
// Pattern: Recursion DFS(PREORDER)
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
    public TreeNode invertTree(TreeNode root) {
        TreeNode newRoot = root;

        helper(newRoot);
        return newRoot;
    }

    void helper(TreeNode root){
        if(root==null)
         return;
       TreeNode temp= root.left;
       root.left= root.right;
       root.right= temp;
       helper(root.left);
       helper(root.right);
    }
}
