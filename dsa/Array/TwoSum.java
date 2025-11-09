// Problem:  Two Sum
// Link: https://leetcode.com/problems/two-sum/description/.
// Notes: Use map to store num[i],index.
// Level: Easy
// Pattern: HashMap (Complement Pattern)
// Revisit: No
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> store = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int remain = target - nums[i];

            if (store.containsKey(remain)) {
                return new int[] { i, store.get(remain) };
            }
            store.put(nums[i], i);
        }
        return new int[] {};
    }
}