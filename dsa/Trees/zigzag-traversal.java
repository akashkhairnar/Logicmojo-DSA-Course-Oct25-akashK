// Problem: 103. Binary Tree Zigzag Level Order Traversal
// Link: https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
// Notes:  BFS just when we are adding to list use addLast and addFirst alternate
// Level: Easy
// Pattern:  BFS
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
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();

        levelOrder(root, result);
        return result;
    }

    void levelOrder(TreeNode root, List<List<Integer>> result) {

        if (root == null)
            return;

        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        boolean flag = true;
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (flag)
                    list.addLast(node.val);
                else
                    list.addFirst(node.val);
                if (node.left != null)
                    queue.add(node.left);
                if (node.right != null)
                    queue.add(node.right);

            }

            result.add(list);
            flag = !flag;
        }

    }

}
