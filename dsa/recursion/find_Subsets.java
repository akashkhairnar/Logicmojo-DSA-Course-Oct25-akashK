// Problem:  78. Subsets
// Link: https://leetcode.com/problems/subsets/description/
// Notes:  subsequence pattern to pick and not pick current element dual recursion call
// Level: Medium 
// Pattern: backtracking
// Revisit: Yes

class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result= new ArrayList<>();
      List<Integer> list= new ArrayList<>();
        helper(0,nums,list,result);
        return result;
        
    }
    private void helper(int index,int[] nums,List<Integer> list,List<List<Integer>> result){

        if(index >= nums.length){    //base case
            result.add(new ArrayList<>(list));  // Because at each recursion state, we want to freeze the current contents permanently.
                                              //  new ArrayList<>(list) creates a new independent list object with the same values.
            return;
        }
        list.add(nums[index]);   //pick element
        helper(index+1,nums,list,result); // call to pick next element after curent pick
        list.remove(list.size()-1);    // not pick
        helper(index+1,nums,list,result);  // call to pick next once 
    }
}
