// Problem: 235. Lowest Common Ancestor of a Binary Search Tree
// Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/
// Notes: if both descendants greater than root then check right tree if smaller then left tree else root is ans.
// Level: Easy
// Pattern: DFS 
// Revisit: no


/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */

class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {

        if (root == null)
            return null;
        if (p.val < root.val && q.val < root.val)
            return lowestCommonAncestor(root.left, p, q);
        if (p.val > root.val && q.val > root.val)
            return lowestCommonAncestor(root.right, p, q);
        return root;
    }
}
