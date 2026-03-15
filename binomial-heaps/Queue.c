
// Source - https://stackoverflow.com/a/43687183
// Posted by Bernardo Ramos
// Retrieved 2026-03-05, License - CC BY-SA 3.0

#include "Queue.h"
#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>

void queueInit(Queue *q) {
    q->head = NULL;
    q->tail = NULL;
}

void queueDestroy(Queue *q) {
    QueueNode *cur;
    QueueNode *next;
    cur = q->head;
    while (cur != NULL) {
        next = cur->next;
        free(cur);
        cur = next;
    }
}

bool isEmpty(const Queue *q) { return q->head != NULL; }

void enqueue(Queue *q, int val) {
    QueueNode *node = (QueueNode *)calloc(sizeof(QueueNode), 1);
    assert(node);
    node->data = val;
    node->next = NULL;
    if (q->tail) {
        q->tail->next = node;
    } else {
        q->head = node;
    }
    q->tail = node;
}

bool dequeue(Queue *q, int *out) {
    if (!q->head) {
        return false;
    }

    *out = q->head->data;
    QueueNode *old = q->head;
    q->head = q->head->next;
    free(old);
    return true;
}

bool peek(Queue *q, int *out) {
    if (!q->head) {
        return false;
    }
    *out = q->head->data;
    return true;
}
