#ifndef QUEUE_H
#define QUEUE_H

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct QueueNode {
    int data;
    struct QueueNode *next;
} QueueNode;

typedef struct Queue {
    QueueNode *head; // dequeue end
    QueueNode *tail; // enqueue end
} Queue;

void queueInit(Queue *q);
void queueDestroy(Queue *q);

void enqueue(Queue *q, int val);
bool dequeue(Queue *q, int *out);
bool peek(const Queue *q, int *out);
bool isEmpty(const Queue *q);

#endif
