# Chapter 7: Week 6 — Python: From Low-Level Control to High-Level Abstraction

By week 5, you had learned to treat memory as something you can design with, using pointers, `struct`, and dynamic allocation to build your own data structures. In week 6, the course makes a deliberate shift in perspective: instead of asking you to implement everything “from scratch” in C, we introduce **Python**, a more modern, higher-level language that provides many of the same capabilities through built-in abstractions.

This shift is not a retreat from what you learned in C. Rather, it is a payoff: once you understand what is happening “under the hood,” you are in a much better position to appreciate what higher-level languages are doing for you, what trade-offs they introduce, and how to use them effectively.

---

## 7.1 From C to Python: The Same Problems, Less Machinery

The most immediate difference you notice in Python is that many of the syntactic requirements of C simply disappear. Consider the simplest program you wrote at the start of the course:

### 7.1.1 “Hello, world” in C vs. Python

In C, printing text required several pieces of structure:

- including a library (`stdio.h`)
- defining `main`
- using `printf`
- ending lines with semicolons
- explicitly printing `\n` if you wanted a newline

```c
#include <stdio.h>

int main(void)
{
    printf("hello, world\n");
}
```

In Python, the same output is:

```py
print("hello, world")
```

Even in this tiny example, Python is already doing several things for you:

- You do not need to `#include` a standard I/O library for `print` to work.
- You do not need to define `main`.
- You do not need semicolons.
- You get a newline automatically after `print(...)`.

Python also allows either double quotes (`"..."`) or single quotes (`'...'`) for strings, as long as you are consistent. Many programmers prefer double quotes so that apostrophes inside a string are less likely to require escaping.

---

## 7.2 Compilation vs. Interpretation

In C, your workflow typically looked like this:

1. compile (often via `make`, which calls a compiler like `clang`)
2. run the compiled program (e.g., `./hello`)

Python removes the explicit compile step.

### 7.2.1 The Python interpreter

Python is typically run through a program called `python`, which is an **interpreter**. An interpreter reads your source code and executes it directly, top to bottom, left to right, without you manually compiling it into a separate executable first.

Python programs are conventionally stored in files ending with:

- `.py`

and run like:

```bash
python hello.py
```

This does not mean there is no translation happening at all (Python does compile internally to bytecode), but the key practical point remains: you do not explicitly compile and link the program each time you change it.

---

## 7.3 Libraries in Python: `import` Instead of `#include`

C uses header files (`.h`) and preprocessing directives like:

```c
#include <stdio.h>
```

Python uses **imports**.

### 7.3.1 Importing an entire module

You can import a whole module (a library) like this:

```py
import cs50
```

and then refer to functions inside it using dot notation:

```py
x = cs50.get_int("x: ")
```

This style is useful when you want to avoid name conflicts (for example, if you wrote your own `get_int` function).

### 7.3.2 Importing specific functions

If you only want a specific function, you can import it directly:

```py
from cs50 import get_int
```

and then call it without a prefix:

```py
x = get_int("x: ")
```

This “fine-grained” importing can also be more efficient conceptually: you are being explicit about what you need.

---

## 7.4 Variables and Types: Fewer Declarations, Same Concepts

Python still has familiar types like integers and strings, but it does not require you to declare a variable’s type in advance.

### 7.4.1 Assignment (still not equality)

Just like in C, the equals sign assigns right-to-left:

```py
counter = 0
```

Python also supports:

```py
counter = counter + 1
counter += 1
```

but **Python does not have** `++` or `--`. The designers intentionally omitted them, expecting `+= 1` and `-= 1` to be sufficient and clearer.

### 7.4.2 Core built-in types you will use immediately

Python includes:

- `bool` (`True` / `False` — note the capitalization)
- `int`
- `float`
- `str` (Python’s name for string)

Some C types disappear from view (like `long` and `double`) because Python tries to simplify the numeric model for you. For integers in particular, Python’s `int` is not limited to a fixed number of bits in the same way C’s `int` typically is.

---

## 7.5 Input in Python: `input()` and Conversion with `int(...)`

Python has a built-in function:

```py
input("Prompt: ")
```

It always returns a **string** (`str`), because everything typed on a keyboard is fundamentally text.

### 7.5.1 A greeting program

In Python, you can write a greeting program using `input()`:

```py
answer = input("What's your name? ")
print(f"hello, {answer}")
```

This uses an **f-string** (format string), discussed more below.

### 7.5.2 Why `1 + 2` can become `"12"`

If you do:

```py
x = input("x: ")
y = input("y: ")
print(x + y)
```

and type `1` then `2`, you will see:

- `12`

because `x` and `y` are strings, and `+` concatenates strings.

To add numerically, you must convert:

```py
x = int(input("x: "))
y = int(input("y: "))
print(x + y)
```

Here, `int(...)` is not “casting” in the C sense; it is conversion using a function.

### 7.5.3 What happens if conversion fails?

If the user types something like `cat`:

```py
x = int(input("x: "))
```

Python will raise a runtime error (an exception), such as a `ValueError`, because `"cat"` is not a valid integer literal.

This is one reason the CS50 Python library’s `get_int()` can still be useful early on: it repeatedly prompts until the user provides an integer.

---

## 7.6 Printing and Formatting Output

Python’s `print()` is more flexible than C’s `printf()`. It can print strings, integers, floats, and more without format codes.

### 7.6.1 Concatenation with `+`

```py
name = input("Name: ")
print("hello, " + name)
```

This works, but it requires you to manage spacing carefully.

### 7.6.2 Multiple arguments to `print()`

`print()` can take multiple arguments separated by commas:

```py
name = input("Name: ")
print("hello,", name)
```

By default, Python inserts a single space between arguments.

### 7.6.3 f-strings (format strings)

An f-string is a string prefixed with `f`, which allows expressions inside `{...}`:

```py
name = input("Name: ")
print(f"hello, {name}")
```

If you forget the `f`, Python will print the braces literally instead of interpolating the variable.

### 7.6.4 Controlling the newline: named parameters (e.g., `end=`)

By default, `print()` ends with a newline. You can override that with the **named parameter** `end`:

```py
print("?", end="")
print("?", end="")
print("?")
```

or more commonly:

```py
for _ in range(4):
    print("?", end="")
print()
```

Here:

- `end=""` suppresses the newline each iteration
- the final `print()` (with no arguments) prints just a newline

Named parameters like `end=` are different from the positional arguments you used in C: they explicitly name which parameter you are setting.

---

## 7.7 Conditionals in Python: Colons and Indentation

Python removes curly braces and instead uses:

- a colon (`:`) to begin a block
- indentation (typically 4 spaces) to define the block

```py
if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x is equal to y")
```

A key stylistic and technical difference from C is that indentation is not just for human readability in Python. It is part of the language’s syntax. Poor indentation can break your program.

Python also uses the keyword `elif` (not `else if`).

---

## 7.8 String Comparison: More Intuitive Than C

In C, comparing strings with `==` compares pointers (addresses), not characters. That is why two identical typed strings could still compare as “different.”

In Python, strings are higher-level objects, and `==` compares their contents:

```py
s = input("s: ")
t = input("t: ")

if s == t:
    print("Same")
else:
    print("Different")
```

Typing `cat` and `cat` yields `Same`, as you would naturally expect.

---

## 7.9 Methods and Object-Oriented Ideas: `s.lower()` Instead of `tolower(s)`

Python embraces **object-oriented programming (OOP)**. One practical consequence is that data types often come with built-in functionality.

A **method** is a function associated with an object. For strings (`str`), methods include:

- `.lower()`
- `.upper()`

Instead of writing something like `tolower(s)` (and having to apply it character-by-character), you write:

```py
s = input("Do you agree? ")
s = s.lower()
```

You can also chain calls:

```py
s = input("Do you agree? ").lower()
```

### 7.9.1 Improving “agree” with normalization and membership testing

A direct translation of a yes/no check might be:

```py
s = input("Do you agree? ")

if s == "Y" or s == "y":
    print("Agreed")
elif s == "N" or s == "n":
    print("Not agreed")
```

This fails for reasonable inputs like `yes`, `YES`, or `no`.

A more robust approach:

1. convert the input to lowercase
2. check membership in a collection of allowed values

```py
s = input("Do you agree? ").lower()

if s in ["y", "yes"]:
    print("Agreed")
elif s in ["n", "no"]:
    print("Not agreed")
```

Here, the keyword `in` checks whether a value is a member of a list.

---

## 7.10 Loops in Python: `while`, `for`, and `range()`

Python supports loops similar in spirit to C, but with simpler syntax.

### 7.10.1 `while` loops

```py
i = 0
while i < 3:
    print("meow")
    i += 1
```

### 7.10.2 `for` loops and `range()`

A more Pythonic approach:

```py
for i in range(3):
    print("meow")
```

`range(3)` yields the sequence:

- `0, 1, 2`

### 7.10.3 The underscore convention: “I won’t use this variable”

If you do not actually use the loop variable, you can signal that with `_`:

```py
for _ in range(3):
    print("meow")
```

This has no special runtime meaning; it is a readability convention.

### 7.10.4 Infinite loops

In Python:

```py
while True:
    print("meow")
```

Note the capitalization: `True` and `False` are capitalized in Python.

---

## 7.11 Iterating Over Strings

In Python, strings are **iterable**, meaning you can loop over them character-by-character:

```py
before = input("Before: ")
print("After: ", end="")
for c in before:
    print(c.upper(), end="")
print()
```

This shows how `end=""` can be used to prevent `print()` from moving to a new line each time.

However, Python strings also support an `.upper()` method that applies to the whole string at once:

```py
before = input("Before: ")
after = before.upper()
print(f"After: {after}")
```

You can even place expressions directly inside an f-string:

```py
before = input("Before: ")
print(f"After: {before.upper()}")
```

This is convenient when the expression is short and still readable.

---

## 7.12 Defining Your Own Functions: `def`, `main`, and Order of Definitions

Python uses the keyword `def` to define a function:

```py
def meow():
    print("meow")
```

### 7.12.1 Why order matters

Python reads top to bottom. If you call a function before Python has seen its definition, you will get a runtime error such as:

- `NameError: name 'meow' is not defined`

This leads to a common convention: define a `main()` function, define helper functions beneath it, and then call `main()` at the bottom.

### 7.12.2 A conventional Python structure

```py
def main():
    for _ in range(3):
        meow()

def meow():
    print("meow")

main()
```

Unlike C, Python does not automatically call `main()`. If you define it, you must call it.

### 7.12.3 Parameters

You can make functions more flexible by adding parameters:

```py
def main():
    meow(3)

def meow(n):
    for _ in range(n):
        print("meow")

main()
```

---

## 7.13 Division, Precision, and Integer Overflow

Python changes the behavior of some arithmetic in ways that reduce common beginner mistakes, but not all numeric issues disappear.

### 7.13.1 Division: no integer truncation by default

In C, `1 / 3` with integers truncates to `0`.

In Python:

```py
x = int(input("x: "))
y = int(input("y: "))
z = x / y
print(z)
```

If `x = 1` and `y = 3`, `z` becomes approximately:

- `0.3333333333333333`

Python returns a float when needed.

### 7.13.2 Floating-point imprecision still exists

Python still uses floating-point representations, so precision issues remain. You can display many digits using formatting syntax in an f-string:

```py
x = int(input("x: "))
y = int(input("y: "))
z = x / y
print(f"{z:.50f}")
```

This prints 50 digits after the decimal, revealing the underlying approximation.

### 7.13.3 Integer overflow: not the same problem in Python

In C, integers are typically fixed-size, so they can overflow.

In Python, integers grow as needed: Python allocates more memory to store larger and larger integers. This removes the classic “wraparound” overflow behavior for `int` in typical modern Python implementations.

---

## 7.14 Exceptions: Handling Errors Without Special Return Values

In C, one of the main ways to signal errors is to return “special” values like `NULL` or `-1`. That approach can consume legitimate return values and forces programmers to check results constantly.

Python supports **exceptions**, which are “out-of-band” error signals. When something goes wrong, Python raises an exception such as:

- `ValueError`
- `NameError`

### 7.14.1 Catching a `ValueError` with `try` / `except`

If you attempt:

```py
x = int(input("x: "))
```

and the user types `cat`, Python raises a `ValueError`.

You can handle it:

```py
try:
    x = int(input("x: "))
except ValueError:
    print("Not an integer")
```

### 7.14.2 Implementing a robust `get_int()` with a loop

A CS50-style `get_int()` can be written by repeatedly trying until success:

```py
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass
```

Here:

- `while True` creates an intentional infinite loop
- `return` ends the function (and therefore stops the loop)
- `pass` does nothing, allowing the loop to try again silently

This demonstrates both exception handling and a common Python pattern: deliberately loop forever, then `break` or `return` once you have valid input.

---

## 7.15 Rewriting “Mario” Patterns in Python

Many of the looping patterns you wrote in C become smaller and clearer in Python.

### 7.15.1 A column of bricks

```py
for _ in range(3):
    print("#")
```

### 7.15.2 Prompting for a positive height (a Pythonic substitute for do-while)

Python has no `do ... while` loop. A common approach is:

```py
from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0:
        break

for _ in range(n):
    print("#")
```

This forces repeated prompting until `n` is positive.

### 7.15.3 A row of characters

Using `end=""`:

```py
for _ in range(4):
    print("?", end="")
print()
```

Or using string “multiplication”:

```py
print("?" * 4)
```

### 7.15.4 A 3×3 grid

Nested loops:

```py
for _ in range(3):
    for _ in range(3):
        print("#", end="")
    print()
```

Or using repetition for each row:

```py
for _ in range(3):
    print("#" * 3)
```

---

## 7.16 Lists: Dynamic Sequences (Like Arrays, But Managed for You)

Python’s **list** type is written with square brackets:

```py
scores = [72, 73, 33]
```

Python manages memory for lists automatically: they can grow and shrink without you calling `malloc` or `free`.

### 7.16.1 Averaging scores with `sum()` and `len()`

```py
scores = [72, 73, 33]
average = sum(scores) / len(scores)
print(f"Average: {average}")
```

In C, you would have needed to loop and sum manually. Python provides these building blocks directly.

### 7.16.2 Building a list by appending user input

```py
from cs50 import get_int

scores = []

for _ in range(3):
    score = get_int("Score: ")
    scores.append(score)

average = sum(scores) / len(scores)
print(f"Average: {average}")
```

`append()` is a list method that adds to the end of the list, handling resizing for you.

---

## 7.17 Looping, Searching, and a Python Quirk: `for ... else`

Python supports a construct that looks unusual at first: a `for` loop can have an `else` clause. The `else` runs only if the loop finishes **without** hitting `break`.

A linear search might be written like this:

```py
names = ["Carter", "David", "John Harvard"]
name = input("Name: ")

for n in names:
    if n == name:
        print("Found")
        break
else:
    print("Not found")
```

However, Python often lets you avoid writing the loop at all by using membership testing:

```py
names = ["Carter", "David", "John Harvard"]
name = input("Name: ")

if name in names:
    print("Found")
else:
    print("Not found")
```

Python performs the linear search for you.

---

## 7.18 Dictionaries (`dict`) and Sets (`set`): Hash Tables and Uniqueness Built In

In week 5, a dictionary (in the CS sense) was an ADT, often implemented using a hash table. In Python, dictionaries and sets are built into the language.

### 7.18.1 Sets: collections without duplicates

A **set** is a collection that automatically removes duplicates. Python uses sets in the spell-checker example because it is convenient to test membership quickly.

In Python, a global set can store all dictionary words:

```py
words = set()
```

Then checking membership becomes simple:

```py
def check(word):
    return word.lower() in words
```

### 7.18.2 Loading a dictionary file into a set

A Pythonic way to load all lines from a dictionary file:

```py
words = set()

def load(dictionary):
    with open(dictionary) as file:
        words.update(file.read().splitlines())
    return True
```

Key ideas here:

- `with open(...) as file` ensures the file is managed cleanly
- `file.read()` reads the whole file into a string
- `.splitlines()` turns it into a list of lines (words)
- `words.update(...)` inserts them into the set

Then:

```py
def size():
    return len(words)
```

And `unload()` is effectively unnecessary in Python for this program, because memory is managed automatically:

```py
def unload():
    return True
```

In contrast to C, Python hides `malloc`, `free`, pointers, and manual cleanup, which is a major reason programs can become dramatically shorter.

### 7.18.3 Dictionaries: key–value pairs (hash tables for free)

A Python dictionary associates keys with values.

One approach is a list of dictionaries (each person is a dictionary with a `"name"` and `"number"` key):

```py
people = [
    {"name": "Carter", "number": "+1-617-495-1000"},
    {"name": "David",  "number": "+1-617-495-1000"},
    {"name": "John",   "number": "+1-949-468-2750"},
]
```

You can then search through `people`:

```py
name = input("Name: ")

for person in people:
    if person["name"] == name:
        print(f"Found {person['number']}")
        break
else:
    print("Not found")
```

Notice the syntax:

- `person["name"]` indexes a dictionary using a string key
- it looks like array indexing, but the “index” is a key, not a number

If you only need a simple mapping from names to numbers, you can simplify further into one dictionary:

```py
people = {
    "Carter": "+1-617-495-1000",
    "David":  "+1-617-495-1000",
    "John":   "+1-949-468-2750",
}
```

Then lookup becomes very direct:

```py
name = input("Name: ")

if name in people:
    print(f"Found {people[name]}")
else:
    print("Not found")
```

This illustrates why dictionaries are sometimes called a “Swiss Army knife” data structure in practice: any time you want to associate one thing with another, a dictionary is a natural tool.

---

## 7.19 Command-Line Arguments in Python: `sys.argv`

In C, command-line arguments arrive via `argc` and `argv` in `main`.

In Python, they are available through the `sys` module.

### 7.19.1 Reading `argv`

```py
from sys import argv

if len(argv) == 2:
    print("hello,", argv[1])
else:
    print("hello, world")
```

Here:

- `argv[0]` is the script name (e.g., `greet.py`)
- `argv[1]` is the first command-line argument after the script name

When you run:

```bash
python greet.py David
```

the word `python` is not included in `argv`; the list begins at the script name.

### 7.19.2 Exiting with status codes: `sys.exit`

You can import `sys` and exit with specific status codes (as you did in C by returning from `main`):

```py
import sys

if len(sys.argv) != 2:
    print("Missing command-line argument")
    sys.exit(1)

print("hello,", sys.argv[1])
sys.exit(0)
```

---

## 7.20 Why Not Always Use Python? Trade-Offs: Speed, Memory, and Development Time

Python can make programs dramatically shorter, more readable, and faster to write, especially because it provides:

- powerful built-in data structures (`list`, `dict`, `set`)
- high-level I/O (`input`, `print`)
- a large ecosystem of libraries

But Python often comes with costs:

- It is frequently **slower** than C for the same algorithm, because the interpreter and runtime do more work.
- It can use **more memory**, because Python stores richer objects and manages memory for you with additional overhead.

The key trade-off is similar to the one you saw with data structures: Python often saves **human time** (developer effort) by spending **computer resources** (CPU time and RAM).

---

## 7.21 Python’s Ecosystem: Doing Powerful Things with Libraries

One of Python’s biggest strengths is the ecosystem of third-party libraries. Instead of implementing everything yourself, you can often “stand on the shoulders” of others.

### 7.21.1 Image processing with PIL (Python Imaging Library)

Using PIL, you can blur an image in only a few lines:

```py
from PIL import Image, ImageFilter

before = Image.open("bridge.bmp")
after = before.filter(ImageFilter.BoxBlur(10))
after.save("out.bmp")
```

Similarly, edge detection can be performed with a built-in filter:

```py
from PIL import Image, ImageFilter

before = Image.open("bridge.bmp")
after = before.filter(ImageFilter.FIND_EDGES)
after.save("out.bmp")
```

These examples mirror the kinds of computations you implemented manually in C by iterating over pixels, but they are now accessible through library abstractions.

### 7.21.2 Installing libraries with `pip`

Python commonly uses a tool called `pip` to install third-party packages, such as:

```bash
pip install face_recognition
```

With such a library, tasks like face detection and recognition can be performed with relatively little code compared to implementing computer vision yourself.

### 7.21.3 Fun (but real) libraries: `cowsay`

After installing:

```bash
pip install cowsay
```

you can write:

```py
import cowsay

name = input("What's your name? ")
cowsay.cow(f"Hello, {name}")
```

This demonstrates both Python’s ease of expression and the idea that importing a package can add entirely new capabilities to your programs quickly.

### 7.21.4 Generating QR codes with `qrcode`

After installing:

```bash
pip install qrcode
```

you can generate a QR code image:

```py
import qrcode

img = qrcode.make("https://youtu.be/xvFZjo5PgG0")
img.save("qr.png")
```

In just a few lines, your program produces an image file (`qr.png`) that encodes a URL—an example of how Python can connect code to real-world formats and tools with minimal friction.

---

## 7.22 Summary: What Changes in Week 6 (and What Doesn’t)

Week 6 introduces Python as a language that deliberately provides higher-level abstractions over the low-level mechanisms you used in C.

What changes:

- You run programs with an interpreter (`python`), not by manually compiling and running.
- Much C syntax disappears: headers, semicolons, curly braces, `main`, manual newlines.
- Indentation becomes part of program correctness.
- Many data structures are built in (`list`, `dict`, `set`) and dynamically managed.
- Strings behave more intuitively (e.g., `==` compares contents).
- Memory management is automatic: no `malloc`, no `free`.
- Exceptions provide a structured way to handle errors without special return values.
- A rich ecosystem of libraries makes advanced tasks (image filtering, face detection, QR generation) accessible quickly.

What does not change:

- The fundamental ideas of programming still apply: variables, conditionals, loops, functions, and abstractions.
- You still must think carefully about correctness, input validation, and edge cases.
- Trade-offs still exist, especially between performance and convenience.
- The skills you built in C remain valuable, because they explain what Python is doing behind the scenes and why those abstractions have costs.

Python makes many problems easier to express, but the course’s deeper goal remains the same: learning how to program in a way that transfers across languages, tools, and years.