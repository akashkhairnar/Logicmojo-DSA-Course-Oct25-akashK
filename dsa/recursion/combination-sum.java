// Problem:  39. Combination Sum
// Link: https://leetcode.com/problems/combination-sum/description/
// Notes:  same pattern pick not pick just we can pick same element mutiple time  so not inc that time Also handle other cases
// Level: Medium
// Pattern:  backtracking
// Revisit: Yes



class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
  List<List<Integer>> result = new ArrayList<>();
  List<Integer> list = new ArrayList<>();
        helper(0, candidates, target, list,result);
        return result;
    }

    void helper(int i, int[] candidates, int target, List<Integer> list,List<List<Integer>> result ){

    if (target==0) {
        result.add(new ArrayList<>(list));
        return;
    }
    if(target<0 || i == candidates.length)
      return;
    
    if (candidates[i]<=target){ // if that candidate value is higher than target why to add??
     list.add(candidates[i]); 
     helper(i, candidates,  target-candidates[i], list,result); //pick case
     list.remove(list.size()-1);
    }
    helper(i+1, candidates,  target,list,result);  //not pick-
}
   
}

