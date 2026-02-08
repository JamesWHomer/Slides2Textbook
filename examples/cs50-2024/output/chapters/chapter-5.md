# Chapter 5: Week 4 — Memory: Hexadecimal, Pointers, Strings, Dynamic Allocation, and Files

Week 4 is where C stops feeling like “a slightly awkward Python” and starts revealing what it has been all along: a language that lets you talk directly about **memory**, meaning the bytes inside your computer where programs, variables, and files ultimately live. The goal this week is not just to learn new syntax, but to develop a concrete mental model for what your code *does* underneath the hood, so that when something breaks—especially in confusing ways like a segmentation fault—you can reason your way to the cause.

This chapter builds that model in layers:

- We begin with how images can be represented as bits, and why **hexadecimal** is a convenient way to talk about those bits.
- We then introduce **addresses** and **pointers**, the tools C gives you to refer to locations in memory.
- We revisit **strings** and reveal what they really are in C: not a special “string” type, but pointers to characters.
- We learn how to correctly **compare** and **copy** strings by working with memory safely.
- We introduce **dynamic memory allocation** with `malloc` and `free`, and a debugging tool, **valgrind**, that helps detect memory bugs.
- We explore the **stack** and the **heap**, and why passing values to functions sometimes fails to change the original variables.
- Finally, we use pointers to move beyond the keyboard and screen and start working with **files**, including copying binary files byte-by-byte.

---

## 5.1 Pixels, Bits, and the Limits of “Enhance”

A digital image looks smooth and detailed on your screen, but it is ultimately just a **grid** of tiny dots called **pixels**. Each pixel stores some information about its color, and the image is simply the collection of all those pixels arranged by row and column.

A useful way to see this is to imagine a very small “pixel art” image made from a limited grid. If each pixel can only be black or white, then one simple representation is:

- `0` means black
- `1` means white

A grid of 0s and 1s can form a recognizable picture (like a smiley face) even though the data is just bits. This observation matters because it highlights a practical limit: if an image contains only so many pixels, then zooming in eventually reveals blocks, not hidden detail. Hollywood-style “enhance, enhance, enhance” is constrained by the fact that the file has a finite amount of information.

Later in the course, you will see that machine learning systems can sometimes *predict* missing detail (by statistical inference), but that is not the same thing as “recovering” information that was never stored in the file to begin with.

---

## 5.2 Color as Numbers: RGB and the Rise of Hexadecimal

Black-and-white pixels are a good starting point, but real images need color. A common convention is **RGB**, short for:

- **R**ed
- **G**reen
- **B**lue

A color is represented as a mixture of these three components. Each component is stored as a number—commonly from 0 to 255—where:

- `0` means “none of that color”
- `255` means “as much of that color as possible”

So:

- black is `(0, 0, 0)`
- white is `(255, 255, 255)`
- pure red is `(255, 0, 0)`
- pure green is `(0, 255, 0)`
- pure blue is `(0, 0, 255)`

### 5.2.1 The notation you see in tools: `#RRGGBB`

In many graphics tools (and web development), RGB colors are written in a compact form that looks like:

- `#000000` for black
- `#FFFFFF` for white
- `#FF0000` for red
- `#00FF00` for green
- `#0000FF` for blue

This is not decimal notation. It is **hexadecimal**.

---

## 5.3 Hexadecimal (Base 16)

**Hexadecimal** is a number system with 16 digits instead of 10. It uses:

- `0 1 2 3 4 5 6 7 8 9`
- `A B C D E F` to represent values 10 through 15

So counting in hexadecimal goes:

- `0, 1, 2, ... 9, A, B, C, D, E, F, 10, 11, 12, ...`

Hexadecimal is also called **base 16**, by analogy with **decimal** being base 10.

### 5.3.1 Place values in hexadecimal

Just as decimal has place values:

- ones, tens, hundreds, …

hexadecimal has:

- ones, sixteens, two-hundred-fifty-sixes, …

So in a two-digit hexadecimal number:

- the right digit is the **16⁰ (ones)** place
- the left digit is the **16¹ (sixteens)** place

For example:

- `0x00` is 0
- `0x01` is 1
- `0x0A` is 10
- `0x10` is 16
- `0xFF` is 255 (because `15 * 16 + 15 = 255`)

### 5.3.2 Why programmers like hexadecimal

Hexadecimal is popular not because it is “more correct” than decimal, but because it is **convenient** when working close to the hardware.

A key fact is:

- 1 hexadecimal digit represents **4 bits** (because 16 possibilities = 2⁴)
- 2 hexadecimal digits represent **8 bits**, which is exactly **1 byte**

So when you see something like `FF`, you can think “that is one byte worth of bits,” and when you see `#RRGGBB`, you can interpret it as:

- `RR` = 1 byte for red
- `GG` = 1 byte for green
- `BB` = 1 byte for blue

This is why a tool can represent 255 as `FF`—it aligns naturally with bytes.

### 5.3.3 The `0x` prefix

A practical problem with hexadecimal is ambiguity: `10` could mean ten (decimal) or sixteen (hex). A common convention is to prefix hexadecimal with:

- `0x`

So:

- `0x10` means “hexadecimal 10,” which is decimal 16.

This prefix is not mathematical; it is just a label to the reader (and, in some contexts, to the compiler).

---

## 5.4 Memory as a Grid of Bytes and the Idea of an Address

To reason about pointers, it helps to picture memory as a large grid of bytes. Each byte has a **location**, called an **address**. Programs store values in memory, and the CPU needs a way to refer to “which byte” holds “which data.”

Computers typically represent addresses using **hexadecimal** because addresses are naturally byte-based and hexadecimal matches bytes cleanly.

When you write:

```c
int n = 50;
```

your program is asking the computer to reserve enough bytes for an `int` (commonly 4 bytes) and store the bits representing 50 in those bytes. Those bytes live somewhere in memory, at some address like `0x...` (the exact value is not important, and it will vary each time you run the program).

---

## 5.5 Addresses and Pointers in C

C gives you direct access to these memory locations.

### 5.5.1 The address-of operator: `&`

The operator `&` means:

> “Give me the address of this variable.”

Example:

```c
int n = 50;
printf("%p\n", &n);
```

- `%p` is the `printf` format code for a pointer (an address).
- `&n` is the address where `n` is stored.

You will see an output like:

- `0x7ffc...` (some large hexadecimal number)

### 5.5.2 What is a pointer?

A **pointer** is a variable whose value is an address.

For example:

```c
int n = 50;
int *p = &n;
```

Read this slowly:

- `int *p` declares `p` as “a pointer to an int,” meaning it can store the address of an integer.
- `&n` is the address of `n`.
- so `p` now stores the location of `n`.

Pointers on modern systems are commonly **8 bytes** (64 bits). Historically, many systems used 4-byte (32-bit) pointers, which limited the total addressable memory. As machines gained more memory, pointer sizes increased to represent larger address spaces.

### 5.5.3 The dereference operator: `*`

The operator `*` is used in two related but distinct ways:

1. In a declaration, it means “this variable is a pointer”:

   ```c
   int *p;
   ```

2. In an expression, it means “go to that address” (dereference it):

   ```c
   printf("%i\n", *p);
   ```

If `p` stores the address of `n`, then `*p` means “the integer located at the address stored in `p`,” which is the same as `n`.

So:

```c
int n = 50;
int *p = &n;

printf("%p\n", p);   // prints the address
printf("%i\n", *p);  // prints 50
```

Even though the `*` character appears in both places, it is not multiplication here. It is pointer syntax, and context determines whether it is declaring a pointer or dereferencing one.

---

## 5.6 Strings Revisited: The Training Wheels Come Off

For weeks, you have used:

```c
string s = "HI!";
```

and thought of `s` as “a string.” That is a good mental model, but in *C itself*, there is no built-in `string` type. Instead, a C string is an array of characters, and the “string variable” is typically just the address of the first character.

### 5.6.1 The null terminator

A string like `"HI!"` is not stored as three bytes. It is stored as four:

- `'H'`
- `'I'`
- `'!'`
- `'\0'` (the **null terminator**)

The null terminator is a byte of all zero bits, and it marks the end of the string. Functions like `printf("%s", s)` print characters until they reach `'\0'`.

### 5.6.2 What `string` really is: `char *`

In CS50, `string` is an abstraction provided by the CS50 library. Underneath, it is:

- `char *`

That is, “a pointer to char,” interpreted as “the address of the first character in a sequence of characters.”

So these are conceptually the same:

```c
string s = "HI!";
```

and (in “raw C”):

```c
char *s = "HI!";
```

The double quotes do something important for you: the compiler stores the characters in memory and initializes `s` to the address of the first character. That is why you do **not** write `&"HI!"`—the compiler already gives you the address of the first character automatically.

### 5.6.3 Printing a string address versus printing a string

Because a string variable is really an address:

- `%p` prints the address itself
- `%s` treats the address as “start of a string” and prints characters until `'\0'`

Example:

```c
char *s = "HI!";

printf("%p\n", s);   // address of 'H'
printf("%s\n", s);   // HI!
```

And you can confirm that `s` is the same as `&s[0]`:

```c
printf("%p\n", s);
printf("%p\n", &s[0]);
```

### 5.6.4 Strings as contiguous memory

Because the characters are stored contiguously:

- if `s` points to `'H'` at some address, then `'I'` is at the next address, and so on.

This is exactly the same contiguous-memory idea you used with arrays in week 2—strings are simply arrays of `char` with a special terminator at the end.

---

## 5.7 Pointer Arithmetic and “Syntactic Sugar”

Once you accept that `s` is “the address of the first character,” you can manipulate strings using pointer operations.

If `s` is a `char *`, then:

- `s + 1` is the address of the next character
- `s + 2` is the address of the character after that

And dereferencing follows the pointer:

```c
printf("%c\n", *s);       // first character
printf("%c\n", *(s + 1)); // second character
printf("%c\n", *(s + 2)); // third character
```

This is closely related to array indexing. In fact:

- `s[0]` is equivalent to `*(s + 0)`
- `s[1]` is equivalent to `*(s + 1)`
- `s[2]` is equivalent to `*(s + 2)`

Array indexing is therefore a kind of **syntactic sugar**: a friendlier way to write pointer arithmetic.

---

## 5.8 Comparing Strings: Why `==` Does Not Work

In week 3, you used `strcmp` to compare strings and were warned not to use `==`. Now you can see precisely why.

Consider:

```c
char *s = get_string_somehow();
char *t = get_string_somehow();

if (s == t)
{
    printf("same\n");
}
else
{
    printf("different\n");
}
```

Because `s` and `t` are pointers, `s == t` compares their **addresses**, not the characters they point to. Even if the user types the same word twice, those two strings may live in two different places in memory, so their addresses differ, and `==` will report “different.”

### 5.8.1 The correct tool: `strcmp`

To compare the characters, you need a function that walks through both strings and compares them character-by-character:

```c
#include <string.h>

if (strcmp(s, t) == 0)
{
    printf("same\n");
}
else
{
    printf("different\n");
}
```

Recall what `strcmp` returns:

- `0` if equal
- a negative value if `s` comes “before” `t`
- a positive value if `s` comes “after” `t`

The exact positive/negative value is not meaningful; only the sign matters.

---

## 5.9 Copying Strings: Assignment Copies the Address, Not the Characters

A second subtle bug appears when you try to “copy a string” the same way you copy an integer:

```c
char *s = get_string_somehow();
char *t = s;  // looks like a copy, but isn't
```

This does not duplicate the characters. It duplicates the pointer value, meaning:

- `t` points to the same memory as `s`

So if you modify the string via `t`, you are also modifying `s`, because they share one underlying array of characters.

A classic demonstration is “capitalize the first letter of the copy.” If you do:

```c
t[0] = toupper(t[0]);
```

then `s[0]` changes too, because `s` and `t` are aliases for the same string in memory.

---

## 5.10 Dynamic Memory: `malloc`, `free`, and Making a Real Copy

To actually copy a string into a new location, you need to allocate new memory for the copy, then copy the bytes.

### 5.10.1 `malloc`: memory allocate

`malloc` asks the operating system for a chunk of memory and returns the **address of the first byte** of that chunk.

You pass `malloc` the number of bytes you want.

A typical pattern to copy a string is:

1. Compute the number of bytes needed (string length + 1 for `'\0'`).
2. Allocate that many bytes.
3. Copy characters, including the null terminator.

Example:

```c
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

char *s = get_string_somehow();

char *t = malloc(strlen(s) + 1);
if (t == NULL)
{
    // out of memory
    return 1;
}

// Copy the bytes, including '\0'
for (int i = 0; i <= strlen(s); i++)
{
    t[i] = s[i];
}

if (strlen(t) > 0)
{
    t[0] = toupper(t[0]);
}

// use s and t...

free(t);
```

Two details matter here:

- The loop uses `<= strlen(s)` so it copies the null terminator at the end. If you only copy characters up to `< strlen(s)`, you will forget `'\0'`, and `t` will not be a valid C string.
- `malloc` can fail. When it fails, it returns `NULL`, a special value meaning “address 0,” used as a sentinel for “no valid address.”

### 5.10.2 `strcpy`: don’t reinvent the wheel

Because copying strings is so common, C provides:

- `strcpy(destination, source)` in `<string.h>`

So instead of a manual loop you can do:

```c
char *t = malloc(strlen(s) + 1);
if (t == NULL)
{
    return 1;
}

strcpy(t, s);
```

(You may see the name said informally as “string copy”; the actual function name in standard C is `strcpy`.)

### 5.10.3 `free`: give memory back

Every `malloc` should eventually be paired with `free`:

```c
free(t);
```

If you allocate memory repeatedly and never free it, your program can slowly consume more and more memory, causing a **memory leak**. Over time, leaks can make programs sluggish or unstable, and in large systems they can become serious reliability issues.

---

## 5.11 Debugging Memory Bugs with Valgrind

Memory bugs can be deceptive because a program can compile and even appear to run, while still doing something invalid. To help detect common mistakes, you can use **valgrind**, a tool that runs your program and reports memory-related errors such as:

- invalid reads/writes (touching memory you don’t own)
- memory leaks (allocating without freeing)

### 5.11.1 Invalid write example: writing past an allocated block

Suppose you allocate space for 3 integers:

```c
int *x = malloc(3 * sizeof(int));
```

Valid indices are:

- `x[0]`, `x[1]`, `x[2]`

If you accidentally write `x[3]`, you are writing beyond the allocated memory. This can cause crashes—or worse, silently corrupt other data.

Valgrind reports errors like “Invalid write of size 4,” where 4 is the size of an `int` on that system.

### 5.11.2 Memory leak example: forgetting to `free`

If you allocate:

```c
int *x = malloc(3 * sizeof(int));
```

but never call:

```c
free(x);
```

valgrind will report something like “definitely lost,” indicating bytes that were allocated and never reclaimed.

---

## 5.12 Garbage Values: The Danger of Uninitialized Variables

A **garbage value** is whatever bits happen to already be in a region of memory that you have not initialized. In C, local variables are not automatically set to 0. If you declare:

```c
int scores[1024];
```

and immediately print the contents without storing anything first, you will see unpredictable numbers. Those numbers are not random in a mystical sense; they are simply leftover bits from prior memory use.

Garbage values become far more dangerous when they appear in pointers.

---

## 5.13 Segmentation Faults and Dereferencing Bad Pointers

A **segmentation fault** occurs when your program tries to access memory it is not allowed to access. A common way to cause this is:

- dereferencing an uninitialized pointer

Consider this pattern:

```c
int *x = malloc(sizeof(int));
*x = 42;

int *y;     // uninitialized!
*y = 13;    // dereferencing garbage address -> likely crash
```

Here, `y` contains garbage bits. Those bits are treated as an address. `*y = 13` means “go to that address and write 13,” which could be anywhere—often an invalid region—so the program crashes.

A popular claymation metaphor (“Binky”) dramatizes this: pointers begin as arrows that point nowhere, and dereferencing them before setting up the pointee causes chaos. The core lesson is serious even if the presentation is playful:

> Allocating a pointer variable is not the same as allocating the memory it should point to.

---

## 5.14 The Stack and the Heap

To understand why some functions fail to modify variables, it helps to know how memory is typically organized while a program runs.

A simplified model divides memory into regions:

- **Machine code** (the compiled instructions)
- **Global variables** (variables defined outside all functions)
- **Heap** (dynamic memory allocated with `malloc`)
- **Stack** (function call frames: parameters and local variables)

Two regions matter most this week:

### 5.14.1 The heap

The **heap** is where memory comes from when you call `malloc`. It is used for data that should outlive a single function call, such as dynamically sized arrays or strings whose size is not known until runtime.

### 5.14.2 The stack

The **stack** stores function call frames (often called **stack frames**). Each time you call a function, a new frame is created containing:

- the function’s parameters
- the function’s local variables

When the function returns, its stack frame is discarded. That means:

> Local variables inside a function do not survive after the function returns.

### 5.14.3 Overflows: stack, heap, and buffers

Because the stack and heap both use finite memory, programs can break if they use too much:

- **stack overflow**: too many or too-large stack frames, often from deep recursion
- **heap overflow** (in one sense): using heap memory incorrectly, or allocating so much that memory is exhausted
- **buffer overflow**: writing past the end of an array (a “buffer”), corrupting adjacent memory

These issues are not just academic; they are sources of crashes and, historically, security vulnerabilities.

---

## 5.15 Why the “Swap” Function Didn’t Work (Passing by Value)

Consider a function intended to swap two integers:

```c
void swap(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
}
```

And a `main` program:

```c
int x = 1;
int y = 2;

swap(x, y);

printf("%i %i\n", x, y);
```

Even though the logic inside `swap` is correct, `x` and `y` do not change. The reason is:

- C passes function arguments **by value**, meaning it copies them.
- `a` and `b` are copies of `x` and `y`.
- Swapping `a` and `b` swaps only the copies inside the `swap` stack frame.
- When `swap` returns, that frame disappears, and `x` and `y` remain unchanged.

---

## 5.16 Swapping Correctly: Passing Pointers (Pass by Reference)

To swap the original variables, you must give the function access to their memory addresses:

```c
void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

Now the call site must pass addresses:

```c
swap(&x, &y);
```

This is the same underlying idea as earlier:

- `&x` gives the address of `x`
- `*a` dereferences the pointer to access and modify the integer stored there

This pattern—passing pointers so a function can modify the caller’s variables—is one of the most important uses of pointers in C.

---

## 5.17 Input Without Training Wheels: `scanf` and Its Risks

So far, CS50’s `get_int` and `get_string` have handled many details for you. In standard C, a commonly used function for input is:

- `scanf`

### 5.17.1 Scanning an integer

This is relatively straightforward:

```c
int n;
printf("n: ");
scanf("%i", &n);
printf("n: %i\n", n);
```

The crucial detail is `&n`: `scanf` needs the **address** of `n` so it can store the user’s input into that variable. If you passed `n` instead of `&n`, `scanf` would receive only a copy and would not be able to change the original.

### 5.17.2 Scanning a string: where should the characters go?

Strings are harder because `scanf("%s", ...)` needs a place to store an *unknown number of characters*. If you write:

```c
char *s;
scanf("%s", s);
```

you are in trouble because `s` is an uninitialized pointer; it points nowhere valid. `scanf` will try to write to the garbage address stored in `s`, often causing a segmentation fault.

To use `scanf` safely, you need allocated space, such as an array:

```c
char s[4];
scanf("%s", s);
```

Now `s` is a valid buffer of 4 bytes, and `scanf` can write into it.

But this is still dangerous: if the user types more than 3 characters (plus `'\0'`), the input will overflow the buffer and may crash or corrupt memory. The deeper point is:

> In C, safe string input is difficult because you rarely know in advance how long the user’s input will be.

CS50’s `get_string` avoids this by allocating and reallocating memory as the user types, growing the buffer dynamically so it fits the input.

---

## 5.18 File I/O: Opening, Writing, Reading, and Closing Files

Once you understand memory and pointers, you can start manipulating **files**: stored data such as text documents, CSVs, and images.

Common file functions in C include:

- `fopen` / `fclose` (open/close a file)
- `fprintf` / `fscanf` (print to / scan from a file, often for text)
- `fread` / `fwrite` (read/write raw bytes, often for binary formats like images)
- `fseek` (jump to a position in a file, like fast-forward/rewind)

### 5.18.1 Writing a simple phonebook to a CSV file

A CSV file (comma-separated values) is a plain text format where commas separate columns and newlines separate rows. Spreadsheet programs can open it easily.

A program can:

1. open a file in **append mode** (`"a"`) so it adds new entries instead of overwriting,
2. ask the user for a name and number,
3. write a line like `name,number\n`,
4. close the file.

In C, the file handle is a pointer-like type:

- `FILE *`

Example structure:

```c
FILE *file = fopen("phonebook.csv", "a");
if (file == NULL)
{
    return 1;
}

char *name = get_string_somehow();
char *number = get_string_somehow();

fprintf(file, "%s,%s\n", name, number);

fclose(file);
```

A key safety habit appears here: because `fopen` returns a pointer, you should check for `NULL`. A `NULL` file pointer usually indicates the file could not be opened (missing permissions, missing directory, etc.).

---

## 5.19 Copying Binary Files Byte-by-Byte

Text output with `fprintf` is useful, but images and other binary files are not plain text. To copy a binary file, you can read raw bytes and write them to a new file.

### 5.19.1 A `byte` type

C does not have a built-in `byte` type in the simplest sense, but it provides fixed-width integer types in `<stdint.h>`, including:

- `uint8_t`: an unsigned 8-bit integer (exactly one byte)

You can create a friendlier synonym with `typedef`:

```c
#include <stdint.h>
typedef uint8_t byte;
```

This is the same technique used by CS50’s `string`, which is implemented as a synonym for `char *`.

### 5.19.2 A small copy program using `fread` and `fwrite`

A minimal file-copy strategy is:

- open source file for reading in binary mode: `"rb"`
- open destination file for writing in binary mode: `"wb"`
- repeatedly read one byte from source and write it to destination until there are no more bytes

Conceptually:

```c
byte b;
while (fread(&b, sizeof(b), 1, src) == 1)
{
    fwrite(&b, sizeof(b), 1, dst);
}
```

This works because:

- `fread` returns the number of “items” successfully read (here we read 1 item of size 1 byte)
- when the file ends, it returns 0, and the loop stops

This style of code makes concrete a powerful idea: a file is ultimately a sequence of bytes, and you can process it at the byte level if you have the right tools.

---

## 5.20 From Bytes to Images: Bitmap Files and Filters (A Preview)

A bitmap image format (BMP) stores an image as pixel data in a structured binary file. Because you can now read and write bytes from files, you can begin writing programs that manipulate images by:

- reading pixel values
- modifying them (for example, changing colors)
- writing the modified pixels to a new file

This is the foundation of common “filters”:

- **grayscale** (convert RGB to shades of gray)
- **reflection** (mirror the image)
- **blur** (smudge pixels by averaging neighbors)
- **edge detection** (highlight boundaries by comparing neighboring pixels)

At first glance, these effects seem high-level, like features of an app. In reality, they reduce to systematic transformations of pixel data stored as bytes in an image file.

---

## 5.21 Summary: What Week 4 Adds to Your Mental Model

After this week, you should be able to think about C programs in a lower-level, more accurate way:

- **Memory** is bytes; variables occupy specific bytes at specific **addresses**.
- **Hexadecimal** is a convenient shorthand for bytes and addresses.
- `&` gets an address; `*` dereferences an address.
- A **pointer** stores an address, and pointers are central to how C works.
- A C **string** is an array of `char` ending with `'\0'`, and a “string variable” is typically a `char *` pointing to the first character.
- Comparing strings requires `strcmp` because `==` compares addresses, not characters.
- Copying strings requires allocating new memory (`malloc`) and copying bytes (`strcpy`), and allocated memory must be released (`free`).
- Tools like **valgrind** help detect memory bugs that compilers often cannot.
- The **stack** holds function frames; the **heap** holds dynamically allocated memory.
- Passing values to functions copies them; passing pointers enables functions to modify the caller’s memory.
- File I/O functions (`fopen`, `fprintf`, `fread`, `fwrite`, `fclose`) let you move beyond the keyboard and screen and manipulate persistent data, including binary files like images.

These ideas make C feel more complex, but they also explain behaviors that used to feel mysterious. Once you can “see” the memory model, many bugs become less random and more like solvable puzzles with clear rules.