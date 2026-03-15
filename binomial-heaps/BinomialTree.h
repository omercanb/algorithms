#ifndef BINOMIAL_TREE_H
#define BINOMIAL_TREE_H

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct BinomHeapNode {
    int key;
    struct BinomHeapNode *parent;
    struct BinomHeapNode *child; // Leftmost child
    struct BinomHeapNode *sibling;
    size_t degree; // This tree is a B_k where k = degree
} BinomHeapNode;

typedef struct {
    BinomHeapNode *root;
    size_t size;
} BinomHeap;

void binomTreeCheckChildInvariant(BinomHeapNode *root);
bool binomTreeCheckSiblingInvariant(BinomHeapNode *root);
void binomTreeCheckPointerLogic(BinomHeapNode *root);
void binomTreeCheckHeapProperty(BinomHeapNode *root);
void binomTreeCheckInvariants(BinomHeapNode *root);

void binomTreeJoin(BinomHeapNode *parent, BinomHeapNode *child);
BinomHeapNode *newBinomHeapNode(int key);
BinomHeapNode *binomTreeBuild(int k);
void binomTreeDestroy(BinomHeapNode *root);
void binomTreePrint(const BinomHeapNode *root);
extern int count;
#endif // BINOMIAL_TREE_H
