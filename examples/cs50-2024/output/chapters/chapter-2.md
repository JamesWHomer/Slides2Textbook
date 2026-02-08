# Chapter 2: Week 1 — C, Compilation, Control Flow, and the Limits of Representation

Week 0 deliberately focused on programming ideas without the distractions of punctuation, file systems, and compilers. In week 1, CS50 keeps the *ideas* from Scratch—functions, conditionals, loops, variables, return values, and abstraction—but now expresses those ideas in a traditional text-based language: **C**. C can look cryptic at first, largely because it makes you write down details that Scratch hides behind blocks, but those details are also what make C a powerful lens for understanding what computers are actually doing underneath the hood.

The goal of learning C in CS50 is not “to memorize C,” but to add a new set of tools to your problem-solving toolkit. Along the way, you also begin to see a second major theme of computer science: computers are not magical, and they are not infinitely precise. Their memory is finite, their number representations have limits, and those limits can cause real failures in real systems.

---

## 2.1 From Scratch Blocks to C Text: Same Concepts, New Syntax

In Scratch, a first program might be:

- **when green flag clicked**
- **say** `"hello, world"`

In C, the analogous program uses a function named `printf` (pronounced “print f,” where the `f` hints at *formatted* printing):

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
}
```

At first glance, this is more visually complicated than Scratch. It contains symbols you do not normally use in English writing—parentheses, curly braces, semicolons, and a `#include` line. Early on, it helps to treat much of this as required “boilerplate,” while keeping your attention on the central idea:

- **`printf("hello, world\n");`** is the spiritual equivalent of Scratch’s **say** block.

The rest of the file is the surrounding structure that C requires so that the computer knows where your program begins, and what tools (libraries) you intend to use.

---

## 2.2 Source Code vs. Machine Code, and the Role of a Compiler

A computer ultimately executes **machine code**: instructions represented as patterns of bits (0s and 1s). Humans, however, write **source code**, which is the human-readable text you type in a language like C.

To get from source code to machine code, you use a **compiler**:

- A **compiler** is a program that translates code written in one language (C source code) into another language (machine code) that the computer can execute.

This translation step is essential. Without it, you would have to write programs directly in 0s and 1s—possible in principle, but painfully slow and error-prone in practice.

---

## 2.3 The CS50 Development Environment: `cs50.dev`, VS Code, and the Terminal

Rather than requiring every student to install identical tools on their own laptops (which vary across Windows, macOS, Linux, versions, and configurations), CS50 standardizes your environment using the cloud:

- You work at **https://cs50.dev**, a browser-based environment that includes:
  - **Visual Studio Code (VS Code)**, a widely used professional code editor.
  - A pre-configured system with compilers and tools you need for the course.

### 2.3.1 GUI vs. CLI

In this environment you use both:

- A **graphical user interface (GUI)**: tabs, file explorer panes, clickable elements.
- A **command-line interface (CLI)** (also called a **terminal** or **console**): a text-based interface where you type commands.

A CLI can feel like a step backward if you are used to clicking icons, but it is often faster once you gain comfort with it, particularly for repetitive developer tasks like compiling, running, and moving files.

### 2.3.2 Your Prompt and the `$`

In many terminals you will see a symbol such as:

- `$`

This is called a **prompt**. It is not currency; it is simply a convention indicating where you should type commands.

---

## 2.4 Your First C Program: Writing, Compiling, Running

CS50 introduces a simple three-step rhythm for C programs:

1. **Write** the code (create/edit a `.c` file)
2. **Compile** the code (convert it to machine code)
3. **Run** the program (execute it)

In CS50’s environment, those steps often look like this:

```text
code hello.c
make hello
./hello
```

### 2.4.1 Creating a File: `code hello.c`

The command:

```text
code hello.c
```

opens (or creates) a file named `hello.c`. The `.c` extension is the conventional file extension for C source code.

#### File-naming conventions that save time later

When working in a terminal, certain habits prevent avoidable problems:

- Prefer **lowercase** filenames.
- Avoid **spaces** in filenames.
- Keep extensions lowercase as well.

These are not laws of nature, but they reduce friction because spaces and unusual characters complicate command-line typing.

### 2.4.2 Compiling: `make hello`

After writing code, you compile it:

```text
make hello
```

A common beginner mistake is to type `make hello.c`. In CS50’s workflow, you typically compile by naming the *program you want to produce* (`hello`), not the source file. The tool `make` will look for `hello.c` and produce an executable program named `hello`.

When compilation succeeds, it often prints **nothing**. Paradoxically, that silence is good news. If compilation fails, you may see many lines of error messages; those messages are trying to point you toward mistakes in your code.

### 2.4.3 Running: `./hello`

To run the compiled program:

```text
./hello
```

The `./` means “run the program named `hello` located in the current folder.”

This is conceptually similar to double-clicking an application icon, but in the CLI you explicitly state where the program is located.

---

## 2.5 `printf`, Newlines, and Escape Sequences

If you write:

```c
printf("hello, world");
```

your output may appear immediately followed by your next terminal prompt (`$`) on the same line. That is not “wrong” as far as the computer is concerned, but it is usually undesirable formatting for humans.

To print a newline at the end, you include:

- `\n`

```c
printf("hello, world\n");
```

### 2.5.1 What `\n` actually is

`\n` is an **escape sequence**, meaning it is a special two-character pattern inside a string that represents a single special character (a newline). It is “escaped” because it would be hard or inconvenient to type the newline character directly inside the quotes as part of the string.

### 2.5.2 Printing a literal backslash (escaping the escape)

Sometimes you want to print characters that normally have special meaning. A common pattern in programming is:

- To print a literal backslash, you often need to escape it with another backslash.

For example, printing `\n` literally (as two visible characters) involves using `\\n` in many contexts.

---

## 2.6 Libraries, Header Files, and `#include`

C comes with many useful functions, but those functions are organized into **libraries**—bundles of code written by other people that you can reuse rather than reinvent.

To use functions from a library, you often include a **header file**, typically with a `.h` extension:

```c
#include <stdio.h>
```

- `stdio.h` is the “standard input/output” header.
- `printf` is associated with this library, so including `stdio.h` tells the compiler that `printf` exists and how it is meant to be used.

A helpful mental model early on is:

- `#include <...>` is like telling the compiler: “Before compiling, bring in the definitions I need from this library.”

### 2.6.1 Documentation: manual pages and `manual.cs50.io`

Professional documentation for C exists in “manual pages,” but those are often written for experienced programmers. CS50 provides friendlier documentation at:

- **https://manual.cs50.io**

This documentation is especially useful when you know *what you want to do* (“get input,” “print formatted output”) but you do not yet remember the exact function names or argument patterns.

---

## 2.7 The CS50 Library: Training Wheels for Input (`cs50.h`)

C is an older language, and it does not make user input easy for beginners. To keep your focus on problem-solving rather than low-level input parsing, CS50 provides its own library with helper functions, included via:

```c
#include <cs50.h>
```

This gives you functions such as:

- `get_string` — prompt the user for text
- `get_int` — prompt the user for an integer
- `get_float` — prompt the user for a floating-point number
- `get_char` — prompt the user for a single character
- and others

These are “training wheels” in the sense that they simplify early weeks; later in the course, you will learn what these functions are doing and how to work without them.

---

## 2.8 Variables and Types: `string`, `int`, `char`, `float`, `double`

In Scratch, you can create a variable without specifying what kind of value it stores. In C, you generally must specify a variable’s **type**, which tells the compiler how to represent the value in memory.

### 2.8.1 A greeting program with input

In Scratch, the “ask … and wait” block returns a value (the user’s answer). In C with CS50’s library, the analogous program is:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string answer = get_string("What's your name? ");
    printf("hello, %s\n", answer);
}
```

Here:

- `get_string("What's your name? ")` prompts the user and **returns** the typed text.
- `string answer = ...` stores that return value in a variable named `answer`.
- `printf("hello, %s\n", answer);` prints a formatted string where `%s` is replaced by the value of `answer`.

### 2.8.2 Strings, format codes, and the “formatted” in `printf`

Unlike Scratch’s “join” block, C often uses **format codes** inside a format string:

- `%s` means “insert a **string** here”
- `%i` means “insert an **integer** here”
- `%f` means “insert a **floating-point number** here”
- `%li` is commonly used for a **long integer** (more on “long” later)

The important idea is that `printf` can take multiple arguments:

```c
printf("hello, %s\n", answer);
```

- The first argument is the format string: `"hello, %s\n"`
- The second argument is the value to plug in where `%s` appears: `answer`

### 2.8.3 Single characters vs. strings: `char` and quotes

C distinguishes between:

- A **string**: a sequence of characters, written with **double quotes** `"..."`.
- A **char**: a single character, written with **single quotes** `'...'`.

Example:

```c
char c = get_char("Do you agree? ");
```

Later, when comparing:

```c
if (c == 'y')
{
    printf("Agreed\n");
}
```

Using `'y'` (single quotes) is essential here, because it is one character, not a whole string.

---

## 2.9 Conditionals and Boolean Expressions in C

Scratch’s conditionals map directly to C conditionals. In C, the structure is:

```c
if (condition)
{
    // code if condition is true
}
else
{
    // code if condition is false
}
```

The `condition` is a **Boolean expression**: a yes/no question that evaluates to true or false.

### 2.9.1 Comparing values: `<`, `>`, and `==` vs. `=`

In C:

- `=` is **assignment** (“put the value on the right into the variable on the left”)
- `==` is **equality comparison** (“are these two values equal?”)

This difference matters. For example:

```c
if (x == y)
{
    printf("x is equal to y\n");
}
```

Using `=` here would mean something else entirely, and is a classic source of bugs.

### 2.9.2 A comparison program: `compare.c`

A simple program that compares two integers might look like:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("What's x? ");
    int y = get_int("What's y? ");

    if (x < y)
    {
        printf("x is less than y\n");
    }
    else if (x > y)
    {
        printf("x is greater than y\n");
    }
    else
    {
        printf("x is equal to y\n");
    }
}
```

Notice a design point: the final case does not need to test `x == y`. If `x` is not less than `y` and not greater than `y`, then it must be equal. Using `else` is both simpler and typically more efficient.

### 2.9.3 Input validation (and why CS50’s `get_int` helps)

If the user types something that is not a number (like `"cats"`), CS50’s `get_int` will keep prompting until it receives a valid integer. This is *not* C’s default behavior; it is part of the CS50 library’s beginner-friendly design.

---

## 2.10 Logical Operators: “or” (`||`) and “and” (`&&`)

When checking multiple conditions, C uses:

- `||` for logical **or**
- `&&` for logical **and**

For example, to accept either lowercase or uppercase yes:

```c
if (c == 'y' || c == 'Y')
{
    printf("Agreed\n");
}
else if (c == 'n' || c == 'N')
{
    printf("Not agreed\n");
}
```

This improves design by avoiding duplicated `printf` statements and reducing the chance you update one branch but forget another.

---

## 2.11 Loops in C: `while`, `for`, and `do ... while`

Loops are how you make the computer do something repeatedly without copy/pasting the same line many times.

### 2.11.1 `while` loops

A `while` loop repeats as long as its condition remains true:

```c
int counter = 3;

while (counter > 0)
{
    printf("meow\n");
    counter--;
}
```

This pattern has three key parts:

1. Initialize a variable (`counter = 3`)
2. Check a condition (`counter > 0`)
3. Update the variable (`counter--`) so the loop eventually stops

C supports several equivalent update styles:

```c
counter = counter - 1;
counter -= 1;
counter--;
```

Similarly, increments can be written as `counter++`.

### 2.11.2 `for` loops

A `for` loop packages initialization, condition, and update into one line:

```c
for (int i = 0; i < 3; i++)
{
    printf("meow\n");
}
```

You can read this as:

- Start `i` at 0.
- While `i` is less than 3, do the loop body.
- After each iteration, increase `i` by 1.

This is often the most common loop style when you know in advance how many times you want to repeat something.

### 2.11.3 Infinite loops

Sometimes you want a loop that never ends. One pattern is:

```c
while (true)
{
    printf("meow\n");
}
```

The idea is simple: if the condition is always true, the loop never exits. (In standard C, using `true` typically involves including `<stdbool.h>`, though some environments and libraries make it available automatically.)

### 2.11.4 `do ... while` loops (prompt at least once)

Sometimes you want to do something *at least once* before checking whether it should repeat. That is exactly what a `do ... while` loop expresses:

```c
int n;

do
{
    n = get_int("Size: ");
}
while (n < 1);
```

This structure is especially useful for input validation: it guarantees the user is prompted once, and then prompted again only if their input does not meet the constraint.

---

## 2.12 Abstraction with Functions: Creating Your Own Building Blocks

Scratch lets you create custom blocks (“My Blocks”). C lets you create your own **functions**, which serve the same purpose: they let you name a behavior and reuse it.

### 2.12.1 A simple function with no return value (`void`)

A function that only produces a side effect (like printing) and does not return a value is often declared with `void`:

```c
void meow(void)
{
    printf("meow\n");
}
```

- The first `void` means the function returns nothing.
- The `(void)` means the function takes no arguments.

Then you can call it from `main`:

```c
int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        meow();
    }
}
```

### 2.12.2 Function prototypes (so order doesn’t trap you)

C is read top-to-bottom. If you call `meow()` before the compiler has seen the definition of `meow`, you will get an error.

One solution is to define `meow` above `main`, but that pushes `main` downward, which is inconvenient because `main` is the entry point you typically want to find quickly.

A better solution is to write a **function prototype** above `main`:

```c
#include <stdio.h>

void meow(void);

int main(void)
{
    meow();
}

void meow(void)
{
    printf("meow\n");
}
```

A prototype is a promise to the compiler: “this function exists later, and it has this signature.”

### 2.12.3 Functions with parameters (inputs)

To generalize `meow` so that it can meow any number of times:

```c
void meow(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("meow\n");
    }
}
```

Then `main` becomes a high-level description:

```c
int main(void)
{
    meow(3);
}
```

This is abstraction in action: `main` can now express *what* should happen without being cluttered by *how* it happens.

---

## 2.13 Return Values and Scope: When Functions Compute Answers

So far, many examples have focused on side effects (printing to the screen). But functions can also compute a value and hand it back to the caller via a **return value**.

### 2.13.1 A simple calculator and formatted printing

Adding two integers:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x: ");
    int y = get_int("y: ");

    printf("%i\n", x + y);
}
```

Here `%i` tells `printf` to print an integer.

### 2.13.2 Writing an `add` function (and discovering scope)

A first attempt at an `add` function might incorrectly try to use variables from `main`:

```c
int add(void)
{
    return x + y;   // ERROR: x and y are not in scope here
}
```

This fails because of **scope**.

- **Scope** is the region of a program where a variable name is valid and accessible.
- In C, variables declared inside one set of curly braces `{ ... }` are generally not accessible outside those braces.

`x` and `y` exist inside `main`’s braces, not inside `add`’s braces. To fix this, you pass values as parameters:

```c
int add(int a, int b)
{
    return a + b;
}
```

Then call it like:

```c
int z = add(x, y);
printf("%i\n", z);
```

And, if you want, you can even avoid the extra variable and “nest” the call:

```c
printf("%i\n", add(x, y));
```

### 2.13.3 Why `main` is declared `int main(void)`

You have repeatedly seen:

```c
int main(void)
```

Even if your program does not explicitly return a value, the convention is that `main` returns an integer status code to the operating system:

- `0` typically means “success.”
- Nonzero values often indicate some kind of error.

This is one reason why you may sometimes see numeric “error codes” reported by software: they originate from return values used as signals.

---

## 2.14 Working with the Linux Command Line: Files and Folders as Commands

When you use `cs50.dev`, you are effectively working on your own Linux-based environment in the cloud (technically, a container). The terminal commands you type are commands executed in that environment.

Some foundational commands include:

- `ls` — list files in the current directory
- `cd` — change directory
- `mv` — move (also used to rename)
- `cp` — copy
- `rm` — remove (delete) files
- `mkdir` — create a directory
- `rmdir` — remove a directory (when empty)
- `clear` — clear the terminal screen

### 2.14.1 Renaming a file with `mv`

To rename `meow.c` to `woof.c`:

```text
mv meow.c woof.c
```

This is the CLI equivalent of right-click → rename in a GUI.

### 2.14.2 Deleting a file with `rm`

To delete a file:

```text
rm hello.c
```

Be careful: deletion is often difficult to undo. Many command-line tools assume that if you type a deletion command, you mean it.

### 2.14.3 `./program` and the meaning of `.`

In paths:

- `.` means “this directory.”
- `..` means “the parent directory.”

That is why you run your program with:

```text
./hello
```

You are explicitly saying: “run `hello` from here.”

### 2.14.4 Terminal productivity features: history and autocomplete

Two practical features you will naturally start using:

- The **up arrow** cycles through previous commands.
- **Tab completion** auto-completes filenames and commands when the prefix is unambiguous.

These do not change what you can do, but they dramatically reduce typing.

---

## 2.15 Building Patterns: Mario, Grids, and Nested Loops

CS50 often uses *Mario* as a playful setting for pattern-printing problems, because they force you to think precisely about rows, columns, and repetition.

### 2.15.1 Printing a row of question marks

A hardcoded approach:

```c
printf("????\n");
```

A loop-based approach prints one character repeatedly:

```c
for (int i = 0; i < 4; i++)
{
    printf("?");
}
printf("\n");
```

This illustrates a small but important detail: if you print a newline inside the loop, you get one character per line. If you want one row, print the newline *after* the loop.

### 2.15.2 Printing a 2D grid: nested loops

To print a 3×3 grid using `#` characters:

```c
for (int i = 0; i < 3; i++)
{
    for (int j = 0; j < 3; j++)
    {
        printf("#");
    }
    printf("\n");
}
```

The structure matches how screens are typically written in text:

- The outer loop iterates over **rows**.
- The inner loop iterates over **columns**.
- After each row, print a newline.

### 2.15.3 Avoiding “magic numbers” with a variable

If the size is used in multiple places, writing `3` repeatedly is fragile. A common improvement is to use a single variable:

```c
int n = 3;

for (int i = 0; i < n; i++)
{
    for (int j = 0; j < n; j++)
    {
        printf("#");
    }
    printf("\n");
}
```

### 2.15.4 Making the program dynamic with input (and validating it)

With CS50’s `get_int`, you can ask the user for the size:

```c
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;

    do
    {
        n = get_int("Size: ");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
```

The `do ... while` avoids duplicating the prompt, because it naturally expresses: “prompt once, and keep prompting while the input is invalid.”

---

## 2.16 Comments in C

C supports **comments**, which are notes for humans that the compiler ignores.

A common single-line comment begins with `//`:

```c
// prompt user for positive integer
```

Comments do not change what the program does, but they can clarify *why* the program is written the way it is, which matters when you return to your code later or share it with others.

(As a contrast: in Python, `#` starts a comment, but in C `#` is used for directives like `#include`.)

---

## 2.17 The Limits of Computers: Memory Is Finite

After learning how to write programs that seem to “do math,” it is crucial to confront a deeper reality: a computer has a finite amount of memory, so it cannot represent all numbers perfectly or count forever without consequences.

In practice, limitations often show up in two forms:

1. **Integer overflow** (counting too high with a fixed number of bits)
2. **Floating-point imprecision** (representing real numbers approximately)

---

## 2.18 Integer Overflow: When Counting Wraps Around

If you only have a fixed number of digits or bits, you can represent only a fixed range of numbers.

A vivid mental model is a fixed-width counter. If you can store only three digits, you can count:

- 000, 001, 002, …, 999

But then the next count would “wrap” because there is nowhere to store the carry.

Computers store integers with a fixed number of bits. A common size is **32 bits** for an `int` (by modern convention). With 32 bits:

- There are \(2^{32}\) possible bit patterns, roughly **4 billion**.

If the system uses only nonnegative values, the largest representable number is:

- **4,294,967,295**

If the system also represents negative values (as most do), then roughly half the patterns are used for negatives, leaving a maximum around **2 billion** for positive values.

When you exceed the maximum representable value, the number does not become “bigger than maximum.” Instead, it typically **wraps around**, producing a value that is suddenly small again (often 0 or a negative number). That phenomenon is **integer overflow**.

### 2.18.1 Larger integers: `long` and 64 bits

If 32-bit integers are not enough, many systems support 64-bit integers, commonly accessed in C as `long` (or related types depending on platform). With 64 bits, the range is astronomically larger—not merely doubled, but exponentially expanded.

CS50’s library even provides `get_long`, and `printf` can print long integers using `%li`.

---

## 2.19 Truncation: Integer Division Loses the Fraction

Consider dividing:

- \(1 \div 3 = 0.3333...\)

If you do integer division in C, the result is truncated (the fractional part is discarded). For example, if `x` and `y` are integers:

```c
int x = 1;
int y = 3;
printf("%i\n", x / y);
```

This prints:

- `0`

This is not rounding; it is **truncation**. Everything after the decimal point is thrown away because the computation is being performed in integer arithmetic.

---

## 2.20 Floating-Point Values: `float`, `double`, and Imprecision

To preserve fractional values, you use floating-point types:

- `float` (often 32 bits)
- `double` (often 64 bits, more precision)

A first instinct might be to simply print with `%f`, but format codes must match types. If you tell `printf` to expect a floating-point value while passing it an `int`, the compiler may warn you or error.

A common approach is to **cast** integers to floating-point before division.

### 2.20.1 Casting to avoid truncation

```c
int x = get_int("x: ");
int y = get_int("y: ");

double z = (double) x / (double) y;
printf("%f\n", z);
```

- `(double) x` means “treat `x` as a double for this expression.”
- Now the division is performed in floating-point arithmetic, so the fractional part is preserved.

### 2.20.2 Controlling decimal places in `printf`

`printf` supports formatting precision. For example:

- `%.5f` prints 5 digits after the decimal point.

```c
printf("%.5f\n", z);
```

### 2.20.3 Floating-point imprecision: why you don’t get infinite 3’s

Even with `double`, you may see:

- `0.33333333333333331483`

instead of a perfect infinite repetition of `3`.

This is **floating-point imprecision**. The computer is not “bad at math”; it is representing a real number using a finite number of bits, and most real numbers cannot be represented exactly in binary floating-point form. The stored value is the closest representable approximation, and printing many digits reveals that approximation.

---

## 2.21 Real-World Consequences of Representation Limits

These limitations are not merely academic. They have produced major historical and engineering problems.

### 2.21.1 Y2K: when two digits weren’t enough

Many older systems stored years using two digits (e.g., `99` for 1999). Memory used to be expensive, and saving bytes mattered. But when the year rolled over to 2000, a system storing only two digits could interpret `00` as 1900 rather than 2000, causing date comparisons and time-based logic to fail.

### 2.21.2 The 2038 Problem: when 32-bit time overflows

Many systems track time as the number of seconds since an “epoch,” commonly:

- January 1, 1970

If time is stored in a 32-bit integer, eventually the counter overflows, and the time representation wraps around, potentially making systems think it is the early 1900s again. This is predicted to occur in **2038** for many 32-bit time representations.

A common mitigation is to switch to **64-bit** time counters, which pushes the overflow so far into the future (on the order of hundreds of millions of years) that it is no longer a practical concern—though it is still, fundamentally, finite.

### 2.21.3 Bugs in games: Pac-Man and Donkey Kong

Representation limits also surfaced in classic games:

- **Pac-Man**: reaching a sufficiently high level (notably around level 256) could trigger overflow-like behavior that corrupted the game state and display.
- **Donkey Kong**: an internal time calculation could wrap in a way that left only a few seconds to complete a level, making progress impossible.

The underlying lesson is the same: if you store a value in a type that cannot represent the range you eventually reach, behavior becomes incorrect in surprising ways.

### 2.21.4 Boeing 787: overflow and the “turn it off and on” fix

A particularly striking real-world example involved the Boeing 787. Documentation described a scenario in which, after a certain amount of continuous power-on time (248 days), a counter could overflow, leading systems to enter failsafe modes simultaneously—causing loss of power.

The short-term workaround echoed a familiar computing trope:

- power cycle the system (turn it off and back on)

Restarting resets memory, and thus resets counters. Longer-term, the solution required a software update to prevent the overflow condition.

---

## 2.22 Where This Chapter Leaves You

By the end of week 1, you have taken the core ideas from Scratch and expressed them in C:

- You can write **source code** and understand that it must be compiled into **machine code**.
- You can use a development environment (`cs50.dev`) that combines a code editor and a terminal.
- You can print output with **`printf`**, including special characters via **escape sequences** like `\n`.
- You can use **libraries** via **header files** (`stdio.h`, `cs50.h`) and consult documentation via **manual pages**.
- You can store data in **variables** with explicit **types** (`int`, `string`, `char`, `float`, `double`).
- You can make decisions with **conditionals**, compare values with `==` (not `=`), and combine logic with `||` and `&&`.
- You can repeat actions with **loops** (`while`, `for`, `do ... while`) and build two-dimensional patterns using **nested loops**.
- You can write your own **functions**, use **prototypes**, pass **arguments**, and return values—while respecting **scope**.
- You understand that computers have **finite memory**, leading to **integer overflow**, **truncation**, and **floating-point imprecision**, and that these constraints have caused real failures in the world.

In the next stage of the course, these foundations become the basis for more complex programs, deeper reasoning about memory, and a clearer understanding of what “dangerous” and “powerful” mean when working close to the machine.