# Chapter 4: Week 3 — Algorithms: Searching, Sorting, Big-O, and Recursion

By week 3, you already have enough C vocabulary to express nontrivial programs: variables, conditionals, loops, functions, arrays, and strings. This week shifts the focus away from new syntax and toward something more fundamental: **how to think algorithmically**, meaning how to take a real-world problem, describe a step-by-step process to solve it, and then reason about how well that process will scale as the problem grows.

The core theme is that the *same* problem can be solved in multiple ways, and those ways can differ dramatically in performance. The difference is not usually about “micro-optimizations,” but about choosing a fundamentally better strategy.

To make that concrete, we will focus on three kinds of tasks that show up everywhere in computing:

- **Searching**: Is the piece of data you want present, and where?
- **Sorting**: Can you rearrange data into an order that makes other tasks faster?
- **Recursion and divide-and-conquer**: Can you solve a big problem by solving smaller versions of the same problem and combining the results?

Along the way, we will introduce the standard language computer scientists use to describe performance: **Big O**, **Omega**, and **Theta** notation.

---

## 4.1 Problem Size vs. Time: Why Strategy Matters

In week 0, a phone book illustrated a key insight: when you search a sorted phone book, you do not need to scan one page at a time. You can go to the middle, decide which half you need, then repeat. That “halving, halving, halving” behavior produces a curve that grows very slowly as the phone book grows.

A similar idea appeared in a live “attendance-counting” thought experiment. Instead of counting people one-by-one (or even two-at-a-time), the group paired off, added their counts, sat down, and repeated. In theory, each round halves the number of participants still standing, so the number of rounds grows like a logarithm: even if the room doubled in size, it would add only about one extra round. In practice, the demo produced a wrong number because humans introduced a bug, but the *algorithmic* idea was the point: **divide and conquer** can be fundamentally faster than counting linearly.

That same principle is behind features you use daily, like searching contacts: good implementations do not usually scan top-to-bottom; they typically narrow the search range repeatedly.

To reason about these tradeoffs, we need to describe algorithms precisely, and then analyze them.

---

## 4.2 Arrays as the Playground: Contiguous Data Enables Systematic Searching

Week 2 defined an **array** as a sequence of values stored **contiguously** (back-to-back) in memory. That property matters for algorithms because it makes it possible to refer to “the first element,” “the middle element,” “the last element,” and so on in a disciplined way.

We will imagine an array as a row of “lockers” indexed from left to right:

- If the array has `n` elements, the indices are `0` through `n - 1`.
- Access uses square brackets, like `array[i]`.

Even if a human can “see the whole row at once,” a computer’s model is more constrained: it can read memory locations, but it must do so *procedurally*, step by step. That is exactly why the algorithm matters: the computer will do whatever sequence of inspections you instruct it to do.

---

## 4.3 Searching: Linear Search vs. Binary Search

### 4.3.1 The search problem

A common search problem can be described like this:

- **Input**: an array of values (for example, integers), and a target value (for example, `50`)
- **Output**: a boolean answer—**true** if the target appears in the array, **false** otherwise

There are multiple ways to implement the “black box” that performs the search.

---

### 4.3.2 Linear search

**Linear search** means scanning the data one element at a time, typically from left to right (or right to left). The order does not matter; the defining idea is that you check items one-by-one until you either find the target or exhaust the list.

A clear pseudocode version is:

```text
For i from 0 to n - 1:
    If array[i] is the target:
        Return true
Return false
```

A subtle but important detail is the placement of `Return false`. It must happen **after** the loop finishes. If you mistakenly return false the first time you see a mismatch, you would reject the array too early.

Linear search works on any array, sorted or not, but it can be slow when the target is near the end—or not present at all.

---

### 4.3.3 Binary search

**Binary search** is a divide-and-conquer search strategy that applies when the array is **sorted**. The idea is:

1. Look at the middle element.
2. If it is the target, you are done.
3. If the target is smaller, search only the left half.
4. If the target is larger, search only the right half.
5. If there is no data left to search, the target is not present.

A high-level pseudocode version is:

```text
If no elements remain:
    Return false
If middle element is the target:
    Return true
Else if target < middle element:
    Search left half
Else if target > middle element:
    Search right half
```

The “no elements remain” rule is crucial. Without it, the algorithm could keep trying to subdivide forever (or, in real code, run into invalid indices). This stopping condition is the algorithm’s **base case** (a concept we will return to when discussing recursion).

Binary search is powerful because each step discards half the remaining candidates, so the number of checks grows very slowly as `n` grows. The tradeoff is that binary search requires sorted input; if the data is unsorted, you cannot safely throw away half the array based on one comparison.

---

## 4.4 Measuring Efficiency: Big O, Omega, and Theta

When we discuss performance, we usually do **not** mean “how many seconds did it take on my laptop.” Hardware varies, and software environments vary. Instead, we measure how the number of steps grows as the input size grows.

Let:

- `n` = the size of the input (number of pages, number of people, number of elements in an array)

### 4.4.1 Big O: an upper bound (often worst case)

**Big O notation**, written `O( … )`, describes an **upper bound** on running time. Informally, it answers:

> “In the worst case, how many steps might this take, as `n` grows?”

Examples of common Big O categories include:

- `O(1)` — constant time (a fixed number of steps, regardless of `n`)
- `O(log n)` — logarithmic time (halving repeatedly)
- `O(n)` — linear time (one pass over the data)
- `O(n log n)` — linearithmic time (common in efficient sorting)
- `O(n^2)` — quadratic time (often “nested loop” behavior)

A key practice in Big O analysis is that we typically **ignore constant factors** and lower-order terms, because for large `n` they do not change the overall growth trend. For instance, `O(n)` and `O(n/2)` are both categorized as `O(n)`.

This “throw away constants” habit is not saying constants never matter in reality; rather, it is saying that asymptotically (as `n` becomes very large), the dominant term controls the behavior.

### 4.4.2 Omega: a lower bound (often best case)

**Omega notation**, written `Ω( … )`, describes a **lower bound** on running time. Informally, it answers:

> “In the best case, how few steps might this take?”

For searching:

- Linear search has a best case of `Ω(1)` if the target happens to be the first element.
- Binary search also has a best case of `Ω(1)` if the target happens to be the middle element on the first check.

### 4.4.3 Theta: a tight bound when upper and lower match

**Theta notation**, written `Θ( … )`, describes a situation where the upper and lower bounds are the same order, meaning the algorithm’s growth is tightly characterized.

For example, if an algorithm always takes on the order of `n` steps whether the input is “nice” or “unlucky,” then it might be `Θ(n)`.

---

## 4.5 Implementing Linear Search in C (Integers)

Algorithms become more concrete when translated to code. Consider implementing linear search over an integer array.

A useful C feature is that if you already know the values you want in an array, you can initialize the array with **curly braces**:

```c
int numbers[] = {20, 500, 10, 5, 100, 1, 50};
```

Here, the compiler can infer the array’s length from the initializer list, which can prevent mismatches between “how big you said the array is” and “how many values you actually provided.”

A simple linear-search program looks like this in spirit:

- Store a small list of integers in an array.
- Prompt the user for a target integer.
- Loop through the array, and if you find it, print `"found"` and exit successfully.
- If the loop ends without finding it, print `"not found"` and exit with a failure status.

A key design detail is **when to print** and **when to exit**. If you print `"not found"` inside the loop every time an element does not match, you will print `"not found"` many times even though the target might appear later. Instead:

- Print `"found"` immediately when found, and return from `main`.
- Only print `"not found"` after the loop finishes.

### 4.5.1 Exit status and returning from `main`

Recall that `main` returns an `int`. By convention:

- `return 0;` signals success.
- `return 1;` (or any nonzero value) signals failure.

This is why many programs return `0` when they work as expected and nonzero values when something goes wrong. Returning from `main` immediately terminates the program, just like returning from any other function.

---

## 4.6 Searching Strings: Why `==` Is Not Enough, and `strcmp` Matters

If you switch from integers to strings, it is tempting to write:

```c
if (strings[i] == s)
{
    ...
}
```

But in C, this does not compare strings the way you expect. For now, the important practical rule is:

> To compare two strings in C, use `strcmp` from `<string.h>`.

### 4.6.1 `strcmp` and what it returns

The function:

```c
int strcmp(const char *s1, const char *s2);
```

returns an integer that indicates how the two strings compare:

- `0` if the strings are equal
- a negative number if `s1` comes “before” `s2`
- a positive number if `s1` comes “after” `s2`

This ordering is often described playfully as **ASCII-betical order**, because the comparison is based on the underlying numeric character codes (ASCII or compatible encodings).

Even if you only care about equality, this richer return value is useful in general because it can support sorting and ordering, not just yes/no equality.

### 4.6.2 A string-search example

If you have a Monopoly-inspired array:

```c
string strings[] = {"Battleship", "Boot", "Cannon", "Iron", "Thimble", "Top hat"};
```

then searching should look conceptually like:

```c
if (strcmp(strings[i], s) == 0)
{
    // found
}
```

If you forget to `#include <string.h>`, the compiler will complain because it has not been told that `strcmp` exists or how to call it.

---

## 4.7 A Simple Phone Book: From Parallel Arrays to a Better Data Structure

### 4.7.1 The “code smell” of parallel arrays

A first attempt at a phone book might use two arrays:

- One array of names
- One array of numbers

with the implicit assumption that index `i` in the names array corresponds to index `i` in the numbers array.

This works for tiny examples, but it tends to “smell” wrong: as the program grows, it is easy for the arrays to drift out of sync. Adding, removing, or rearranging entries becomes fragile.

This is a classic motivation for using a richer data structure: we want to keep related fields together.

### 4.7.2 Phone numbers as strings

Even though we call it a “phone number,” it is often best stored as a **string**, not an integer, because:

- Phone numbers can contain `+`, `-`, spaces, or parentheses.
- Phone numbers can be too long for typical integer types.
- You do not do arithmetic on phone numbers.

A good rule of thumb is:

> If you will not do math on it, and it may contain formatting, it is often best stored as a string.

### 4.7.3 Creating your own type with `struct` and `typedef`

C lets you define your own compound data type using a **structure**, or `struct`. A `struct` is a value that contains multiple fields, each with its own type.

A common pattern is:

```c
typedef struct
{
    string name;
    string number;
}
person;
```

This does two things:

- `struct { ... }` defines the structure layout: it has a `name` field and a `number` field.
- `typedef ... person;` creates a new type name, `person`, so you can declare variables of that type.

### 4.7.4 Using the dot operator to access fields

Once you have an array of `person`, you can keep each name with its number:

```c
person people[3];
```

To set or read fields inside a `struct`, you use the **dot operator** (`.`):

- `people[0].name` means “the name field of the first person”
- `people[0].number` means “the number field of the first person”

Conceptually, this lets you rewrite a phone book so that each entry is one coherent unit rather than a fragile pairing across two separate arrays.

### 4.7.5 Initialization and garbage values

If you create a `person` but do not initialize all its fields, the uninitialized fields will contain **garbage values**, just like uninitialized variables in general. You *can* do partial initialization in C, but you should treat it as dangerous unless you are very careful never to read the uninitialized field.

---

## 4.8 Sorting: Turning Unsorted Data Into Sorted Data

Searching gets dramatically faster when data is sorted (binary search is the classic example), but sorting itself has a cost. A natural question is:

> How expensive is it to sort, and can we sort efficiently enough that it’s worth it?

Sorting can be framed as:

- **Input**: an array of values in arbitrary order
- **Output**: the same values in increasing (or alphabetical) order

We will look at three sorting algorithms:

1. **Selection sort**
2. **Bubble sort**
3. **Merge sort**

The first two are simpler to understand but can be slow for large `n`. The third is a standard example of a faster, divide-and-conquer algorithm.

---

## 4.9 Selection Sort: Repeatedly Select the Smallest Remaining Element

### 4.9.1 The idea

Selection sort works by repeatedly selecting the smallest element from the unsorted portion of the array and swapping it into its correct position.

In human terms, if people are holding numbers:

1. Find the smallest number across the whole line.
2. Swap it into position 0.
3. Find the smallest number among positions 1 through the end.
4. Swap it into position 1.
5. Repeat.

A typical pseudocode formulation is:

```text
For i from 0 to n - 1:
    Find the smallest element between array[i] and array[n - 1]
    Swap it with array[i]
```

### 4.9.2 Running time: why it becomes quadratic

Selection sort makes many comparisons. On the first pass, it may compare roughly `n - 1` elements. On the second pass, roughly `n - 2`, then `n - 3`, and so on.

This sum:

```text
(n - 1) + (n - 2) + ... + 1
```

is proportional to `n^2`, more precisely `n(n - 1)/2`, which is dominated by the `n^2` term.

So:

- **Big O**: `O(n^2)`
- **Omega**: `Ω(n^2)` (even if the array is already sorted, selection sort still scans to “confirm” the smallest each time)
- Therefore **Theta**: `Θ(n^2)`

Selection sort does not naturally “get lucky” and stop early, because the algorithm as defined does not check whether work is unnecessary; it simply performs its full routine.

---

## 4.10 Bubble Sort: Fix Local Out-of-Order Pairs Repeatedly

### 4.10.1 The idea

Bubble sort repeatedly compares adjacent pairs and swaps them if they are out of order. Over time, large values “bubble” to the right, one swap at a time.

A common pseudocode version is:

```text
Repeat the following (n - 1) times:
    For i from 0 to n - 2:
        If array[i] and array[i + 1] are out of order:
            Swap them
```

The loop ends at `n - 2` (not `n - 1`) because the algorithm looks at `array[i + 1]`, and `i + 1` must remain within bounds.

### 4.10.2 Worst-case running time

This “nested loop” structure leads to roughly `(n - 1)(n - 1)` comparisons, which is still dominated by `n^2`.

So in the worst case:

- **Big O**: `O(n^2)`

### 4.10.3 A practical improvement: quit early if no swaps occur

Bubble sort has an important optimization: if you make a full pass through the array and perform **no swaps**, then the array must already be sorted, and there is no need to continue.

In pseudocode, you might add the idea:

```text
If no swaps occurred during a pass:
    Quit
```

With this improvement, bubble sort can be much faster on already-sorted (or nearly-sorted) data.

- **Best case (already sorted)**: it still must check adjacency across the list at least once, so it takes on the order of `n` steps.
  - **Omega**: `Ω(n)`

Because its worst and best cases differ, bubble sort is not naturally described by a single Theta bound in the same way selection sort is.

---

## 4.11 Recursion: Solving a Problem by Solving Smaller Versions of Itself

### 4.11.1 Definition

A function (or algorithm) is **recursive** if it calls itself. Recursion is not magical; it is a disciplined way to express “divide and conquer” by reusing the same logic on smaller inputs.

A recursive algorithm must have:

- A **recursive case**: the step where it calls itself on a smaller problem.
- A **base case**: a stopping condition that prevents infinite recursion.

Binary search is naturally recursive because “search the left half” and “search the right half” are the same operation applied to a smaller range.

### 4.11.2 Recursion vs. iteration

Earlier in the course, you expressed repetition with loops, such as:

- `for` loops
- `while` loops

Recursion is another way to represent repetition, often when the problem has a “self-similar” structure: smaller subproblems resemble the original problem.

---

## 4.12 A Recursive Structure Example: Printing a Pyramid

A pyramid of height 4 can be described recursively:

- A pyramid of height 4 is a pyramid of height 3, plus one more row.
- A pyramid of height 3 is a pyramid of height 2, plus one more row.
- …
- A pyramid of height 1 is a single row (or “nothing plus one row,” depending on how you define the base case).

### 4.12.1 Iterative approach (loop-based)

An iterative solution might use nested loops:

- Outer loop for each row
- Inner loop to print the correct number of `#` characters for that row

The crucial detail is choosing loop bounds so that the first row prints 1 `#`, the second prints 2 `#`, and so on.

### 4.12.2 Recursive approach (function calls itself)

A recursive `draw(n)` can be defined like this:

1. If `n <= 0`, return (base case).
2. Draw a pyramid of height `n - 1` (recursive case).
3. Print one row containing `n` `#` characters.

This mirrors the definition “height `n` is height `n - 1` plus one row.”

### 4.12.3 Why the base case matters

If you write `draw(n - 1)` without a base case, `n` will eventually become `0`, then `-1`, then `-2`, and so on. Since integers are signed by default, the recursion would not stop on its own. A compiler may even warn that “all paths through this function will call itself” if it can see that no base case exists.

The base case is what makes recursion safe and finite.

---

## 4.13 Merge Sort: A Faster Sorting Algorithm via Divide and Conquer

Selection sort and bubble sort can both be `O(n^2)`, which becomes prohibitively slow as `n` grows. To do better, we return to divide and conquer.

### 4.13.1 The idea (high level)

Merge sort’s pseudocode is concise:

```text
If the array has only one element:
    Quit (it is already sorted)
Sort the left half
Sort the right half
Merge the sorted halves
```

This is recursive: “sort the left half” and “sort the right half” are the same sorting problem on smaller arrays.

### 4.13.2 What “merge” means

The merge step assumes you have two sorted halves, such as:

- Left: `1 3 4 6`
- Right: `0 2 5 7`

To merge them into one sorted list:

- Point at the first element of each half.
- Repeatedly take the smaller of the two pointed-at elements and append it to an output array.
- Advance the pointer in the half you took from.
- Continue until all elements are consumed.

This “stitching together” is efficient because each element is copied exactly once during the merge.

### 4.13.3 Time–space tradeoff

Merge sort typically uses **extra space** (temporary arrays) while merging. This illustrates a common tradeoff in computing:

- If you are willing to use more **space**, you can often reduce **time**.
- If you restrict yourself to constant extra space, you may be forced into slower methods like selection sort or bubble sort.

Merge sort is fast in large part because it embraces additional memory to make merging simple and systematic.

### 4.13.4 Running time: `n log n`

Merge sort divides the problem in half repeatedly:

- The number of times you can halve `n` until reaching 1 is on the order of `log n`.

At each “level” of halving, the merge work across all subarrays sums to about `n` operations (you are moving or comparing each element during merging).

So total work is:

- about `log n` levels
- times about `n` work per level

giving:

- **Big O**: `O(n log n)`
- **Omega**: `Ω(n log n)`
- Therefore **Theta**: `Θ(n log n)`

This places merge sort in a fundamentally better category than `n^2` sorts for large inputs.

---

## 4.14 Putting It All Together: Choosing Algorithms Intelligently

At this point, you have several key algorithmic tools and a language for comparing them:

- **Linear search**: simple, works on unsorted data, worst case `O(n)`
- **Binary search**: fast, but requires sorted data, worst case `O(log n)`
- **Selection sort**: conceptually straightforward, but `Θ(n^2)`
- **Bubble sort**: also `O(n^2)` worst case, but can be `Ω(n)` best case with an early-exit optimization
- **Merge sort**: uses recursion and extra space to achieve `Θ(n log n)`

You also have an important design lesson from building a phone book:

- When data fields belong together, represent them together.
- In C, you can do this by creating your own types with `struct` and `typedef`, and accessing fields with the dot operator.

These ideas—data organization, algorithm choice, and performance reasoning—are not “extra” topics separate from programming. They are the core of what it means to write software that continues to work well as the size of the world (and your input) grows.