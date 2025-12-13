// Problem: 102. Binary Tree Level Order Traversal
// Link: https://leetcode.com/problems/binary-tree-level-order-traversal/description//
// Notes:  use Queue interate over curr ques size remove elemet &  store every child in queue
// Level: Easy
// Pattern: Tree BFS
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
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if(root==null)
         return result;

        Queue<TreeNode> que= new LinkedList<>();
        que.add(root);

        while(!que.isEmpty()){
          
            List<Integer> list= new ArrayList<>();
            int size= que.size();
            for( int i=0;i<size;i++){
             TreeNode node =que.poll();
             list.add(node.val);
             if(node.left!=null)que.add(node.left);
             if(node.right!=null)que.add(node.right);

            }
            result.add(list);
        }



        return result;

        
    }
}
