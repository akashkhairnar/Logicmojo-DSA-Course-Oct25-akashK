// Problem: 83. Remove Duplicates from Sorted List
// Link: https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/
// Notes:  two pointer= link the nodes if not match
// Level: Easy
// Pattern: Two Pointer
// Revisit: no


/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode deleteDuplicates(ListNode head) {

    ListNode curr= head;
    while(curr!=null){
        ListNode next= curr.next;
       while(next!=null&& curr.val== next.val){
        next= next.next;
       }
       curr.next= next;
       curr=curr.next;

    }
    return head;
        
    }
}
//on
