#ifndef BINOMIAL_HEAP_H
#define BINOMIAL_HEAP_H

#include "BinomialTree.h"
#include <stddef.h>

void binomHeapInit(BinomHeap *h);
void binomHeapAppend(BinomHeap *h, int key);
void binomHeapUnion(BinomHeap *h1, BinomHeap *h2);
void binomHeapPrint(const BinomHeap *h);
void binomHeapCheckRootListInvariants(const BinomHeap *h);
void binomHeapTest(void);

#endif
