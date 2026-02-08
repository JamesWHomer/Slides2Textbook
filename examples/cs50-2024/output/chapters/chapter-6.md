# Chapter 6: Week 5 — Data Structures: Abstract Data Types, Linked Lists, Trees, Hash Tables, and Tries

By week 5, you have enough C in your toolkit to stop thinking of memory as something that merely “holds variables,” and to start using memory deliberately as a **design medium**. This week’s topic—**data structures**—is really about the question:

> Given the same raw memory (bytes and addresses), how can we organize data so that common operations become faster, simpler, or more scalable?

To make that question precise, we will repeatedly separate two levels of thinking:

- An **abstraction**: a high-level description of what a data structure *does* and what operations it supports.
- An **implementation**: the low-level details of how we represent that structure in memory using arrays, pointers, `struct`, and `malloc`.

This distinction matters because there are often many valid implementations of the same abstraction, and each comes with trade-offs, especially between **time** (speed) and **space** (memory).

---

## 6.1 Abstract Data Types (ADTs): What vs. How

An **abstract data type** (ADT) is a “data structure concept” defined primarily by:

- what it stores,
- what operations it supports,
- what guarantees it provides about those operations,

without committing to how it is implemented in memory.

For example, a “queue” is not defined by whether it uses an array or a linked list. A queue is defined by the *rule* it follows: who comes out first.

This week begins with two ADTs that are both familiar from everyday life:

- **Queues** (lines)
- **Stacks** (piles)

These are intentionally simple, because they let you focus on the relationship between an ADT and its implementation.

---

## 6.2 Queues: FIFO (First In, First Out)

A **queue** (often called a “line”) has a fairness property:

- **FIFO**: **First In, First Out**

If three people line up in order 1, 2, 3, then a queue guarantees they will be served in order 1, 2, 3.

### 6.2.1 Queue operations: enqueue and dequeue

The standard queue operations are:

- **enqueue**: add an element to the queue (enter the line)
- **dequeue**: remove an element from the queue (leave the line)

The key point is that `dequeue` removes the *oldest* element.

### 6.2.2 Implementing a queue with an array

A simple implementation is to use an array with a fixed **capacity**, and track how many elements are currently stored (often called the **size**):

- the array stores elements contiguously in memory
- an integer `size` tells you how many slots are in use

This works, but it immediately raises an issue that will drive much of the rest of this chapter:

> Arrays have fixed size, and memory elsewhere in the program may prevent you from simply “extending” an array in place.

---

## 6.3 Stacks: LIFO (Last In, First Out)

A **stack** is the opposite ordering policy:

- **LIFO**: **Last In, First Out**

In a stack, the most recently added item is the first one removed.

This is not always “fair” in the same sense as FIFO, but it is often exactly what we want. A common real-world analogy is an email inbox where the newest messages appear at the top; many people naturally read the most recent messages first, which is a stack-like pattern.

### 6.3.1 Stack operations: push and pop

The standard stack operations are:

- **push**: add an element to the top of the stack
- **pop**: remove the element from the top of the stack

### 6.3.2 Implementing a stack with an array

Just like a queue, a stack can be implemented with:

- an array of capacity `N`, and
- an integer that tracks the current number of elements.

The difference between a stack and a queue is not “the memory layout,” but the **logic** used to decide which element gets removed next.

This is a key ADT lesson:

> The same underlying storage (like an array) can implement different ADTs depending on what operations you perform and how.

---

## 6.4 Arrays Revisited: Contiguity and the Cost of Growing

Recall the defining property of an array:

- An array stores elements **contiguously** (back-to-back) in memory.

That contiguity is powerful. It enables direct indexing (`a[i]`) and makes binary search possible when data is sorted. But it becomes a burden the moment you want an array to grow beyond its allocated capacity.

### 6.4.1 The “add a 4th element” problem

Suppose you have an array of three integers containing:

- `1, 2, 3`

You now want to add `4`.

In an idealized diagram, you might imagine placing `4` immediately after `3`, but real memory is busy. That “next” region might already be in use by something else—perhaps another variable, perhaps a string, perhaps something you never explicitly created but that the program needs.

Even if there are many unused (garbage) bytes elsewhere in memory, you cannot just place `4` anywhere:

- the data must remain contiguous to still be “an array.”

### 6.4.2 The naive growth strategy: allocate a bigger array and copy

A workable strategy is:

1. Allocate a new array that is larger.
2. Copy the old elements into the new array.
3. Add the new element.
4. Free the old array.

This works, but it has costs:

- **Time cost:** copying requires iterating over all old elements → about **Big O(n)** work.
- **Space cost (temporarily):** during copying, you momentarily hold both arrays in memory.

And the problem repeats: if you later add a 5th element, then a 6th, you may keep paying this copying cost again and again.

---

## 6.5 Growing an Array Manually with `malloc`: A Worked Example

To see exactly what “copying into a bigger array” looks like in C, consider an example program that begins with space for 3 integers, then “resizes” to space for 4.

### 6.5.1 Starting with a fixed array (easy, but not resizable)

A fixed array version might look like this:

```c
#include <stdio.h>

int main(void)
{
    int list[3];
    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    for (int i = 0; i < 3; i++)
    {
        printf("%i\n", list[i]);
    }
}
```

This prints `1 2 3`, but the array’s size is permanently 3 for the life of the variable. You cannot `free` it, and you cannot “make it larger” in place.

### 6.5.2 Switching to dynamic allocation (resizable in principle)

To make resizing possible, you must allocate the array on the heap:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *list = malloc(3 * sizeof(int));
    if (list == NULL)
    {
        return 1;
    }

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    // ... later, we decide we want room for 4 ints ...
}
```

A subtle but important convenience appears here:

- Even though `list` is a pointer, you can still write `list[i]`.
- Array indexing is “syntactic sugar” for pointer arithmetic.

### 6.5.3 Allocating a bigger block and copying

Now we allocate a second block, copy, and extend:

```c
int *tmp = malloc(4 * sizeof(int));
if (tmp == NULL)
{
    free(list);     // avoid leaking the original block
    return 1;
}

for (int i = 0; i < 3; i++)
{
    tmp[i] = list[i];
}

tmp[3] = 4;

free(list);
list = tmp;
```

Two memory lessons are embedded in this pattern:

1. **Order matters for correctness.**  
   You must copy the old elements *before* freeing the old memory.

2. **Error handling must clean up.**  
   If allocating `tmp` fails, you must free the original `list` (otherwise you leak memory).

Finally, you would typically free at the end of the program as well:

```c
free(list);
```

This works, but the amount of code is disproportionate to the simple goal (“I want to add one more number”). That pain motivates the next idea:

> What if we stop requiring contiguity, and instead connect values with pointers?

---

## 6.6 Linked Lists: Escaping Contiguity with Pointers

A **linked list** is a data structure that stores elements in separate “chunks” of memory that can live anywhere, as long as each chunk contains:

- the data you care about, and
- a pointer that tells you where to find the next chunk.

Each chunk is called a **node**.

### 6.6.1 Nodes and “metadata”

In a linked list node, the “real” information might be the integer `1`, `2`, `3`, etc.

But the pointer to the next node is still data stored in memory. It is useful not because it is part of the problem domain (“what numbers are in the list”), but because it helps organize the structure.

This is a natural place to introduce the term:

- **data**: the values you conceptually care about (like `1, 2, 3`)
- **metadata**: “data about data,” such as pointers that help connect nodes together

The pointer is metadata: it is an implementation detail that enables the structure to work.

### 6.6.2 Terminating the list with `NULL`

The last node in a linked list must not have an uninitialized “next” pointer. If it did, your program might treat that garbage value as an address and try to follow it, causing crashes or corruption.

So the final node’s pointer is set to:

- `NULL`

This cleanly marks “end of list.”

---

## 6.7 Implementing a Linked List Node in C (`struct`)

To represent a linked list node, we define a `struct` with:

- an integer field (the element),
- a pointer to the next node.

Because the node points to another node of the same type, we use the more explicit `struct node` name inside the definition, and then `typedef` it to the shorter alias `node`.

```c
typedef struct node
{
    int number;
    struct node *next;
}
node;
```

This pattern is extremely common in C: it solves the “self-referential struct” issue while still giving you a convenient short type name.

---

## 6.8 The Arrow Operator (`->`): A Friendlier Syntax for Struct Pointers

When you have a pointer to a struct, you often want to “go to the struct, then access a field.”

You can write that in two equivalent ways:

### 6.8.1 The verbose way: `(*n).field`

```c
(*n).number = 1;
```

This means:

- `n` is a pointer,
- `*n` dereferences it (go to the struct),
- `.` accesses a field inside the struct.

### 6.8.2 The common way: `n->field`

C provides syntactic sugar:

```c
n->number = 1;
```

This is the same operation, but it visually resembles the arrows we draw between nodes in diagrams, and it is far easier to read and write.

---

## 6.9 Building a Linked List Step by Step

A linked list is usually represented by a single pointer to its first node, often called the **head**. In lecture, this pointer was called `list`.

### 6.9.1 Start with an empty list

An empty list should be explicitly initialized:

```c
node *list = NULL;
```

This avoids a garbage pointer and makes it clear that there are currently no nodes.

### 6.9.2 Allocate a new node and fill its fields

```c
node *n = malloc(sizeof(node));
if (n == NULL)
{
    return 1;
}

n->number = 1;
n->next = NULL;
```

This allocates one node and sets its “next” pointer to `NULL`, because (so far) it is the end of the list.

### 6.9.3 Make the list point to that node

```c
list = n;
```

Now the list has one element.

---

## 6.10 Prepending: Constant-Time Insertion at the Front

A very common linked list strategy is to insert new nodes at the front. This is called **prepending**.

The core idea is:

1. Set the new node’s `next` pointer to the current head.
2. Update the head pointer to point to the new node.

```c
n->next = list;
list = n;
```

### 6.10.1 Why prepend?

Prepending is fast:

- It does not matter how long the list already is.
- You never traverse the list.
- The number of pointer updates is constant.

So, the running time for insertion via prepending is:

- **Big O(1)** (constant time)

### 6.10.2 The trade-off: order is reversed

If you insert `1`, then prepend `2`, then prepend `3`, the list becomes:

- `3 -> 2 -> 1`

This is correct as a list, but the order might not match what you want.

---

## 6.11 A Complete Example: Building a Linked List from Command-Line Arguments

To avoid repeatedly prompting for input, you can build a list from `argv`.

A full program outline looks like this:

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next;
}
node;

int main(int argc, char *argv[])
{
    node *list = NULL;

    for (int i = 1; i < argc; i++)
    {
        int number = atoi(argv[i]);

        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            // free memory thus far (not shown here)
            return 1;
        }

        n->number = number;
        n->next = list;
        list = n;
    }

    // Print the list
    node *ptr = list;
    while (ptr != NULL)
    {
        printf("%i\n", ptr->number);
        ptr = ptr->next;
    }

    // Free the list (not shown here)
}
```

Key ideas shown here:

- `atoi` converts a string to an integer (ASCII-to-integer).
- Each new node is prepended, so output will be reversed relative to input.
- Traversal is performed by a “walking pointer” (`ptr`) that follows `next` until `NULL`.

---

## 6.12 Memory Leaks and Orphaned Nodes: The Danger of Losing the Only Pointer

Linked lists are flexible, but they add a new kind of bug that arrays do not have.

Suppose:

- `list` points to the first node (containing `1`).
- You allocate a new node `n` (containing `2`).

If you do this incorrectly:

```c
list = n;
```

without first connecting `n` to the old list, you have a problem:

- nothing points to the node containing `1` anymore.

That node still exists in memory, but your program has lost the only address that could reach it. This situation is often described as:

- the node has been **orphaned**

and it creates:

- a **memory leak**, because the program can no longer `free` that node later.

The correct order for prepending is therefore essential:

```c
n->next = list;
list = n;
```

---

## 6.13 Appending: Preserving Order, but Paying Linear Time

If you want the list to preserve the input order (`1 -> 2 -> 3`), you can **append** each new node to the end instead of prepending to the front.

### 6.13.1 The main idea: find the tail

If `list` is empty, appending is easy:

- `list = n`

But if the list already has nodes, you must traverse until you find the last node (the one whose `next` is `NULL`), then attach the new node:

- `tail->next = n`

### 6.13.2 The trade-off: insertion becomes Big O(n)

Appending costs time because to append you must:

- walk through the list to reach the end.

If there are `n` nodes already, finding the end is **Big O(n)**, which means insertion is no longer constant-time.

This is an early example of a broader theme:

> Improving one property (like preserving order) may worsen another (like insertion speed).

---

## 6.14 Inserting into a Sorted Linked List: Correctness Requires More Cases

If you want the list to be kept in **sorted order** regardless of input order, insertion becomes more intricate, because you must decide where the new node belongs:

- at the beginning (if it is smaller than the current head),
- in the middle (between two nodes),
- at the end (if it is larger than everything currently present).

The key structural idea is **splicing**:

- connect the new node to the “right-hand” neighbor,
- connect the “left-hand” neighbor to the new node.

The code to do this is longer and case-heavy, but conceptually it is still just pointer manipulation with careful order of operations.

The trade-off remains:

- insertion is still **Big O(n)** in the worst case, because you might need to walk to the end.

---

## 6.15 Linked Lists vs. Arrays: The Time–Space Trade-Off

At this point, we can summarize why linked lists are appealing and what they cost.

### 6.15.1 What linked lists solve

Linked lists are **dynamic**:

- they can grow one node at a time,
- they do not require contiguity,
- they do not require copying all elements just to add one more.

### 6.15.2 What linked lists cost

Linked lists require extra memory:

- each node stores at least one extra pointer (`next`)

and they lose the key advantage of arrays:

- you cannot jump directly to the middle
- therefore, **binary search does not work** on a plain linked list

Searching a linked list is typically:

- **Big O(n)** in the worst case, because you may have to traverse the whole chain.

So linked lists trade:

- less wasted space and less expensive resizing
- for slower searching (and extra per-element metadata)

---

## 6.16 Trees: Recovering “Divide and Conquer” Without Contiguity

Arrays made binary search possible because sorted elements were contiguous. Linked lists removed contiguity, but they also removed the ability to divide and conquer efficiently.

Trees are a way to bring back “divide and conquer” structure, even when nodes are scattered throughout memory, by adding more pointers.

### 6.16.1 Binary Search Trees (BSTs): the rule

A **binary search tree** is a tree where each node has:

- a value (like an integer), and
- two pointers:
  - a **left** child
  - a **right** child

The BST property is:

- everything in the left subtree is **smaller** than the node’s value
- everything in the right subtree is **larger** than the node’s value

Because this property holds at every node, a BST is naturally **recursive**: each subtree is itself a BST.

### 6.16.2 A BST node in C

A node might look like this:

```c
typedef struct node
{
    int number;
    struct node *left;
    struct node *right;
}
node;
```

---

## 6.17 Searching a BST with Recursion (and Why It’s Elegant)

Searching a BST mirrors binary search conceptually:

- compare the target number to the current node
- decide to go left or right
- stop when you find the value or hit `NULL`

A recursive search function can be remarkably compact:

```c
bool search(node *tree, int number)
{
    if (tree == NULL)
    {
        return false;
    }
    else if (number < tree->number)
    {
        return search(tree->left, number);
    }
    else if (number > tree->number)
    {
        return search(tree->right, number);
    }
    else
    {
        return true;
    }
}
```

This function has a clear base case:

- if the subtree pointer is `NULL`, the number is not present

and two recursive cases:

- search left subtree
- search right subtree

The code “divides the problem” implicitly by passing a smaller subtree pointer.

### 6.17.1 Expected running time: Big O(log n) … sometimes

If the tree is **balanced** (roughly equal height on left and right), then searching behaves like binary search:

- **Big O(log n)**

This is attractive because it combines:

- the dynamism of linked structures (nodes can be allocated anywhere),
- with the fast search behavior of divide and conquer.

---

## 6.18 The Catch: Unbalanced Trees Can Devolve into Linked Lists

A BST does not automatically stay balanced.

If values are inserted in an unfortunate order (for example, `1`, then `2`, then `3`), the tree can become a straight chain:

- every node has only a right child

At that point, the structure is effectively a linked list in disguise, and searching becomes:

- **Big O(n)**

It is possible to fix this by using specialized “self-balancing” trees that perform rotations and rebalancing during insertion and deletion, but that is beyond the scope of this week’s implementation focus. The key lesson is the conceptual one:

> A BST can be fast, but only if it remains balanced; otherwise, its performance can collapse to linear time.

---

## 6.19 Dictionaries: An ADT for Key–Value Pairs

A **dictionary** is another ADT, defined by storing **key–value pairs**:

- key: a lookup identifier (like a word, or a person’s name)
- value: the associated information (like a definition, or a phone number)

A real dictionary pairs:

- words → definitions

A contacts app pairs:

- names → phone numbers (and possibly more data)

Like stacks and queues, a dictionary can be implemented in multiple ways:

- arrays (limited size, contiguity)
- linked lists (dynamic, but slower search)
- trees (can be fast, but may need balancing)
- hash tables (very fast in practice, with collisions)
- tries (very fast lookups by character, but memory-heavy)

---

## 6.20 Hashing: Mapping Large Inputs to a Finite Set of Buckets

A key idea behind hash tables is **hashing**.

A **hash function** takes an input from a potentially large (even “infinite”) set and maps it to an output in a finite range.

- Domain: all possible names (huge)
- Range: bucket indices like `0..25` (small)

A helpful physical analogy is sorting playing cards into a small number of piles by suit:

- many cards → 4 buckets (hearts, spades, clubs, diamonds)

You are “hashing” each card to a bucket based on some attribute (its suit). Once bucketed, each pile is smaller and easier to work with.

---

## 6.21 Hash Tables: Arrays of Linked Lists (and Collisions)

A **hash table** is a common dictionary implementation that combines:

- an **array** of buckets, and
- **linked lists** (or other structures) to handle collisions inside each bucket.

### 6.21.1 The basic design (26 buckets for A–Z)

A simple approach for storing contacts is:

- create an array of size 26
- bucket each name by its first letter

Conceptually:

- bucket 0: names starting with A
- bucket 1: names starting with B
- …
- bucket 25: names starting with Z

Each array location stores a pointer:

- `NULL` if there are no names in that bucket
- otherwise, a pointer to the first node in a linked list of that bucket’s entries

### 6.21.2 Collisions

A **collision** occurs when two different inputs hash to the same bucket.

For example:

- “Luigi”, “Link”, and “Lyu” all start with `L`
- they all hash to the same bucket

Collisions are not a bug in hash tables; they are an expected consequence of mapping many inputs into a small number of outputs.

The implementation response is:

- store multiple entries in the bucket using a linked list (or similar)

---

## 6.22 Hash Table Performance: Theoretical Worst Case vs. Practical Reality

In an ideal world, hashing would give constant-time lookup:

- **Big O(1)**

But collisions complicate the analysis.

### 6.22.1 Worst case: Big O(n)

In the worst case, all keys hash to the same bucket. Then the hash table becomes:

- one linked list containing all `n` elements

and searching becomes:

- **Big O(n)**

### 6.22.2 Typical case: much better than linear

If keys are distributed reasonably uniformly across buckets, then each bucket contains about:

- `n / k` elements, where `k` is the number of buckets (for example, 26)

In that scenario, searching is closer to:

- **O(n / 26)**

and while Big O notation simplifies that to O(n) (because constant factors are ignored), in real systems:

- “26 times faster” is still a meaningful improvement.

This is one of the places where it becomes important to distinguish:

- asymptotic theory (Big O),
- from real-world wall-clock time and performance engineering.

---

## 6.23 Hash Function Example in C (First Letter Only)

A simple hash function for 26 buckets can use the first letter of the word.

In C, you can compute a bucket index by converting the first letter to uppercase and subtracting `'A'`:

```c
#include <ctype.h>

unsigned int hash(const char *word)
{
    return toupper(word[0]) - 'A';
}
```

A few implementation details are worth noticing:

- `const char *word` indicates that the function does not intend to modify the string.
- `unsigned int` emphasizes that the result should not be negative.
- `toupper(word[0]) - 'A'` gives a number in the range 0–25 for alphabetic input.

This is intentionally simple, and it also highlights a limitation:

- if the first character is not a letter (punctuation, etc.), this function needs additional checks to avoid incorrect results.

In practice, real hash functions are typically more complex than “use the first letter,” specifically to reduce the chance of collisions.

---

## 6.24 The Memory Trade-Off: More Buckets Reduce Collisions, But Increase Space

If collisions are a problem, you can reduce them by increasing the number of buckets.

For example, instead of hashing only the first letter, you might hash the first **three** letters. That creates buckets like:

- LAA, LAB, LAC, …, LZZ
- (and similarly for all other starting letters)

But this explodes the number of buckets:

- `26^3 = 26 * 26 * 26`

Most of those buckets will be unused (because most three-letter combinations are not the start of any real name), but you still have to allocate space for the array if you want direct indexing into it.

This is the time–space trade-off again:

- more buckets can make lookups faster by reducing collisions,
- but more buckets require more memory.

---

## 6.25 Hash Table Structures in C (Nodes and the Table)

A hash table bucket that uses linked lists needs a node structure that stores:

- the key (name),
- the value (phone number),
- a pointer to the next node (for collisions).

Conceptually:

```c
typedef struct node
{
    char *name;
    char *number;
    struct node *next;
}
node;
```

And the table is typically:

```c
node *table[26];
```

Each `table[i]` is:

- `NULL` (no entries),
- or a pointer to the first node of a linked list for that bucket.

---

## 6.26 Tries: A Tree of Arrays (Retrieval Tree)

A **trie** (from “retrieval”) is another dictionary implementation, and it is best described as:

- a **tree of arrays**

Where a hash table is an *array of linked lists*, a trie is an *array (node) whose entries point to arrays (nodes), recursively*.

### 6.26.1 The core idea: one step per character

In a trie:

- each node contains an array of pointers (often size 26 for letters A–Z)
- following a pointer corresponds to consuming the next letter of a word

To store the name “TOAD”:

- go to the `T` pointer from the root
- then to `O`
- then to `A`
- then to `D`

The end of a valid word is marked explicitly (for example, by storing a value like the phone number at that node, or by having a boolean that indicates “this node ends a word”).

This explicit end-marker matters because one name can be a prefix of another:

- “TOAD” is a prefix of “TOADETTE”

A trie must represent both as valid keys, even though one continues beyond the other.

### 6.26.2 A trie node conceptually

A trie node might have:

- `children[26]`: pointers to child nodes
- `number`: the associated value (or `NULL` if no word ends here)

Conceptually:

```c
typedef struct node
{
    struct node *children[26];
    char *number;   // non-NULL only if a word ends here
}
node;
```

---

## 6.27 Trie Performance: Effectively Constant Time (with a Big Caveat)

Searching for a name in a trie takes time proportional to the length of the name:

- “TOM” takes 3 steps
- “TOADETTE” takes 8 steps

If we assume there is a fixed maximum length for keys (names are not infinitely long), then lookup time is bounded by a constant `K`, and we often describe trie operations as:

- **Big O(1)** (constant time), in the sense that it does not grow with the number of stored keys `n`

This is a powerful property: whether you store 3 names or 3 million names, you still only traverse characters of the query key.

### 6.27.1 The downside: enormous memory usage

The practical cost is space.

Even if only one child pointer is used at a node, the node still contains an entire array of 26 pointers, most of which are `NULL`. Across many names, this can create a massive amount of unused pointer space.

So, tries offer extremely fast lookup behavior at the cost of substantial memory overhead, and in many real-world systems hash tables are often favored because they provide excellent performance with less memory consumption.

---

## 6.28 Data Structures Are Everywhere: A Real-World Hash Table Example

A useful way to cement this week’s ideas is to recognize data structures “outside the code.”

Consider a pickup shelf organized alphabetically by first name (for example, at a restaurant where mobile orders are placed under lettered sections). That system is functioning like a hash table:

- the **hash function**: “take the first letter of the name”
- the **buckets**: labeled A through Z
- the **collision handling**: multiple orders under the same letter

It performs well when names are distributed across letters, and performs worse during busy periods when many orders accumulate under the same few letters—exactly the same collision behavior we discussed in theory.

---

## 6.29 Summary: What Week 5 Adds to Your Mental Model

This week’s new power is not just “more syntax,” but a new way of thinking:

- Data structures can be described as **ADTs** (queues, stacks, dictionaries), where the key question is what operations they support and what guarantees they provide.
- The implementation is a separate question, and in C it ultimately comes down to how you use **memory**, **pointers**, and **structs**.

The major structures and their central trade-offs are:

- **Arrays**: contiguous, fast indexing, binary search possible; fixed-size and expensive to grow (copying).
- **Linked lists**: dynamic and easy to grow; require extra pointers and generally require linear-time searching.
- **Binary search trees**: can recover logarithmic search time if balanced; can devolve into linked-list behavior if unbalanced.
- **Hash tables**: often very fast in practice; collisions can degrade performance; quality depends heavily on the hash function and bucket count.
- **Tries**: lookups take time proportional to key length, effectively constant with respect to number of stored keys; can use enormous memory due to many null pointers.

Across all of them is the unifying theme:

> You can often save time by spending space, or save space by spending time, and good design is choosing the trade-off that fits your constraints.