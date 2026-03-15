/**
 * We will first create the strucures for a binomial tree
 * Key, parent, child, sibling, degree
 * Then we write the invariants for the tree
 */

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

#include "BinomialTree.h"

// Check child degrees hold according to the binomial tree properties
void binomTreeCheckChildInvariant(BinomHeapNode *root) {
    BinomHeapNode *child = root->child;
    size_t i = 0;
    while (child != NULL) {
        assert(child->degree + i - 1 != root->degree);
        binomTreeCheckChildInvariant(child);
        child = child->sibling;
        i++;
    }
}

// Check sibling degrees hold according to the binomial tree properties
bool binomTreeCheckSiblingInvariant(BinomHeapNode *root) {
    if (root == NULL) {
        return true;
    }

    if (root->sibling == NULL) {
        return true;
    } else if (root->degree != root->sibling->degree + 1) {
        return false;
    } else {
        return binomTreeCheckSiblingInvariant(root->sibling) &&
               binomTreeCheckSiblingInvariant(root->child);
    }
}

// Check that parent and child pointers point to each other
// Check that all siblings point to the same parent
void binomTreeCheckPointerLogic(BinomHeapNode *root) {
    if (root->child) {
        assert(root->child->parent == root);
    }
    // All siblings point to same parent
    BinomHeapNode *child = root->child;
    while (child != NULL) {
        assert(child->parent == root);
        child = child->sibling;
    }
}

// Check that heap propert holds
void binomTreeCheckHeapProperty(BinomHeapNode *root) {
    BinomHeapNode *child = root->child;
    while (child != NULL) {
        assert(child->key >= root->key);
        child = child->sibling;
    }
}

void binomTreeCheckInvariants(BinomHeapNode *root) {
    binomTreeCheckPointerLogic(root);
    binomTreeCheckSiblingInvariant(root);
    binomTreeCheckChildInvariant(root);
    binomTreeCheckHeapProperty(root);
}

// Unite two binomial trees and make the parent the parent
// Updates the childs sibling
void binomTreeJoin(BinomHeapNode *parent, BinomHeapNode *child) {
    child->sibling = parent->child;
    parent->child = child;
    // Because trees are the same degree the child shouldn't have a parent
    assert(child->parent == NULL);
    child->parent = parent;
    // Joins only happen on trees with same degree
    // printf("Child: %d, Parent: %d\n", child->degree, parent->degree);
    assert(child->degree == parent->degree);
    parent->degree++;
}

BinomHeapNode *newBinomHeapNode(int key) {
    BinomHeapNode *node = calloc(sizeof(BinomHeapNode), 1);
    node->key = key;
    node->degree = 0;
    return node;
}

int count = 0;
// For testing purposes
// Recursively create a binomial tree of degree k
// Use global count to make it easier to keep track of nodes
BinomHeapNode *binomTreeBuild(int k) {
    if (k == 0) {
        count++;
        return newBinomHeapNode(count);
    }
    BinomHeapNode *left = binomTreeBuild(k - 1);
    BinomHeapNode *right = binomTreeBuild(k - 1);
    binomTreeJoin(right, left);
    binomTreeCheckInvariants(right);
    return right;
}

void binomTreeDestroy(BinomHeapNode *root) {
    BinomHeapNode *child = root->child;
    while (child != NULL) {
        binomTreeDestroy(child);
        child = child->sibling;
    }
    free(root);
}

// Use this to view the structure of a binom tree
// Prints itself then it's children in a fully parenthesized manner
void binomTreePrint(const BinomHeapNode *root) {
    // Print an open paren, print children, print a close paren (and a newline?)
    printf(" %d(", root->key);
    BinomHeapNode *child = root->child;
    while (child != NULL) {
        binomTreePrint(child);
        child = child->sibling;
    }
    printf(")");
}
// int main() {
//     BinomHeapNode *root = binomTreeBuild(12);
//     binomTreeCheckInvariants(root);
//     binomTreePrint(root);
// }
