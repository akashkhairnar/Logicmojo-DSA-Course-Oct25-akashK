// Problem:  167. Two Sum II - Input Array Is Sorted
// Link: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/
// Notes:  modified bimaey search(as it is sorted) 
// Level: Easy
// Pattern: Two Pointer
// Revisit: no
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

class Solution {

    public int[] twoSum(int[] arr, int target) {
    
     
     // nlong(n) with binsary search for each element
    //     int len= numbers.length;
    //     for(int i=0;i<len-1;i++){
    //         int ans=search(i+1, len-1,target-numbers[i],numbers);
    //        if(ans!=-1){
    //          return new int[]{i+1,ans+1};
    //        }
    //     }
    //     return new int[]{};
        
    // }

    //  int search(int l, int h,int target,int[]arr){
    //     while(l<=h){
    //           int mid= (l+h)/2;
    //         if(arr[mid]==target){
    //              return mid;
    //         }
    //         else if(arr[mid]>target)
    //          h=mid-1;
    //         else
    //          l=mid+1;
    //     }
    //     return -1;

     int n= arr.length;
      int i=0;
      int j=n-1;
      while(i<j){
        int sum= arr[i]+arr[j];
        if(target== sum){
            return new int[]{i+1,j+1};
        }
        else if(sum>target)
           j--;
        else
          i++;

      }
       return new int[]{};

    }
}
