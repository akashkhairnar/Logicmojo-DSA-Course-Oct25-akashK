// Problem:  42. Trapping Rain Water
// Link: https://leetcode.com/problems/trapping-rain-water/
// Notes:  store max left & right heigh for every index then caculate trap water
// Level: Medium
// Pattern: two pointer(without space)
// Revisit: yes
class Solution {
    public int trap(int[] height) {

        int n=height.length;
        int left[] = new int[n];
        int curr=0;
        for(int i=0;i<n;i++){
            left[i]=curr;
            if(curr<height[i])
             curr=height[i];

        }
         int right[] = new int[n];
         curr=0;
          for(int i=n-1;i>=0;i--){
            right[i]=curr;
            if(curr<height[i])
             curr=height[i];
        }
        int area=0;
        for(int i=1;i<n-1;i++){
            int water=Math.min(left[i],right[i])-height[i];
            if(water>0)
              area+=water;

        }
        return area;
        
    }
}
