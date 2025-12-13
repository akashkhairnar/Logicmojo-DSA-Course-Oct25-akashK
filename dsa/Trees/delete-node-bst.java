// Problem: 450. Delete Node in a BST
// Link: https://leetcode.com/problems/delete-node-in-a-bst/description/
// Notes:  Leaf Node: Just delete it.  One Child: Replace node with its only child.  Two Children: Replace with inorder predecessor (rightmost of left subtree) or inorder successor (leftmost of right subtree). We’ll use predecessor here.
// Level: Medium
// Pattern: basic Tree
// Revisit: YES


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
    public TreeNode deleteNode(TreeNode root, int key) {
       if(root==null) return null;
       return helper(root, key);
        
    }
   TreeNode helper(TreeNode root, int key){
        if(root==null) return null;
        if(key<root.val)
        root.left= helper(root.left, key);
        else if (key>root.val)
        root.right= helper(root.right, key);
        else{
          if (root.left==null & root.right==null)
            return null;
          if(root.left==null)
           return root.right;
          if (root.right==null)
           return root.left;
          
        TreeNode next= findNext(root.right);
        root.val=next.val;
       root.right= helper(root.right,next.val);
        }
        return root;


    }

    TreeNode findNext(TreeNode node){
        while(node.left!=null)
         node= node.left;

        return node;
        
    }
      
}
