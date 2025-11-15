// Problem:  26. Remove Duplicates frm sorted Array
// Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/description
// Notes: two pointer if find different element then update element of slow 
// Level: Easy
// Pattern: Two Pointer
// Revisit: no


class Solution {
    public int removeDuplicates(int[] nums) {
        int i=0;
        int j=i+1;
        int n= nums.length;

        while(j<n){
            if(nums[i]==nums[j]){
                j++;
            }
            else if(nums[i]!=nums[j]){
                i++;
                nums[i]=nums[j];
                j++;
            }
             
        }
        return i+1;
        
    }
}
