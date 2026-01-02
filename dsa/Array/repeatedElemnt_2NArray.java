// Problem:  961. N-Repeated Element in Size 2N Array
// Link: https://leetcode.com/problems/n-repeated-element-in-size-2n-array/description/
// Notes:  Pigeonhole Principle  The repeated element takes up EXACTLY 50% of the array Key observation 2: With 50% density, the element can't be spread too far apart Critical insight: In any window of 3 consecutive elements, the repeated element MUST appear at least twice
// Level: EASY
// Pattern: Sliding Window
// Revisit: yes
class Solution {
    public int repeatedNTimes(int[] nums) {
    //    Set<Integer> set = new HashSet<>();

    //     for (int num : nums) {
    //         if (set.contains(num)) {
    //             return num; // duplicate found
    //         }
    //         else
    //          set.add(num);
    //     }
    //     return -1;

   // pigeon hole principle
    int n= nums.length;
   for( int i=0;i<n-2;i++){
     if( nums[i]==nums[i+1]|| nums[i]==nums[i+2])
      return nums[i];
    
   }
   return nums[n-1];

    }
    
}
