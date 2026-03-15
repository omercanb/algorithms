#include "BinomialHeap.h"
#include "BinomialTree.h"
#include <stdint.h>

static void binomHeapInterleave(BinomHeap *h1, BinomHeap *h2);

// Used for a checksums to check integrity of unions, extract min etc.
static uint64_t hash(int val) {
    uint64_t x = (uint64_t)(unsigned int)val;
    x ^= x >> 16;
    x *= 0x45d9f3b;
    x ^= x >> 16;
    x *= 0x45d9f3b;
    x ^= x >> 16;
    return x;
}

static void checksumRecurse(BinomHeapNode *root, uint64_t *sum) {
    *sum += hash(root->key);
    BinomHeapNode *child = root->child;
    while (child != NULL) {
        checksumRecurse(child, sum);
        child = child->sibling;
    }
}

static uint64_t checksum(BinomHeap *h) {
    uint64_t sum = 0;
    BinomHeapNode *cur = h->root;
    while (cur) {
        checksumRecurse(cur, &sum);
        cur = cur->sibling;
    }
    return sum;
}

void binomHeapInit(BinomHeap *h) {
    h->root = NULL;
    h->size = 0;
}

// Used in debug mode to make sure all binomial heap properties hold
void binomHeapCheckRootListInvariants(const BinomHeap *h) {
    BinomHeapNode *cur = h->root;
    // The accumulator for the binary representation of n (this is a property of
    // binomial heaps)
    size_t sum = 0;
    while (cur) {
        // Check tree invariants first
        binomTreeCheckInvariants(cur);
        // Check the degrees are in strictly decreasing order
        if (cur->sibling) {
            assert(cur->degree < cur->sibling->degree);
        }
        sum += (1 << cur->degree);
        cur = cur->sibling;
    }
    // Check the binary representation of n matches the degrees of nodes in the
    // root list;
    assert(sum == h->size);
}

// Put a new B0 at the start of the list
// Merge adjacent trees of equal degrees
// The merge happens only at the root by merging into the root
// root -> Bk -> Bk -> Bk+1 becomes root -> Bk+1 -> Bk+1 -> root -> Bk+2
BinomHeapNode *binomHeapAppend(BinomHeap *h, int key) {
    // Insert new node at the start of the list
    BinomHeapNode *node = newBinomHeapNode(key);
    node->sibling = h->root;
    h->root = node;
    // This loop proceeds by merging siblings into root (branch 1) or
    // merging root with sibling (branch 2)
    while (h->root->sibling) {
        BinomHeapNode *cur = h->root;
        if (cur->degree == cur->sibling->degree) {
            // Merge so the parent has the smaller key
            if (cur->key < cur->sibling->key) {
                BinomHeapNode *tmp = cur->sibling->sibling;
                binomTreeJoin(cur, cur->sibling);
                cur->sibling = tmp;
            } else {
                h->root = cur->sibling;
                binomTreeJoin(cur->sibling, cur);
            }
        } else {
            break;
        }
    }
    h->size++;
    return node;
}

// Desctructively union h2 onto h1
void binomHeapUnion(BinomHeap *h1, BinomHeap *h2) {
#ifndef NDEBUG
    uint64_t preChecksum = checksum(h1) + checksum(h2);
#endif
    // Merge h2 onto h1 so that the list is sorted by degrees
    binomHeapInterleave(h1, h2);
    // Prev's purpose is to connect the previous node when cur gets merged as a
    // child
    BinomHeapNode *prev = NULL;
    BinomHeapNode *cur = h1->root;
    // General idea of merge
    // If cur and next are equal
    //      Merge UNLESS next next is also equal, if so skip
    //      This way the three equal case gets handled in the next iteration
    while (cur && cur->sibling) {
        BinomHeapNode *next = cur->sibling;
        BinomHeapNode *nextNext = next->sibling; // May be null
        // Case: cur = next < nextNext
        if (cur->degree == next->degree &&
            (nextNext == NULL || next->degree < nextNext->degree)) {
            // Merge cur and next
            if (cur->key < next->key) {
                // Cur becomes the parent
                cur->sibling = next->sibling;
                binomTreeJoin(cur, next);
            } else {
                // Next becomes the parent
                if (prev == NULL) {
                    h1->root = next;
                } else {
                    prev->sibling = next;
                }
                binomTreeJoin(next, cur);
                cur = next;
            }
            // We dont increment the pointers because we merged two
        } else {
            prev = cur;
            cur = cur->sibling;
        }
    }
#ifndef NDEBUG
    uint64_t postChecksum = checksum(h1);
    assert(preChecksum == postChecksum);
    binomHeapCheckRootListInvariants(h1);
#endif
}

// Merges two bimonial heaps in a sorted way
// Used for binom heap union
static void binomHeapInterleave(BinomHeap *h1, BinomHeap *h2) {
#ifndef NDEBUG
    uint64_t preChecksum = checksum(h1) + checksum(h2);
#endif
    BinomHeap h;
    binomHeapInit(&h);
    BinomHeapNode *cur1 = h1->root;
    BinomHeapNode *cur2 = h2->root;
    // Dummy node
    h.root = newBinomHeapNode(0);
    BinomHeapNode *joinedCur = h.root;
    // Merge sort like sorted merge
    while (cur1 && cur2) {
        if (cur1->degree <= cur2->degree) {
            joinedCur->sibling = cur1;
            joinedCur = cur1;
            cur1 = cur1->sibling;
        } else {
            joinedCur->sibling = cur2;
            joinedCur = cur2;
            cur2 = cur2->sibling;
        }
    }
    while (cur1) {
        joinedCur->sibling = cur1;
        joinedCur = cur1;
        cur1 = cur1->sibling;
    }
    while (cur2) {
        joinedCur->sibling = cur2;
        joinedCur = cur2;
        cur2 = cur2->sibling;
    }
    BinomHeapNode *dummy = h.root;
    h.root = h.root->sibling;
    free(dummy);
    // Make h1 the merged heap
    h1->root = h.root;
    h1->size = h1->size + h2->size;
    // Erase h2 so it isn't misused
    h2->root = NULL;
    h2->size = 0;
#ifndef NDEBUG
    uint64_t postChecksum = checksum(h1);
    assert(preChecksum == postChecksum);
#endif
}

int binomHeapExtractMin(BinomHeap *h) {
#ifndef NDEBUG
    uint64_t preChecksum = checksum(h);
#endif
    assert(h->root);
    // Find min by looping through root list and remove the min tree from the
    // root list
    BinomHeapNode *cur = h->root;
    BinomHeapNode *prev = NULL;
    BinomHeapNode *minTree = h->root;
    BinomHeapNode *minTreePrev = NULL;
    while (cur) {
        if (cur->key < minTree->key) {
            minTree = cur;
            minTreePrev = prev;
        }
        prev = cur;
        cur = cur->sibling;
    }
    int minKey = minTree->key;

    // Remove min tree from the list by connecting to its sibling
    if (minTreePrev == NULL) {
        h->root = minTree->sibling;
    } else {
        minTreePrev->sibling = minTree->sibling;
    }
    // Update the size of the heap
    h->size -= 1 << minTree->degree;

    // Reverse the child list
    // prev and cur are now pointers to the child list
    // The children are B_k-1 to B_0
    // We reverse the sibling connections of the child list
    // We also need to maintain the size of the child trees for the heap
    prev = NULL;
    cur = minTree->child;
    while (cur) {
        cur->parent = NULL;
        BinomHeapNode *next = cur->sibling;
        cur->sibling = prev;
        prev = cur;
        cur = next;
    }
    // Because we looped to the end prev is now the root of the reversed list
    BinomHeapNode *childListRoot = prev;
    BinomHeap childHeap;
    binomHeapInit(&childHeap);
    childHeap.root = childListRoot;

    // The child heap doesn't contain the removed element so -1
    childHeap.size = (1 << minTree->degree) - 1;

#ifndef NDEBUG
    binomHeapCheckRootListInvariants(&childHeap);
#endif

    free(minTree);
    binomHeapUnion(h, &childHeap);
#ifndef NDEBUG
    uint64_t postChecksum = checksum(h) + hash(minKey);
    assert(preChecksum == postChecksum);
    binomHeapCheckRootListInvariants(h);
#endif
    return minKey;
}

void binomHeapDecreaseKey(BinomHeapNode *node, int newKey) {
    assert(newKey <= node->key);
    while (node->parent && newKey <= node->key) {
        node->key = node->parent->key;
        node = node->parent;
    }
    node->key = newKey;
}

void binomHeapPrint(const BinomHeap *h) {
    printf("n: %zu\n", h->size);
    BinomHeapNode *cur = h->root;
    while (cur != NULL) {
        printf("Node of degree: %zu (n=%d) -> ", cur->degree, 1 << cur->degree);
        binomTreePrint(cur);
        printf("\n");
        cur = cur->sibling;
    }
}

void binomHeapTest() {
    BinomHeap h;
    binomHeapInit(&h);
    BinomHeapNode *arr[10];
    for (int n = 0; n < 10; n++) {
        arr[n] = binomHeapAppend(&h, n);
    }
    binomHeapCheckRootListInvariants(&h);
    binomHeapPrint(&h);
    printf("Node 7: %d\n", arr[7]->key);
    binomHeapDecreaseKey(arr[7], -1);
    binomHeapPrint(&h);
    // int min = binomHeapExtractMin(&h);
    // binomHeapPrint(&h);
    // printf("Min: %d\n", min);
    // BinomHeap h1;
    // binomHeapInit(&h1);
    // for (int n = 0; n < 100; n++) {
    //     binomHeapAppend(&h1, n);
    // }
    // binomHeapUnion(&h, &h1);
    // printf("Merged:\n");
    // binomHeapPrint(&h);
}

int main() { binomHeapTest(); }
