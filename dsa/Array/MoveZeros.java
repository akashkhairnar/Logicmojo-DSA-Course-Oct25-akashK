// Problem: 283-Move Zeroes
//Link: https://leetcode.com/problems/move-zeroes/description/
// Recap: Count zeros and if count>0 then swap no by that much index.


public void moveZeroes(int[] nums) {
        int count=0;

        for( int i=0;i<nums.length;i++){
        if(nums[i]==0)
        count++;
        else if(count>0){
        nums[i-count]=nums[i];
        nums[i]=0;
        }
        }

}