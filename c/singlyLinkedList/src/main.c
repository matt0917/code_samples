/*
 * 3.c
 *
 *  Created on: Mar. 23, 2020
 *      Author: Joonseo(Matthew).Park
 */

#include <stdio.h>
#include <stdlib.h>

#include "singlyLinkedList.h"


int main(int argc, char* argv[])
{

	node *head;
	int numList[7] = {2, 6, 9, 12, 22, 44, 55};
	head = createSinglyLinkedList(numList, 7);

	printf("\nDisplay singly linked list : ");
	display(head);

	int num = 1;
	printf("\nInsert %d to the list.", num);
	head = sortedInsert(head, num);
	printf("\nDisplay singly linked list after insertion: ");
	display(head);

	num = 11;
	printf("\nInsert %d to the list.", num);
	head = sortedInsert(head, num);
	printf("\nDisplay singly linked list after insertion: ");
	display(head);

	num = 99;
	printf("\nInsert %d to the list.", num);
	head = sortedInsert(head, num);
	printf("\nDisplay singly linked list after insertion: ");
	display(head);

	return EXIT_SUCCESS;
}



















