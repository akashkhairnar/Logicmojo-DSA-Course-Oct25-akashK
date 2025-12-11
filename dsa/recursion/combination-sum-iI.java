// Problem:  40. Combination Sum II
// Link: https://leetcode.com/problems/combination-sum-ii/
// Level: Hard
// Pattern:  backtracking
// Revisit: Yes



class Solution {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);  // as we  don't want duplicate
        List<List<Integer>> result= new ArrayList<>();
        List<Integer> list= new ArrayList<>();
        backtrack( 0,candidates, target,list,result);
        return result;

        
    }
    private void backtrack( int index,int[] candidates, int target, List<Integer> list, List<List<Integer>> result){
        if( target== 0){
            result.add(new ArrayList<>(list));
            return;
        }
        if(index== candidates.length || target<0)
          return;
        
        for(int i=index;i<candidates.length;i++ ){
            if(i>index && candidates[i]==candidates[i-1])  // i > index → next children → skip if same as previous and avoid  duplicate calls
             continue;

            if(candidates[i]> target)
              break;
              
             list.add(candidates[i]);
     
           backtrack( i+1,candidates, target-candidates[i],list,result);
           list.remove(list.size()-1);  
        }
    }
}
