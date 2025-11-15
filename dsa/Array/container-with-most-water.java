// Problem:  11. Container With Most Water
// Link: https://leetcode.com/problems/container-with-most-water/description/
// Notes:  Two pointer- calculate area whatever hight is slower from low & high move that
// Level: Easy
// Pattern: Two Pointer
// Revisit: no

class Solution {
    public int maxArea(int[] height) {
        int l=0;
        int h= height.length-1;
        int max= Integer.MIN_VALUE;
        while(l<h){
            int area= Math.min(height[l],height[h])*(h-l);
            if(max<area)
              max=area;
            if(height[h]<height[l])
             h--;
            else
             l++;
        }
        return max;
        
    }
}
