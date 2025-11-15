// Problem:  238. Product of Array Except Self
// Link: https://leetcode.com/problems/product-of-array-except-self/description/
// Notes: prefix and suffix prodcut store in array and do product later
// Level: Easy
// Pattern: prefix & sufix 
// Revisit: No

class Solution {
    public int[] productExceptSelf(int[] nums) {

         int n= nums.length;
          int pre[]=new int[n];
          int suff[]=new int[n];
          int result[]=new int[n];
        
         int sum=1;
         for(int i=0;i<n;i++){
           pre[i]=sum;
          sum*=nums[i];
         }
          sum=1;
         for(int i=n-1;i>=0;i--){
          suff[i]=sum;
          sum*=nums[i];
         }
         for(int i=0;i<n;i++){
          result[i]=pre[i]* suff[i];
         }
         return result;




    
    }
}
