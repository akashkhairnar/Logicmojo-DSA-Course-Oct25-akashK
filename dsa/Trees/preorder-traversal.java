// Problem: 144. Binary Tree Preorder Traversal
// Link: https://leetcode.com/problems/binary-tree-preorder-traversal/description/
// Notes:  ROOT->LEFT->RIGHT
// Level: Easy
// Pattern: recursion
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
    public List<Integer> preorderTraversal(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        helper(result, root);
       return result;
    }
    void helper(List<Integer>list, TreeNode node){
      if( node==null)
        return;
      list.add(node.val);
      helper(list,node.left);
      helper(list,node.right);
    }
}
