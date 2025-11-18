// Problem:  160. Intersection of Two Linked Lists
// Link: https://leetcode.com/problems/intersection-of-two-linked-lists/
// Notes:  As both length is diff if we start traversing another list then both will be at intersection
// Level: Easy
// Pattern: Two Pointer
// Revisit: no


/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {

        ListNode curr1= headA;
        ListNode curr2= headB;

        while(curr1!=curr2){
            if(curr1==null ){
                curr1=headB;
            }
            else if(curr2==null){
                curr2=headA;
            }
            else{
            curr1=curr1.next;
            curr2=curr2.next;
            }
        }
        return curr1;
        
    }
}
