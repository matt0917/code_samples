/*
 * singlyLinkedList.c
 *
 *  Created on: Mar. 23, 2020
 *      Author: Joonseo(Matthew).Park
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "singlyLinkedList.h"

/*
 * Insert data to the right order in an ordered linked list
 * return inserted node or NULL
 */
node* sortedInsert(node* head, int data)
{
	// check the pointer is null or not
	node *newNode, *curr, *prev;
	newNode = (node*)malloc(sizeof(node));
	if(NULL == newNode){
		printf("Not enough memory to allocated");
		return NULL;
	}
	newNode->data = data;
	// If the linked list is empty make the node as head and return the node
	if(NULL == head){
		head = newNode;
		head->next = NULL;
		return head;
	}
	// If the data is equal or less than the data of the head node, set newNode as head
	// newNode->next will be the current head
	// return newly defined head
	if(data <= head->data){
		newNode->next = head;
		head = newNode;
	} else{
		// traversal through the list and once the node equal or less than the new node,
		// prev->next will be the new node and new->next will be the curr
		prev = head;
		curr = head;
		while( (curr != NULL) && (data > curr->data) ){
			prev = curr;
			curr = curr->next;
		}
		prev->next = newNode;
		newNode->next = curr;
	}
	return head;
}


int delete(node* head)
{
	// check the pointer is null or not
	if(NULL == head){
		return EXIT_FAILURE;
	}
	node* tmp;
	tmp=head->next;
	head->next = tmp->next;
	free(tmp);
	tmp=NULL;

	return EXIT_SUCCESS;
}


void display(node* head)
{
	int count;
	count = 0;
	node* curr;
	curr = head;
	printf("\n");
	while(curr != NULL){
		printf("%d->", curr->data);
		curr = curr->next;
		count++;
	}
	printf("NULL\n");
}


node* createSinglyLinkedList(int dataArray[], unsigned int size)
{
	node *head, *curr;
	int i;
	for (i=0 ; i < size ; i++){
		if (i==0){
			head = (node*)malloc(sizeof(node));
			curr = head;
		}else{
			curr->next = (node*)malloc(sizeof(node));
			curr = curr->next;
		}
		curr->data = dataArray[i];
	}
	curr->next = NULL;

	return(head);
}


















