// Problem: 701. Insert into a Binary Search Tree
// Link: https://leetcode.com/problems/insert-into-a-binary-search-tree/description/
// Notes:  both way recursion & iteration
// Level: Easy
// Pattern: Simple BST
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
    public TreeNode insertIntoBST(TreeNode root, int val) {
        TreeNode node = new TreeNode(val);
        if(root==null){
            root= node;
            return root;
        }
      TreeNode curr= root;
      while( curr!=null){
         if(val< curr.val){
            if(curr.left==null){
             curr.left =node;
             return root;
            }
            curr= curr.left;
         }
         else{
             if(curr.right==null){
             curr.right =node;
             return root;
            }
            curr= curr.right;
         }
      }
      return null;
        
    }
  // recursive
  public TreeNode insertIntoBST2(TreeNode root, int val) {
       if(root ==null)
      return new TreeNode(val);

    if(root.val<val)
      root.right=  insertIntoBST(root.right,val);
    else
       root.left= insertIntoBST(root.left,val);

    return root;
        
    }
}
