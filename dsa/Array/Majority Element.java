// Problem:  169. Majority Element
// Link: https://leetcode.com/problems/majority-element/description/
// Notes:  Moore Voting Algorithm. maintain frequency & max element
// Level: Easy
// Pattern: Moore Voting Algorithm. 
// Revisit: no

class Solution {
    public int majorityElement(int[] nums) {
    // extra space
    //     Map<Integer,Integer> map= new HashMap<>();
    //    int n=nums.length;
    //     for(int i=0;i<n;i++){
    //         if(map.containsKey(nums[i])){
    //             map.put(nums[i],map.get(nums[i])+1);
    //         }
    //         else
    //         map.put(nums[i],1);
    //     }
      

    //     for(Integer key: map.keySet()){
    //         if(map.get(key)>n/2)
    //            return key;
    //     }
    //     return -1;
        
    // }

    int n= nums.length;

    int ans= nums[0] , feq=1;

    for( int i=1;i<n;i++){
        if (nums[i]==ans){
            feq++;
        }
        else{
            feq--;
            if(feq==0){
             ans= nums[i];
             feq=1;
            }
        }
    }
    return ans;
}
}
