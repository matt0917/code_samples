/*
 * singlyLinkedList.h
 *
 *  Created on: Mar. 23, 2020
 *      Author: Joonseo(Matthew).Park
 */

#ifndef SINGLYLINKEDLIST_H_
#define SINGLYLINKEDLIST_H_

typedef struct nodes
{
	int data;
	struct nodes* next;
}node;
node* sortedInsert(node* head, int data);
int delete(node* head);
void display(node* head);
node* createSinglyLinkedList(int dataArray[], unsigned int size);

#endif /* SINGLYLINKEDLIST_H_ */
