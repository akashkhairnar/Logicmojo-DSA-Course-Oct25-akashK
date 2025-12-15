// Problem: Top View of BT
// Link: https://takeuforward.org/plus/dsa/problems/top-view-of-bt?tab=description
// Notes:  we need store width an Node everytime in queue. Maintain treemap so that we can store in sorted order by width (BFS)
// Level: Medium
// Pattern:  BFS
// Revisit: YES





/**
 * Definition for a binary tree node. public class TreeNode { int data; TreeNode left; TreeNode
 * right; TreeNode(int val) { data = val; left = null, right = null } }
 */
class Solution {
  class Pair {
    TreeNode node;
    int width;

    public Pair(TreeNode node, int width) {
      this.node = node;
      this.width = width;
    }
  }

  public List<Integer> topView(TreeNode root) {
    // your code goes here

    List<Integer> result = new ArrayList<>();
    helper(root, 0, result);
    return result;
  }

  public void helper(TreeNode root, int index, List<Integer> list) {

    if (root == null) return;

    Queue<Pair> queue = new LinkedList<>();
    queue.add(new Pair(root, 0));
    Map<Integer, Integer> map = new TreeMap<>(); // sorted by distance

    while (!queue.isEmpty()) {

      Pair pair = queue.poll();
      TreeNode node = pair.node;

      if (!map.containsKey(pair.width)) {
        map.put(pair.width, node.data);
      }
      if (node.left != null) queue.add(new Pair(node.left, pair.width - 1));
      if (node.right != null) queue.add(new Pair(node.right, pair.width + 1));
    }
    list.addAll(map.values());
  }
}
