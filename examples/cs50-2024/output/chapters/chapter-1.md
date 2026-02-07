# CS50-2024

## Chapter 1: Week 0 — Scratch, Computational Thinking, and the Foundations of Information

CS50 is Harvard University’s introduction to the intellectual enterprises of computer science and the art of programming, and it begins with a deceptively simple promise: you will learn how to solve problems, and you will learn how to express those solutions in a form that a computer can execute. In the first week—often called *week 0*—the course deliberately postpones the syntactic details of traditional programming languages and instead focuses on the underlying ideas that make programming possible at all: how information is represented, how algorithms transform inputs into outputs, and how to reason about correctness and efficiency.

This opening week also sets expectations for what learning computer science tends to feel like in practice. A famous analogy from MIT describes education as “drinking from a fire hose,” and that sensation—lots of new terms, many unfamiliar concepts arriving quickly—is normal in an introductory course. The goal is not to absorb everything perfectly on first exposure, but to build comfort over time through repeated practice. A helpful mindset, then, is to get comfortable feeling uncomfortable, especially early on, because “new” is the point of an introduction.

### A Course About Learning to Program (Not Just Learning a Language)

Historically, students might have summarized an introductory course by saying, “I learned C.” CS50 still teaches C, but it also introduces multiple languages and tools because modern computing problems live in many domains:

- **C**, a lower-level language that reveals how computers manage memory and data in a direct way.
- **Python**, a modern language used widely for data science, scripting, and web development.
- **SQL**, a language for working with databases and structured data.
- **HTML, CSS, and JavaScript**, which together underpin most web applications and many mobile experiences.

The deeper goal is not that you “know C” or “know Python” in isolation, but that you learn the transferable concepts that allow you to teach yourself new languages and tools later. In other words, CS50 aims to teach you *how to program*, which is largely the same as teaching you how to express problem-solving ideas precisely.

### Community and Support Structures

CS50 is also structured around community and support. Many students begin with no prior background in computer science, and the course is designed with different “tracks” in problem sets and sections so that students can start from where they are. The course emphasizes progress relative to yourself: what matters is not where you end up compared to classmates, but how far you travel from your own starting point.

Along the way, CS50 culture is punctuated by social and academic events such as CS50 lunches, Puzzle Day (logic puzzles solved in teams), a Hackathon (an overnight build session for final projects), and the CS50 Fair (a showcase of final projects). The course is building toward a capstone final project that you design yourself, with the intention that when you finish CS50, you do not “need CS50” to keep building.

---

## 1.1 What Is Computer Science?

At its core, **computer science is the study of information** and the processes by which information can be represented, transformed, stored, and communicated. Since information is central, computer science naturally becomes about **problem solving**: taking some *input* (the given data or situation) and producing some *output* (the desired result).

A simple model captures this:

- **Input** → **Algorithm** → **Output**

An **algorithm** is a step-by-step procedure for solving a problem. It can be written in English, described verbally, or illustrated physically. When an algorithm is expressed in a form that a computer can execute, we call that expression **code** (a program). Week 0 is largely about understanding what algorithms and code must operate on: representations of information.

---

## 1.2 Representing Information: From Fingers to Bits

Computers ultimately operate using physical phenomena—most commonly electricity. That fact constrains how we represent information inside a machine, but it also provides an elegant foundation.

### Unary: Counting With One Symbol

The simplest representation system is **unary**, where each unit is represented by a single mark (or finger). Counting on fingers is a form of unary notation: each raised finger corresponds to “one more.”

Unary is straightforward but limited. If you use a single hand and treat each finger as either down or up, you might say you can count to 5. However, if you consider not “how many” fingers are up but *which* fingers are up (each finger being a choice between two states), then five fingers yield:

- \(2 \times 2 \times 2 \times 2 \times 2 = 2^5 = 32\) possible configurations.

If one configuration is used for 0, the highest value represented is 31. This observation begins to resemble how computers work: information can be represented by collections of components that are each in one of two possible states.

### Binary: Two Symbols, Many Possibilities

**Binary** is a base-2 representation system that uses only two symbols. By convention, computers use:

- `0` and `1`

These map conveniently to electrical states:

- **0**: no electricity / off
- **1**: electricity present / on

A single `0` or `1` is called a **bit** (short for **binary digit**). Modern computers contain enormous numbers of tiny electrical switches called **transistors**, and each transistor can be treated as storing a bit.

### Place Values in Base 10 vs Base 2

To understand binary, it helps to recall how decimal (base 10) works. Consider the decimal number:

`123`

Its meaning depends on *place values*:

- \(1 \times 10^2\) (hundreds place)
- \(2 \times 10^1\) (tens place)
- \(3 \times 10^0\) (ones place)

So:

\[
123 = 1\cdot 100 + 2\cdot 10 + 3\cdot 1
\]

Binary works the same way, but with powers of 2 instead of powers of 10. With three binary digits, the place values are:

- \(2^2 = 4\)
- \(2^1 = 2\)
- \(2^0 = 1\)

So the pattern `101` in binary means:

\[
1\cdot 4 + 0\cdot 2 + 1\cdot 1 = 5
\]

Using physical metaphors like light bulbs (each bulb off/on representing 0/1) makes it clear that binary counting is not arbitrary; it is systematic. With three bits, you can represent 0 through 7, and to represent 8 you need a fourth bit (`1000`).

---

## 1.3 Bits and Bytes

While a single bit is the fundamental unit, it is often too small to be convenient. A common larger unit is the **byte**, defined as:

- **1 byte = 8 bits**

With 8 bits, you can represent:

- \(2^8 = 256\) total patterns

If the smallest pattern is used to represent 0, then the largest number representable with one byte is:

- **255**

This is why you often see the range **0–255** in computing systems: it is the natural range of values representable by one byte.

---

## 1.4 Representing Text: ASCII and Unicode

Numbers are only the beginning. Computers must also represent letters, punctuation, and symbols.

### ASCII: Mapping Letters to Numbers

One straightforward approach is to **assign each character a number**. This is the idea behind **ASCII**: the **American Standard Code for Information Interchange**.

In ASCII, the capital letter:

- `A` is represented by the number **65**

So, when a computer stores the binary representation of 65 in memory, it can interpret that pattern as the character `A`—provided it is using ASCII (or a compatible encoding) and the context says “treat this as text.”

ASCII is sufficient for English letters (upper and lower case), digits, punctuation, and a handful of control characters. But ASCII’s common 8-bit storage (256 possible values) is not sufficient for the world’s writing systems.

### “Hi!” as Numbers Under the Hood

A message like:

- `Hi!`

can be stored as ASCII values:

- `H` = 72
- `I` = 73
- `!` = 33

In binary, each of these is stored as a pattern of 0s and 1s, but humans rarely read those bits directly. The essential idea is that **text is stored as numbers**, and those numbers are stored as bits.

### Unicode: A Global Standard for Characters (Including Emoji)

To represent accented characters, non-Latin alphabets, and languages with thousands of symbols, modern systems use **Unicode**, which is best thought of as a superset of ASCII with far more possible characters. Unicode may use:

- 16 bits, 24 bits, or 32 bits per character (often thought of as 2, 3, or 4 bytes)

With 32 bits, a system can represent roughly:

- \(2^{32}\) ≈ **4 billion** possible code points

Unicode’s mission is broader than convenience: it aims to represent and preserve human languages digitally, past, present, and future, while also enabling symbolic communication such as emoji.

#### Emoji and Platform Differences

Emoji are “characters” in the Unicode sense, but their *appearance* can differ by platform. Apple, Google, Microsoft, Meta, and others may draw the same Unicode character differently, much like different fonts render the same letters differently. For example, the emoji officially named **“face with tears of joy”** is widely popular, but the exact face design varies across devices.

#### Code Points and Hexadecimal Notation

Unicode characters are often referred to using a notation like `U+....`, where `U+` is simply a convention meaning “here comes a Unicode code point.” The number after it is frequently written in **hexadecimal** (base 16), which compactly represents large binary values. Hexadecimal uses digits `0–9` and letters `A–F`. The important point in week 0 is not mastering hexadecimal, but recognizing that it is another representation for the same underlying bits.

#### Skin Tones and Combinations: More Bits, More Meaning

Unicode also supports modifiers, such as skin tone variations, using additional code points that adjust how a base character is displayed. Some emoji are also composites formed by joining multiple characters, sometimes using special characters like **zero-width joiners** to indicate that separate symbols should be rendered as one combined glyph (for example, certain family or relationship emoji).

---

## 1.5 Context Matters: The Same Bits Can Mean Different Things

A central lesson emerges as soon as we represent text and colors:

> The same pattern of bits can represent different information depending on context.

The ASCII numbers `72 73 33` can mean the text `Hi!` in a messaging context, but if those same values are interpreted as color components, they can represent a shade of yellowish color when treated as **RGB** (red/green/blue) intensities.

In practice:

- A text editor interprets bits as characters.
- A calculator interprets bits as numbers.
- An image editor interprets bits as colors and pixels.

As you begin programming in later weeks, you will often need to tell the computer what *type* of data you intend a sequence of bits to represent, so that it interprets them correctly.

---

## 1.6 Representing Images and Color: RGB and Pixels

Most screens create color using **additive color mixing** with three components:

- **R**ed
- **G**reen
- **B**lue

A common representation uses **one byte per component**, so each color channel ranges from 0 to 255. A single dot on the screen is called a **pixel**, and a typical RGB pixel stores:

- 3 bytes = 24 bits total (one byte for red, one for green, one for blue)

This explains, at a high level, why images can be large files: if an image contains about one million pixels and uses three bytes per pixel, then it contains roughly three million bytes (about 3 MB) of color data, even before compression and other file-format details.

When you zoom into a digital image—such as an emoji—you can see the pixel grid, and each pixel corresponds to stored RGB values.

---

## 1.7 Representing Sound and Video

Computers do not “understand” music as humans do, but they can represent it numerically.

### Sound as Numbers Over Time

One approach to representing music is to encode attributes such as:

- **pitch** (which note)
- **duration** (how long the note lasts)
- **volume** (how loud it is)

More generally, digital audio often represents a sound wave by sampling its amplitude over time, producing sequences of numbers that can be stored as bits.

### Video as Many Images

A **video** can be represented as a sequence of still images (frames) displayed quickly, such as 30 frames per second (FPS). When frames are shown rapidly, human perception interprets the changing images as continuous motion.

---

## 1.8 Algorithms: Correctness and Efficiency

Once we can represent inputs and outputs, we can focus on the procedures that convert one into the other.

### A Phone Book Search as an Algorithm

Consider the problem: find a person’s name in a phone book.

A slow but correct algorithm is:

- start at page 1 and flip one page at a time until you find the name (or reach the end)

This is correct, but it can take many steps. Another algorithm flips two pages at a time, but that can miss a name if the target lies on a skipped page—unless you compensate by stepping back when you pass the relevant section.

A much faster strategy is **divide and conquer**, analogous to what searching tools do digitally:

1. open to the middle of the book
2. decide whether the target is earlier or later alphabetically
3. discard half the book
4. repeat on the remaining half

This algorithm is dramatically faster because each step halves the problem size. For a phone book with about 1,000 pages, you can halve roughly 10 times before you narrow to a single page.

### Measuring Efficiency With Growth

If you plot:

- problem size on the horizontal axis (how many pages)
- time on the vertical axis (how many steps)

then:

- flipping one page at a time grows linearly: more pages means proportionally more work
- halving the search space grows much more slowly, producing a curve associated with logarithmic growth (specifically log base 2 in this scenario)

Efficiency is not the same as correctness. A “one-step” algorithm that chooses a random page is fast but not reliably correct. In computer science, we care about both:

- **Correctness**: does it always produce the right answer?
- **Efficiency**: how does the required time (or space) grow as inputs get larger?

---

## 1.9 Pseudocode and Core Programming Building Blocks

Before writing code in a specific language, it helps to write **pseudocode**: a precise, human-readable description of an algorithm. Pseudocode has no single official format, but it is meant to be clear, structured, and unambiguous enough that someone else could implement it.

A pseudocode version of the phone book algorithm might look like:

```text
1. Pick up phone book
2. Open to middle of phone book
3. Look at page
4. If person is on page
5.     Call person
6. Else if person is earlier in book
7.     Open to middle of left half of book
8.     Go back to line 3
9. Else if person is later in book
10.    Open to middle of right half of book
11.    Go back to line 3
12. Else
13.    Quit
```

This example reveals several foundational building blocks that appear across almost all programming languages:

- **Functions**: actions or verbs (e.g., “Pick up,” “Open,” “Look,” “Call”).
- **Conditionals**: forks in the road (e.g., “If… else if… else…”).
- **Boolean expressions**: yes/no questions that guide conditionals (true/false).
- **Loops**: repeated behavior (e.g., “Go back to line 3”).

These ideas are more important than any one language’s punctuation or syntax because they transfer directly to C, Python, JavaScript, and beyond.

---

## 1.10 Artificial Intelligence, Large Language Models, and the CS50 Duck

Artificial intelligence is a prominent theme in modern computing, and it is relevant to CS50 both intellectually and practically. A simple “chatbot” could be implemented with many explicit conditionals:

```text
If the student says "hello"
    say "hello"
Else if the student says "goodbye"
    say "goodbye"
Else if the student asks "how are you"
    say "well"
...
```

But this approach does not scale: it becomes impossible to anticipate every question (for example, every possible question about binary representation). Modern **large language models (LLMs)** instead ingest large amounts of human language (for example, text from the web) and infer statistical patterns that allow them to generate plausible responses.

These systems can be powerful, but they can also make mistakes (“hallucinate”), and their outputs can vary due to randomness and the desire for non-repetitive responses.

### Course Guardrails

In CS50’s approach for this year, the course emphasizes learning and problem solving rather than outsourcing entire solutions to general-purpose AI systems. For the course’s purposes, CS50 provides its own AI-based tool—a chatbot with the personality of a CS50 teaching assistant—available at **cs50.ai**, themed as a **CS50 duck**. The intent is closer to a patient tutor that helps you get unstuck without simply doing the work for you.

This connects to a long-standing programming tradition known as “rubber duck debugging,” in which explaining your code aloud—often to an inanimate duck—helps you notice your own errors and clarify your thinking.

---

## 1.11 From Bits to Programs: Why Scratch Comes First

If computers “speak” in bits, then any program—no matter how sophisticated—must ultimately be represented as 0s and 1s. For example, even “Hello, world” can be encoded in binary, but humans do not write software at that level. We write software using programming languages that provide abstractions—human-friendly representations that tools translate into machine-level instructions.

CS50 will soon introduce C, where a classic first program looks like:

```c
printf("hello, world\n");
```

Even if you can guess what it does, C also includes syntax that can feel like noise at first: semicolons, braces, `#include`, and other symbols that matter to the compiler but are not the core intellectual ideas.

To focus on ideas rather than punctuation, CS50 begins with **Scratch**, a graphical programming language from MIT. Scratch lets you build algorithms by snapping together blocks, which makes functions, loops, and conditionals tangible and visible.

---

## 1.12 Scratch as a Visual Programming Language

Scratch programs are built by combining **blocks** (puzzle-piece shapes) that represent programming constructs. Blocks are grouped by category and color, such as:

- **Motion** (moving sprites)
- **Looks** (speech bubbles, costumes)
- **Sound**
- **Events** (such as “when green flag clicked”)
- **Control** (loops and conditionals)
- **Sensing**
- **Operators**
- **Variables**
- **My Blocks** (custom blocks you define)
- **Extensions** (additional capabilities like text-to-speech or video sensing)

Scratch projects typically include one or more **sprites**, which are characters or objects on a stage. The stage uses an (x, y) coordinate system:

- the center is (0, 0)
- y increases upward (top is about 180)
- y decreases downward (bottom is about -180)
- x decreases to the left (about -240)
- x increases to the right (about 240)

This coordinate system makes it possible to describe movement precisely, though many Scratch blocks allow you to work without manual coordinate math.

---

## 1.13 A First Scratch Program: “Hello, world”

A minimal Scratch program mirrors the traditional first program in text-based languages:

- **Event**: *when green flag clicked*
- **Action**: *say “hello, world”*

In Scratch terms, the “say” block is a **function-like** action: it performs an operation (displaying a speech bubble). The text inside the block is an **argument** (also called a **parameter**): input that customizes the block’s behavior.

This already matches the input–algorithm–output model:

- input: the string `"hello, world"`
- algorithm/function: the “say” operation
- output: a speech bubble appearing on the screen

---

## 1.14 Input and Return Values: Asking a Question

Scratch can also request input from the user with an “ask … and wait” block. Conceptually, this block:

1. displays a prompt
2. waits for user input
3. produces a value (the input) that other blocks can use

That produced value is a **return value**, accessible via an “answer” block.

To greet a user by name, a program can:

- ask “What’s your name?”
- then say “hello, ” combined with the answer

A subtle bug can occur if you try to say “hello” and then immediately say the name in a separate “say” block: the computer may execute the second so quickly that the first is never visible. One fix is to use “say … for 2 seconds,” but a cleaner solution is to **compose** the output into a single string using the “join” operator block:

- join `"hello, "` with `answer`
- feed the result into a single “say” block

This illustrates an important programming habit: the output of one operation can become the input of another, and composing smaller pieces carefully often yields clearer behavior.

---

## 1.15 Extensions: Text-to-Speech as Another Output Modality

Scratch can be extended with capabilities such as **text-to-speech**. Instead of “say,” a program can “speak” the joined greeting aloud. The same underlying structure remains:

- gather input
- combine it with other text
- produce output

Only the output modality changes—from a speech bubble to synthesized audio. This reinforces the idea that programming is often about connecting inputs to outputs through a sequence of transformations, regardless of whether those outputs are visual, textual, or audible.

---

## 1.16 Loops, Repetition, and Better Design

If a sprite plays a “meow” sound three times, you could duplicate the “play sound meow” block three times. That works, but it is not a robust design because it repeats code. Repetition becomes error-prone when you later need to change behavior: if you meow ten times and want to adjust the wait time between meows, you may forget to update one copy.

A better approach is to use a **loop**, such as “repeat 3,” containing:

- play sound meow
- wait 1 second

This is the same motivation behind efficient algorithms: you want a solution that scales cleanly and minimizes the chance of mistakes.

---

## 1.17 Abstraction and Custom Blocks (“My Blocks”)

Scratch allows you to define your own blocks under **My Blocks**, which are essentially custom functions. If “meow” is a meaningful action in your program, you can encapsulate its implementation into a single block named “meow,” even if internally it plays a sound and waits.

This is **abstraction**: hiding lower-level implementation details so you can think at a higher level. After defining “meow,” your main script can become simpler and easier to read.

You can generalize further by giving your block a parameter, such as:

- `meow (n) times`

Internally, the block can include a loop that repeats the sound `n` times. This transforms a specific behavior into a reusable component, which is one of the central practices of programming in any language.

---

## 1.18 Conditionals and Event-Driven Interaction

Scratch is naturally **event-driven**, meaning programs often respond to events such as:

- clicking the green flag
- pressing a key
- touching a sprite with the mouse pointer
- detecting motion through a camera

A conditional example is making a cat meow when “petted” (when the mouse pointer touches it). A first attempt might check the condition once, immediately after the green flag is clicked, but that is insufficient because interaction can happen later. The fix is to place the conditional inside a loop such as “forever,” so the program keeps checking:

- forever:
  - if touching mouse pointer:
    - play meow

This illustrates a recurring debugging lesson: when a program “does nothing,” it is often doing exactly what you asked—just not what you intended. The difference is resolved by being more explicit about timing and repetition.

---

## 1.19 Sensing the Physical World: Video Motion

With Scratch extensions such as **video sensing**, a program can react to motion detected by a camera. For instance:

- when video motion > threshold:
  - play meow

Changing the threshold changes sensitivity. Too low a threshold can cause constant triggering; too high may cause no response. This kind of tuning reflects a broader reality in computing: when programs interface with noisy real-world inputs (like camera data), careful design choices are required to produce stable behavior.

---

## 1.20 From Blocks to Games: Sprites, Variables, and Incremental Development

Scratch’s building blocks are sufficient to create real interactive games. Examples demonstrated in week 0 include:

- a camera-based “whac-a-mole” style game controlled by head movement
- a multi-sprite game involving moving obstacles (Harvard vs Yale vs MIT) with increasing difficulty
- a simple maze-like setup where keyboard input moves a sprite and “walls” block movement

These programs typically involve:

- **multiple sprites**, each with their own scripts
- **variables**, which store values such as score or time remaining
- **randomness**, which keeps gameplay from being identical every time
- **collision detection**, expressed as Boolean expressions like “touching [sprite]?”

### Building Big Programs as Many Small Versions: “Oscartime”

A particularly instructive example is a Scratch game developed incrementally, where trash falls from the sky and must be dragged into a trash can. The development process is itself a lesson in problem solving:

1. **Version 1**: build the scene (the stage and major visual elements).
2. **Version 2**: make the trash draggable and animate the trash can lid by switching costumes depending on whether the mouse pointer is touching the can.
3. **Version 3**: make trash fall by repeatedly decreasing its y-coordinate.
4. **Version 4**: detect when trash touches the can and “teleport” it back to the top at a random x-position.
5. **Later versions**: add scoring, timing, sound, and richer interactions.

This approach—reducing a grand idea into achievable steps—is how real software is built. You rarely implement “version 20” directly. Instead, you build a correct version 1, then a correct version 2, and so on, steadily increasing complexity while maintaining control over correctness.

---

## 1.21 Where This Chapter Leaves You

By the end of week 0’s material, you have the conceptual foundation for the rest of CS50:

- **Information** can be represented with bits.
- **Numbers**, **text**, **colors**, **images**, **audio**, and **video** are all encodings built on top of those bits.
- **Algorithms** are step-by-step procedures that transform inputs into outputs.
- Good solutions require both **correctness** and **efficiency**.
- Programming languages differ in syntax, but most share the same fundamental building blocks:
  - functions
  - conditionals
  - Boolean expressions
  - loops
  - variables
  - abstraction

Scratch serves as the first medium for these ideas because it makes program structure visible. In the next chapter, these same concepts will reappear in a text-based language (C), where you will begin to type programs rather than assemble them from blocks. The intellectual work, however, remains the same: representing information precisely and designing algorithms that reliably and efficiently solve problems.