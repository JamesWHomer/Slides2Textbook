# Chapter 8: Artificial Intelligence — From Decision Trees to Large Language Models

Artificial intelligence (AI) can feel like it “arrived” suddenly, because the tools that the public now uses—image generators, chatbots, and deepfakes—are unusually visible and unusually accessible. But the ideas beneath those tools connect back to foundational computer science themes you have already practiced: representing problems precisely, choosing algorithms, reasoning about efficiency, and using abstraction to manage complexity.

This chapter builds those ideas in a deliberate progression. We begin with the human-facing phenomenon—AI that can generate convincing images, video, and text—and then work backward toward the underlying mechanisms: decision trees, game-playing with minimax, the limits of brute-force search, and the shift toward machine learning, reinforcement learning, and neural networks. We end where today’s popular tools live: large language models (LLMs), transformers, attention, embeddings, and the practical realities of systems that can still “hallucinate.”

---

## 8.1 AI in Everyday Life (and Why It Suddenly Feels Everywhere)

AI is not only the newest generation of chatbots. It has been present for years in systems most people now take for granted:

- **Spam detection** in services like Gmail and Outlook has become so effective that many people rarely need to check their spam folder at all.
- **Handwriting recognition** has steadily improved as systems learn to adapt to many different writing styles.
- **Recommendation systems** (for movies, music, shopping, and more) often outperform any hand-written rule set, because no human can explicitly encode rules for the preferences of millions of people across millions of items.
- **Voice assistants** like Siri, Google Assistant, and Alexa rely on AI for speech recognition and natural-language understanding.

These are not “magic,” but they are systems that successfully detect patterns in data and make useful predictions. What has changed recently is that AI has become dramatically better at producing *human-like outputs*—especially images, video, and text—which makes it more emotionally compelling and, in some cases, more socially dangerous.

---

## 8.2 Generative AI and the New Problem of Believability

### 8.2.1 Images that no longer have obvious “tells”

In the early days of modern image generation, you could often spot obvious mistakes. A famous example was **hands**: generated images frequently produced the wrong number of fingers, unnatural joints, or inconsistent anatomy. Those details served as “tells” that revealed the image was synthetic.

But those tells are disappearing. AI-generated images can now look like plausible photographs, and sometimes even careful observers cannot reliably distinguish real images from generated ones. In demonstrations of side-by-side comparisons, a viewer may correctly identify one generated image, only to discover that a later pair of images are *both* generated.

The practical implication is that the burden of proof shifts. If “seeing is believing” becomes unreliable for images, it becomes harder to treat visual evidence as inherently trustworthy.

### 8.2.2 Deepfakes: when video becomes editable reality

Image generation is only part of the story. **Deepfakes** extend the same idea to video: a real person may perform motions and speak words, while software modifies the resulting footage so that it appears to be someone else. A convincing deepfake is not merely a filter; it is a synthesis of visual identity.

This matters beyond novelty, because disinformation becomes easier to create and harder to refute when it can be produced not only as text, but also as realistic images—and eventually as realistic video.

### 8.2.3 Text generation: the rise of ChatGPT

If image generators made AI visible, conversational text generators made AI *interactive*. Tools like **ChatGPT** create the feeling that you are talking with an assistant that can explain, summarize, rewrite, and answer questions in natural language. This interactivity has pushed AI into classrooms, workplaces, and daily routines.

One consequence is that education must decide not only what AI can do, but what students *should* do with it while learning.

---

## 8.3 AI in Education: Rubber Duck Debugging Becomes a “Duck Debugger”

### 8.3.1 Rubber duck debugging (the human version)

Within programming culture, there is a long-standing technique called **rubber duck debugging** (often just “rubber ducking”). The idea is simple: when your code is not working and you have no one nearby to ask, you explain your program out loud to an inanimate object—often, literally, a rubber duck.

The duck does not respond, but the act of turning vague thoughts into precise explanations often reveals the mistake. The debugging “assistant” is not the duck’s intelligence; it is your own reasoning becoming clearer as you articulate it.

### 8.3.2 From a quacking duck to an AI teaching assistant

CS50 historically provided a digital duck that would respond with a small number of “quacks.” Even that minimal interaction was sometimes enough to prompt students to realize what they had overlooked.

More recently, however, the duck has effectively “come to life” as an AI-based teaching assistant—often framed as a rubber duck persona—designed to be helpful without undermining learning.

### 8.3.3 Academic honesty and the need to temper helpfulness

Modern AI tools can be *too helpful*. In a course setting, a system that simply produces final answers can function like an “overzealous friend” who completes your work rather than helping you learn.

As a result, CS50’s policy (as described in the course materials) prohibits using third-party AI tools that suggest or complete answers to questions or lines of code (for example, ChatGPT in its general form, GitHub Copilot, Bing Chat, and similar systems), because they can bypass the learning process.

At the same time, it would be reactionary to ignore the genuine potential for AI to support learning. CS50 therefore allows students to use **CS50’s own AI-based tools**, designed to behave more like a good teacher or teaching fellow: guiding students toward answers rather than handing over complete solutions.

---

## 8.4 How CS50’s AI Duck Works: Systems, Prompts, and APIs

### 8.4.1 APIs: borrowing capabilities from other companies

Many modern AI systems are accessed through **APIs** (Application Programming Interfaces). An API is a service boundary: another company provides a capability (like generating text), and your software sends requests and receives results.

In this model, the “heavy lifting”—the large language model computations—often happens on infrastructure operated by organizations such as OpenAI or Microsoft. A course or company can then build its own product on top of those services.

### 8.4.2 The problem of “recent” knowledge and the role of a vector database

Large language models are trained on data up to a certain point in time. If a model’s training data ends at a cutoff date, it may not “know” about:

- last week’s lecture,
- this semester’s assignments,
- course-specific conventions,
- newly updated documentation.

To address this, CS50 augments the AI with course-specific information stored in a local **vector database**. The purpose of this database is to enable searching for relevant, more recent information and then providing that information to the model as additional context, so the responses can be grounded in the course’s actual materials rather than only in the model’s older training data.

This pattern—retrieving current or local information and injecting it into the model’s context—is a practical way to improve accuracy and course relevance.

### 8.4.3 Prompt engineering: shaping the AI’s behavior with language

In current AI practice, a common technique is **prompt engineering**, which is less like “engineering” in the traditional mathematical sense and more like carefully written instructions in English.

A particularly important concept is the **system prompt**, which is a piece of text given to the model that describes how it should behave. CS50 uses a system prompt to encourage a teaching-assistant persona and to enforce constraints such as staying on-topic and not providing full problem set solutions.

Alongside the system prompt is the **user prompt**, which is the student’s actual question. Conceptually:

- The system prompt sets the role and boundaries (“how you should behave”).
- The user prompt supplies the immediate task (“what the user wants right now”).

This framing helps explain why the same underlying model can behave quite differently depending on how it is instructed.

---

## 8.5 Where Students Encounter the Duck: Integrated Help in the Programming Environment

CS50 students use **Visual Studio Code** through a browser-based environment at `cs50.dev`. Within that environment, the duck can provide several types of support that are particularly useful when learning:

### 8.5.1 Explaining highlighted code

Students can highlight one or more lines of code and request an explanation. The duck then produces a natural-language description of what those lines do.

This is especially valuable when the code looks “arcane,” as early C code often can, because the system can translate syntactic details into a narrative explanation.

### 8.5.2 Advising on code style and formatting

The duck can also propose improvements to code formatting and style—for instance, correcting indentation and structure so the code becomes more readable. Students can then ask the system to explain the changes, turning a purely aesthetic transformation into a learning moment about conventions and clarity.

### 8.5.3 Explaining error messages in plain English

Programming frequently produces error messages that are precise but unfriendly, especially to beginners. Another form of support is translating terminal or compiler errors into more approachable explanations, so students can focus on the underlying mistake instead of being blocked by unfamiliar wording.

### 8.5.4 AI-assisted Q&A with disclaimers and human endorsement

CS50 has also integrated the duck into an asynchronous Q&A platform used across courses. In this setting, the duck can answer questions quickly—often in seconds—providing what amounts to “virtual office hours.”

Because AI is not perfect, CS50 includes disclaimers such as an explicit reminder that the duck is experimental and that students should not assume correctness unless a human has endorsed the reply. Course staff can then mark responses as correct or add additional guidance.

This hybrid approach acknowledges a key reality: even when AI is highly useful, it can still be wrong in ways that sound confident.

---

## 8.6 From “AI as Magic” to “AI as Algorithms”: Starting with Games

To understand what makes AI work, it helps to begin with problems where the world can be described clearly, the possible actions are limited, and success can be measured. **Games** are ideal for this, because you can often reduce them to:

- a finite set of states (board positions, paddle positions),
- a finite set of actions (move left, move right),
- a clear objective (win, score points, survive).

### 8.6.1 Breakout and decision trees: turning intuition into rules

Consider *Breakout*, an early arcade game in which a paddle deflects a ball toward bricks. Humans can usually predict where the ball will go and move the paddle accordingly.

That intuitive reasoning can be represented as a **decision tree**, which is a branching structure of yes/no questions leading to actions:

- If the ball is left of the paddle, move the paddle left.
- Else if the ball is right of the paddle, move the paddle right.
- Else, do not move.

In pseudocode, that logic looks like:

- While the game is ongoing:
  - If the ball is left of the paddle: move left.
  - Else if the ball is right of the paddle: move right.
  - Else: do nothing.

This is a form of “AI” in the broad sense: it is a system that behaves intelligently in a limited domain. But it is also completely **deterministic** and **hand-authored**. A human has anticipated the relevant scenarios and encoded the response.

In simple games with predictable physics, this can be effective—but it does not scale well to domains where the number of situations explodes.

---

## 8.7 Tic-Tac-Toe, Minimax, and Scoring Game Outcomes

### 8.7.1 Strategy as a decision tree (win, block, otherwise…)

Tic-tac-toe is a useful next step because the state space is bigger than Breakout’s immediate “left/right” choice, and because planning ahead matters.

A natural decision-tree strategy begins with two core questions:

1. Can I win on this move (get three in a row)?
   - If yes, take the winning move.
2. If not, can my opponent win on their next move?
   - If yes, block that move.
3. Otherwise, the “best” move may require thinking more than one step ahead.

This is where human intuition often becomes inconsistent: many people play reasonably but not optimally, because the consequences of a move may be several turns away.

### 8.7.2 Assigning numeric values to outcomes

To make reasoning more systematic, we can assign **scores** to final board outcomes. One simple scoring scheme is:

- If **O** wins: score = **-1**
- If **X** wins: score = **+1**
- If the game is a draw: score = **0**

Now the players have opposite goals:

- **X** wants to **maximize** the score (prefer +1, tolerate 0, avoid -1).
- **O** wants to **minimize** the score (prefer -1, tolerate 0, avoid +1).

This converts “winning” and “losing” into a mathematical objective.

### 8.7.3 Minimax: choosing moves by looking ahead

The **minimax** algorithm is built on this idea. In words:

- If it’s X’s turn, evaluate each possible move and choose the one with the **highest** resulting score.
- If it’s O’s turn, evaluate each possible move and choose the one with the **lowest** resulting score.

A crucial detail is what “evaluate” means. In tic-tac-toe, you can expand a decision tree of future moves until you reach end states (wins, losses, draws). Those leaves have known values (+1, 0, -1). You then propagate those values backward through the tree:

- At an X node (X’s choice), you take the **maximum** child value.
- At an O node (O’s choice), you take the **minimum** child value.

Even when a player cannot force a win, minimax can still choose the move that avoids a loss—often producing a draw if that is the best achievable outcome.

### 8.7.4 Why minimax becomes hard: the tree gets enormous

Tic-tac-toe is small enough that brute-force lookahead is feasible. In fact, there are **255,168** possible games of tic-tac-toe—large for a human to enumerate, but manageable for a computer.

But the same approach scales poorly:

- In chess, considering only the first **four moves** back and forth yields about **288 million** possible sequences.
- In Go, the first four moves yield about **266 quintillion** possibilities.

At that scale, even modern computers cannot simply “search everything” to guarantee optimal play, because:

- the number of branches is too large,
- the required memory is too large,
- and the required time is too large.

This limitation motivates a shift from hand-authored rules and exhaustive search toward systems that can **learn patterns** from data and experience.

---

## 8.8 Machine Learning: Letting the Computer Learn Instead of Being Told

**Machine learning** is a subset of AI that focuses on enabling systems to improve performance without being explicitly programmed with step-by-step rules for every scenario. Instead of writing the full decision logic ourselves, we provide:

- data,
- feedback,
- and an objective,

and the system adjusts itself to perform better over time.

One particularly intuitive form is reinforcement learning.

---

## 8.9 Reinforcement Learning: Rewards, Punishments, and Learned Behavior

### 8.9.1 The core idea: maximize reward

In **reinforcement learning**, an agent (a program or robot) learns by trial and error. The system performs actions, observes outcomes, and receives feedback as a numeric reward:

- **+1** for desirable behavior,
- **-1** for undesirable behavior (or “punishment”).

If the agent is designed to maximize total reward, it will tend to repeat behaviors that lead to positive outcomes and reduce behaviors that lead to negative outcomes.

A key feature of reinforcement learning is that a human does not need to specify the correct action in every situation. Instead, the human (or environment) defines what counts as “good” or “bad,” and the agent discovers a strategy.

### 8.9.2 Pancake flipping as reinforcement learning

A vivid demonstration of this concept is training a robot to flip a pancake. Initially, the robot may fail repeatedly—dropping the pancake or flipping it incorrectly. Over many trials, with feedback indicating success or failure, the robot can learn the motion pattern that reliably produces a flip.

What makes this example especially instructive is that there is no single “line of code” that describes the perfect motion. The behavior emerges from repeated attempts and feedback.

### 8.9.3 The “Floor Is Lava” grid: learning paths through trial and error

Another reinforcement learning scenario can be represented as a grid:

- A starting position (the agent).
- A goal square (success).
- “Lava” squares (failure).

The agent can move up, down, left, or right. It does not begin with knowledge of where the hazards are. It must explore, suffer failures, and gradually learn which moves to avoid and which moves to prefer.

Over time, the agent can learn a safe path to the goal.

### 8.9.4 A key trade-off: exploring vs. exploiting

A learned solution is not always the best solution. If an agent discovers *a* safe path, it can “exploit” that knowledge by repeating it, but that path might be longer than necessary.

This introduces the fundamental tension between:

- **Exploiting**: using what you already know works.
- **Exploring**: trying something new to see if there is a better option.

A common way to formalize this is to add a small probability of making a random move. That probability is often denoted **epsilon (ε)**:

- With probability ε (for example, 10%), choose a random action (explore).
- Otherwise, choose the action with the highest known value (exploit).

The point is not randomness for its own sake; it is a disciplined way to avoid getting stuck in a solution that is locally good but globally suboptimal.

---

## 8.10 Deep Learning and Neural Networks: Learning Patterns Through Layers of Computation

Some problems are too complex for simple trial-and-error reward signals, or too high-dimensional to be handled with small tables of values. This is where **deep learning** becomes especially important.

Deep learning is closely associated with **neural networks**, which are computational structures inspired (loosely) by biological neurons. The inspiration is not that computers replicate biology exactly, but that networks of simple units can produce complex behavior when connected and tuned.

### 8.10.1 Neural networks as inputs, outputs, and learned parameters

A neural network can be described at a high level as:

- **Inputs**: numeric features that describe the situation.
- **Outputs**: a prediction or classification.
- **Internal structure**: layers of nodes (“neurons”) connected by weighted edges.
- **Parameters**: numbers (weights and biases) that determine how inputs are transformed into outputs.

Training a neural network means adjusting those parameters so that the network’s outputs match desired outcomes on many examples.

### 8.10.2 A simple classification example: red vs. blue points

Imagine a coordinate plane with:

- an x-axis and y-axis,
- points scattered in the plane,
- each point labeled either **red** or **blue**.

The computational task is: given a new point’s (x, y), predict whether it should be labeled red or blue.

A simple approach is to find a line that separates the plane into two regions:

- points on one side are predicted blue,
- points on the other side are predicted red.

Initially, a vertical line might separate many points correctly, but as more data appears, a diagonal line might perform better. The model is trying to find the boundary that best fits the observed labels.

### 8.10.3 The math beneath the boundary: a linear function

This kind of separation can be expressed as a function like:

\[
ax + by + c
\]

If the result is greater than 0, you predict one class (say, red). Otherwise, you predict the other class (say, blue).

In this framing:

- \(x\) and \(y\) are inputs,
- \(a\), \(b\), and \(c\) are parameters the model must learn.

The deep-learning idea generalizes this far beyond two inputs and one line. Real neural networks can have many layers, many nodes, and enormous numbers of parameters. Even the engineers building them do not necessarily have a human-interpretable meaning for each parameter; what matters is that the system performs well on prediction tasks.

---

## 8.11 From Predicting Labels to Generating Content: Large Language Models

Deep learning can be used not only to classify (“is this red or blue?”) but also to **generate** (“produce the next word,” “produce an image,” “produce a continuation of this sentence”).

### 8.11.1 Large language models: predicting the next token at scale

Systems like ChatGPT are built on **large language models (LLMs)**: very large neural networks trained on massive amounts of text. You can think of them as pattern-learning machines that have absorbed statistical regularities from enormous corpora—often described informally as “a lot of the internet,” plus other sources.

A practical way to understand their behavior is:

- The model reads a prompt (your input).
- It predicts what should come next.
- It repeats this process to generate a sequence of words.

Even though this process is based on prediction, the resulting text can look like reasoning, explanation, or conversation, because many examples of those forms exist in the data the model learned from.

### 8.11.2 Transformers and attention: handling long-range relationships in text

A major leap in language modeling came from the **transformer architecture**, introduced in a widely influential 2017 paper. One of the key ideas in transformers is **attention**.

Attention allows the model to assign different “importance” to different words in a sentence when interpreting or generating text. Intuitively:

- Some words strongly relate to other specific words.
- Some words (like articles and common prepositions) may contribute less meaningfully in many contexts.

By representing relationships between words with learned numeric values, the model can keep track of context more effectively—especially relationships between words that are far apart in the sentence.

This matters because older approaches struggled with long-distance dependencies. For example, in the sentence:

> “Massachusetts is a state in the New England region of the Northeastern United States. It borders on the Atlantic Ocean to the east. The state’s capital is …”

A system must connect “The state’s capital” back to “Massachusetts,” despite many intervening words. Modern models are substantially better at this kind of contextual linkage.

---

## 8.12 Embeddings: Turning Words into Numbers

Computers ultimately operate on numbers. For a language model to work with text, it must represent words (and pieces of words) numerically.

An **embedding** is a numeric representation of a word (or token) that captures aspects of its meaning and usage. In modern systems, an embedding is often a high-dimensional vector—meaning a long list of floating-point numbers.

For example, one commonly used embedding representation has **1,536** floating-point values for a single word. This is not meant to be human-readable; rather, it is a mathematical object that can be compared to other embeddings to measure similarity or relationship in a way that supports learning and prediction.

Embeddings help make “semantic proximity” computational: words and phrases used in similar contexts tend to end up with vectors that are “near” each other in the embedding space, allowing the model to generalize patterns rather than memorize only exact strings.

---

## 8.13 What Can Go Wrong: Hallucinations and Overconfidence

Despite their capabilities, LLMs can produce incorrect statements that sound plausible and confident. This phenomenon is commonly called a **hallucination**.

A useful way to understand hallucinations is to remember what the model is optimizing for: producing a likely continuation of text. Sometimes the most statistically “likely” continuation is not actually true.

In practice, this is why systems like CS50’s duck include disclaimers and human oversight. It is also why users must learn a new literacy: not only how to ask good questions, but how to verify claims, cross-check sources, and treat fluent output as *not automatically authoritative*.

---

## 8.14 A Closing Metaphor: The “Homework Machine” and the Limits of Apparent Perfection

A playful, cautionary metaphor for AI’s usefulness—and fallibility—appears in Shel Silverstein’s 1981 poem “Homework Machine,” in which a “perfect contraption” produces homework answers instantly, only to reveal a ridiculous mistake:

> “Here it is, 9 plus 4,  
> and the answer is 3.  
> 3?  
> Oh, me.  
> I guess it’s not as perfect  
> as I thought it would be.”

The poem captures something surprisingly modern: output can look polished and fast while still being wrong in ways that matter. As AI systems improve, the mistakes may become rarer and subtler, but the underlying lesson remains important—especially in education and in any setting where correctness matters.

---

## 8.15 Summary: A Mental Map of Modern AI

By connecting the visible world of generative AI back to foundational algorithms and learning paradigms, you now have a structured way to think about what “AI” means in practice:

- Some “AI” is simply **hand-written logic**, such as decision trees that translate human intuition into deterministic rules.
- Algorithms like **minimax** show how game-playing can be formalized with scoring and exhaustive lookahead—until the state space becomes too large.
- **Machine learning** shifts from explicit rules to systems that learn from data and feedback.
- **Reinforcement learning** uses reward signals to shape behavior through trial and error, while balancing **exploration vs. exploitation**, often with an epsilon-style randomness mechanism.
- **Deep learning** uses neural networks with many parameters to detect patterns and make predictions, even when the internal representations are not easily interpretable.
- **Large language models** apply deep learning to language generation, enabled by transformer architectures, attention mechanisms, and embeddings that represent words as high-dimensional numeric vectors.
- Today’s systems can still produce confident errors, making **verification** and **careful use** essential skills alongside programming itself.

This progression—from deterministic rules, to search, to learning, to generative models—reflects the broader arc of AI: when problems become too complex for humans to encode fully, we increasingly build systems that learn patterns from the world, and we then manage the trade-offs that come with that power.