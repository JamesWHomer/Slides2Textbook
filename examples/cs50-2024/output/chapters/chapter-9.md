# Chapter 9: Data at Scale — From CSV Files to Relational Databases with SQL

Software projects rarely stay small for long, and the moment your program has to store and analyze more than a handful of values, the question becomes less about *whether* you can write code to process data and more about *which tool is appropriate for the job*. You have already seen this pattern: using C for everything becomes painful once you want higher-level expressiveness, and Python often makes many tasks dramatically more pleasant. This chapter continues that progression by introducing a tool that is specifically designed for a particular kind of problem: storing, searching, and aggregating structured data efficiently.

That tool is **SQL**—*Structured Query Language*—a language designed not for general-purpose programming, but for asking questions of data that is stored in a **database**. The key idea is not “learn another language to collect languages,” but rather to recognize a theme that appears throughout computing: different problems call for different abstractions, different runtimes, and different ways of thinking.

We will begin with a familiar data format—**CSV files**—and use Python to read, summarize, and query them. Then we will deliberately hit a point where the Python approach starts to feel tedious and “too manual,” and we will use that discomfort as motivation to introduce SQL. From there we will build up relational database concepts, including **tables**, **schemas**, **primary keys**, **foreign keys**, and several common relationship patterns (one-to-one, one-to-many, and many-to-many). We will apply these ideas to a real-world dataset derived from IMDb, and we will end with two practical concerns that matter anytime databases are used in real systems: **performance** (via indexes) and **correctness/security** (via transactions and defenses against SQL injection).

---

## 9.1 Collecting and Exporting Data: Spreadsheets and “Flat File” Databases

A convenient way to gather structured data is to use a form-based interface, such as Google Forms, which automatically records responses into a spreadsheet. Conceptually, a spreadsheet is already a database-like structure: it stores information in **rows** and **columns**, where each row is typically one “record” (one form submission, one customer, one event) and each column represents one attribute (a timestamp, a name, a selection).

However, spreadsheets are primarily designed for human interaction—clicking, sorting, filtering, and using formulas—whereas programming often requires **automated** analysis and repeatable queries. The simplest bridge between those worlds is to export spreadsheet data into a plain text format that programs can read easily.

### 9.1.1 CSV: Comma-Separated Values

A **CSV file** (Comma-Separated Values) is a plain text representation of a table:

- Each **row** is written on its own line, separated by newline characters (`\n`).
- Each **column** within a row is separated by a delimiter, most commonly a comma (`,`).

Because CSV is plain text, it is widely portable: it can be produced by Google Sheets, Excel, Apple Numbers, and countless other systems, and it can be consumed by programs written in almost any language.

A CSV file often begins with a **header row**, which is a special first row that names the columns. For example, a file might begin with something like:

- `Timestamp,language,problem`

followed by many rows of actual data.

### 9.1.2 A subtlety: commas *inside* data

CSV seems simple until you notice a problem: what if a field contains a comma as part of its content? For instance, a value like `"Hello, World"` includes a comma, which would normally be interpreted as a delimiter between columns.

The conventional solution is **quoting**: if a field contains a comma (or certain other special characters), it is wrapped in double quotes so that CSV readers treat the comma as literal content rather than as a separator. Spreadsheet software typically handles this automatically when exporting.

This detail matters because it explains why “just splitting each line on commas” is not a robust way to parse CSV; you generally want to use a CSV parser library that properly handles quoting and escaping rules.

---

## 9.2 Reading CSV Data with Python

Python includes a standard module called `csv` that understands the CSV format and provides tools for reading it safely and conveniently.

Suppose you have a file named `favorites.csv`, exported from a spreadsheet. It contains responses to questions like “favorite language” and “favorite problem,” along with an automatically generated timestamp. That means each row has three columns:

1. `Timestamp`
2. `language`
3. `problem`

### 9.2.1 Opening files: `open` vs. `with open(...)`

You can open a file in Python using:

```python
file = open("favorites.csv", "r")
# use file
file.close()
```

This resembles the pattern you may recognize from C (`fopen` / `fclose`), but Python commonly encourages a more robust pattern using `with`, which automatically closes the file for you when the block ends:

```python
with open("favorites.csv", "r") as file:
    # use file
# file is now closed automatically
```

The advantage is not just convenience: automatic closing is safer, especially when errors occur.

### 9.2.2 Reading rows with `csv.reader`

A straightforward approach is to create a **reader** that yields each row as a list of strings:

```python
import csv

with open("favorites.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip the header row
    for row in reader:
        print(row[1])  # language is column 1 (0-indexed)
```

Here, `row` is a list with three elements. Because Python lists are zero-indexed:

- `row[0]` is the timestamp
- `row[1]` is the language
- `row[2]` is the problem

This works, but it quietly assumes that column positions never change. If someone rearranges the spreadsheet columns and re-exports the CSV, code like `row[1]` can suddenly refer to the wrong column.

### 9.2.3 Making CSV code more robust with `csv.DictReader`

To avoid fragile “magic indices,” Python also provides `csv.DictReader`, which uses the header row as dictionary keys. Each row becomes a dictionary mapping column names to values:

```python
import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["language"])
```

This approach is more resilient: even if column order changes, as long as the header names remain consistent, the code continues to work.

---

## 9.3 Counting Categories in Python: From Manual Counters to Dictionaries and `Counter`

Once you can read rows, a natural next step is to *summarize* the data: for example, count how many people chose each favorite language.

### 9.3.1 The manual approach: separate variables

One way is to create one variable per category:

```python
scratch = 0
c = 0
python = 0

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        favorite = row["language"]
        if favorite == "Scratch":
            scratch += 1
        elif favorite == "C":
            c += 1
        elif favorite == "Python":
            python += 1

print(f"Scratch: {scratch}")
print(f"C: {c}")
print(f"Python: {python}")
```

This is not “wrong,” but it is rigid:

- It assumes you know all categories in advance.
- It grows awkward if more categories are added (for example, if “SQL” becomes an option later).

### 9.3.2 A more general approach: a dictionary of counts

A **dictionary** is a natural fit for counting: use the category as the key and the running total as the value.

```python
counts = {}

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        favorite = row["language"]
        if favorite in counts:
            counts[favorite] += 1
        else:
            counts[favorite] = 1

for favorite in counts:
    print(f"{favorite}: {counts[favorite]}")
```

This version adapts automatically to new categories because it does not hard-code them into variables.

### 9.3.3 Sorting results in Python

If you want output in a specific order, Python’s `sorted` can help.

Sorting by key (alphabetical):

```python
for favorite in sorted(counts):
    print(f"{favorite}: {counts[favorite]}")
```

Sorting by value (count), using `counts.get` as the key function:

```python
for favorite in sorted(counts, key=counts.get):
    print(f"{favorite}: {counts[favorite]}")
```

Reversing to get largest-first:

```python
for favorite in sorted(counts, key=counts.get, reverse=True):
    print(f"{favorite}: {counts[favorite]}")
```

This highlights an important Python idea: objects (like dictionaries) come with associated methods (like `.get`), and many built-in tools accept functions as parameters to control behavior.

### 9.3.4 The library approach: `collections.Counter`

Counting categories is so common that Python provides a dedicated tool:

```python
import csv
from collections import Counter

counts = Counter()

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        counts[row["language"]] += 1

for favorite, count in counts.most_common():
    print(f"{favorite}: {count}")
```

A `Counter` automatically treats missing keys as having count 0, so you can increment without writing `if/else` initialization logic.

### 9.3.5 Making analysis interactive

Once you have counts, you can also build a small interactive tool:

```python
favorite = input("Favorite problem: ")
print(f"{favorite}: {counts[favorite]}")
```

This is a useful pattern in data analysis: build code that loads and summarizes data once, and then allows fast queries.

### 9.3.6 The motivation for SQL: “I am writing too much code to ask simple questions”

Even with `Counter`, you are still writing code, loops, and bookkeeping. The moment you find yourself repeatedly writing “read every row, filter it, count it, sort it,” you are experiencing the reason SQL exists: databases are built to do this kind of work directly.

---

## 9.4 Databases and SQL: A Tool Designed for Structured Queries

A **database** is software designed to store data, manage it over time, and answer questions about it efficiently. Instead of keeping data in a plain text file, you store it in a database file or on a database server, and you query it with SQL.

### 9.4.1 Relational databases: tables and relations

A **relational database** stores data in one or more **tables**, where each table resembles a spreadsheet sheet: rows and columns. The word “relational” emphasizes that you can have **multiple tables** with **relationships** between them, rather than one giant sheet that tries to contain everything.

### 9.4.2 SQL as a declarative language

SQL is typically a **declarative** language:

- In Python, you often say *how* to compute something: loop over rows, increment counters, sort a list.
- In SQL, you usually say *what* you want: “count rows where language is C,” or “group by language,” and the database decides how to execute that request efficiently.

### 9.4.3 CRUD: the basic operations

In most database systems, you can describe the main capabilities with **CRUD**:

- **Create**: add new data
- **Read**: retrieve data
- **Update**: change existing data
- **Delete**: remove data

SQL’s common keywords align with these ideas:

- **INSERT**: add rows (create data)
- **SELECT**: retrieve rows (read data)
- **UPDATE**: modify rows (update data)
- **DELETE**: remove rows (delete data)

Some systems also include **DROP**, which deletes entire tables—powerful and dangerous.

---

## 9.5 SQLite: A Lightweight SQL Database

There are many database systems (with slightly different dialects of SQL), including Oracle, MySQL, PostgreSQL, and Microsoft SQL Server. In this chapter’s examples, we use **SQLite**, a lightweight and widely used SQL implementation.

SQLite is common on desktops and mobile devices because it stores a database in a single local file (often with extension `.db`) and does not require running a separate server process.

### 9.5.1 Creating a database from a CSV file

Suppose you have `favorites.csv`. You can create a SQLite database `favorites.db` and import the CSV into a table.

From the terminal:

1. Start SQLite and create/open the database file:

```text
sqlite3 favorites.db
```

2. Switch SQLite into CSV import mode:

```text
.mode csv
```

3. Import the CSV as a table (here named `favorites`):

```text
.import favorites.csv favorites
```

4. Quit SQLite:

```text
.quit
```

You now have a binary database file `favorites.db` that contains the CSV’s contents in table form.

### 9.5.2 Inspecting the database: `.schema`

When you open the database again:

```text
sqlite3 favorites.db
```

You can ask SQLite to show the **schema**, meaning the structural definition of tables:

```text
.schema
```

or for a specific table:

```text
.schema favorites
```

In SQLite, commands beginning with a dot (like `.schema`) are SQLite-specific “meta commands,” not standard SQL. By contrast, keywords like `SELECT`, `FROM`, `WHERE`, `GROUP BY`, and `ORDER BY` are standard SQL concepts.

---

## 9.6 Querying Data with SQL: SELECT, WHERE, LIMIT, COUNT, DISTINCT

### 9.6.1 Selecting rows and columns

To retrieve data, SQL uses `SELECT ... FROM ...`.

Select every column (`*`) from a table:

```sql
SELECT * FROM favorites;
```

Select one column:

```sql
SELECT language FROM favorites;
```

Because databases can contain many rows, it is often useful to limit output:

```sql
SELECT language FROM favorites LIMIT 10;
```

### 9.6.2 Counting rows

If you want the number of rows:

```sql
SELECT COUNT(*) FROM favorites;
```

This returns a small result table with a single value.

### 9.6.3 DISTINCT values

To find which distinct languages appear:

```sql
SELECT DISTINCT(language) FROM favorites;
```

To count how many distinct languages appear:

```sql
SELECT COUNT(DISTINCT(language)) FROM favorites;
```

This demonstrates a common pattern: SQL functions can be **nested**, passing the output of one function into another.

### 9.6.4 Filtering with WHERE

SQL uses `WHERE` to filter rows without writing loops and `if` statements.

Count how many rows have language `"C"`:

```sql
SELECT COUNT(*) FROM favorites WHERE language = 'C';
```

Filter by multiple conditions using boolean operators like `AND`:

```sql
SELECT COUNT(*)
FROM favorites
WHERE language = 'C' AND problem = 'Hello, World';
```

Notice an important difference from C and Python:

- SQL uses `=` for equality comparison (similar to Scratch), not `==`.

---

## 9.7 Aggregation with GROUP BY and ORDER BY: Doing in One Line What Took Many Lines in Python

The counting task that required dictionaries or `Counter` in Python becomes very concise in SQL.

### 9.7.1 Grouping and counting

Count how many times each language appears:

```sql
SELECT language, COUNT(*)
FROM favorites
GROUP BY language;
```

Here, `GROUP BY language` “smushes together” all rows with the same language and lets `COUNT(*)` compute how many were in each group.

### 9.7.2 Ordering by count

To sort these groups by how frequent they are:

```sql
SELECT language, COUNT(*)
FROM favorites
GROUP BY language
ORDER BY COUNT(*);
```

This sorts in ascending order by default. To reverse it:

```sql
SELECT language, COUNT(*)
FROM favorites
GROUP BY language
ORDER BY COUNT(*) DESC;
```

### 9.7.3 Aliases with AS

If you want to refer to `COUNT(*)` more easily, you can give it an alias:

```sql
SELECT language, COUNT(*) AS n
FROM favorites
GROUP BY language
ORDER BY n DESC;
```

### 9.7.4 Top results with LIMIT

To get the single most popular language:

```sql
SELECT language, COUNT(*) AS n
FROM favorites
GROUP BY language
ORDER BY n DESC
LIMIT 1;
```

The combination of `GROUP BY`, `ORDER BY`, and `LIMIT` is one of the most common patterns in real SQL usage.

---

## 9.8 INSERT, DELETE, and UPDATE: Changing Data (and Why It Can Be Dangerous)

SQL is not only for reading; it can modify data as well.

### 9.8.1 Inserting rows

To insert a new row, use `INSERT INTO ...`.

For example, you might insert a new favorite language and problem while leaving timestamp unspecified:

```sql
INSERT INTO favorites (language, problem)
VALUES ('SQL', 'Fiftyville');
```

If a column is not provided, it may become `NULL`, which represents the absence of a value. In SQL, `NULL` is not a pointer address; it is simply the database’s way of saying “no value here.”

### 9.8.2 Deleting rows

A dangerous command is:

```sql
DELETE FROM favorites;
```

This deletes **all rows**. Without a `WHERE` clause, it is catastrophic.

A safer pattern is to delete only rows matching a condition, such as removing entries with missing timestamps:

```sql
DELETE FROM favorites
WHERE Timestamp IS NULL;
```

The presence of `WHERE` is the difference between a targeted change and wiping a table.

### 9.8.3 Updating rows

Similarly, `UPDATE` can change many rows. Without a `WHERE` clause, it changes *all* rows:

```sql
UPDATE favorites
SET language = 'SQL', problem = 'Fiftyville';
```

This kind of command illustrates why production systems rely on careful access control, backups, review processes, and often separate “staging” databases. SQL is powerful enough to make irreversible mistakes quickly.

---

## 9.9 Designing Data Well: Normalization and Relational Structure

So far, our `favorites` data lived comfortably in a single table. Many real-world data sets do not.

To see why, consider modeling TV shows and the people who star in them.

### 9.9.1 The “too many columns” problem

A naïve spreadsheet design might try to represent a show like *The Office* as:

- `title`
- `star1`
- `star2`
- `star3`
- ...

But shows have different numbers of stars. Some rows would need 2 star columns; others might need 20. The table becomes jagged and sparse, with many empty cells.

### 9.9.2 The “too much duplication” problem

A second attempt might place each (show, star) pair on its own row:

- `title`, `star`
- `The Office`, `Steve Carell`
- `The Office`, `Rainn Wilson`
- ...

This avoids the jagged edge, but it repeats the string `"The Office"` many times. Repeating long strings wastes space and creates opportunities for inconsistencies (typos, formatting differences, accidental edits).

### 9.9.3 Normalization: store facts once, relate them with IDs

A common relational approach is to split data into multiple tables, each with a **unique identifier**:

- A **shows** table: one row per show (with a unique show ID)
- A **people** table: one row per person (with a unique person ID)
- A **stars** table: a linking table that associates show IDs with person IDs

This design:

- stores each show title once,
- stores each person name once,
- uses numeric IDs to represent relationships.

Although the `stars` table repeats the show ID multiple times, repeating a small integer is typically far cheaper than repeating the entire show title string, and it is better suited for fast indexing and joins.

---

## 9.10 IMDb as a Case Study: Multiple Tables and Real Queries

To practice SQL on large, realistic data, consider a database derived from IMDb data, stored in a file such as `shows.db`. This database includes multiple tables, including:

- `shows` (show metadata)
- `ratings` (rating and vote counts)
- `genres` (genre labels per show)
- `people` (people involved)
- `stars` (show–person starring relationships)
- `writers` (show–person writing relationships)

### 9.10.1 Exploring tables with small samples

A practical first step with any unfamiliar database is to inspect a few rows:

```sql
SELECT * FROM shows LIMIT 10;
SELECT * FROM ratings LIMIT 10;
```

You can also count scale:

```sql
SELECT COUNT(*) FROM shows;
```

A database like this can contain hundreds of thousands of rows, far beyond what you would want to process by hand in a spreadsheet.

### 9.10.2 Understanding schemas and types

Viewing schemas reveals column types and constraints.

For example, `shows` might have:

- `id` (INTEGER, primary key)
- `title` (TEXT, NOT NULL)
- `year` (NUMERIC)
- `episodes` (INTEGER)

And `ratings` might have:

- `show_id` (INTEGER, NOT NULL, foreign key)
- `rating` (REAL, NOT NULL)
- `votes` (INTEGER, NOT NULL)

SQLite uses a small family of types such as:

- **INTEGER**: whole numbers
- **REAL**: floating-point values
- **TEXT**: strings
- **NUMERIC**: often used for date/time-like values or numeric data not strictly typed as integer/real
- **BLOB**: binary large objects (files or raw bytes), though it is often better to store large files outside the database and store file paths in the database instead

Additionally, schemas can impose constraints like:

- **NOT NULL**: the value must be present
- **UNIQUE**: no duplicates allowed
- **PRIMARY KEY**: the unique identifier for rows in a table
- **FOREIGN KEY**: a value that references a primary key in another table

---

## 9.11 Primary Keys, Foreign Keys, and Relationship Patterns

### 9.11.1 Primary keys

A **primary key** is a column (or set of columns) whose value uniquely identifies a row in a table. For a `shows` table, `id` is typically the primary key: two different shows should not share the same `id`.

### 9.11.2 Foreign keys

A **foreign key** is a column whose values are primary keys in another table.

For example, `ratings.show_id` refers to `shows.id`. The show ID is “foreign” to the `ratings` table in the sense that the ID originates as the primary key of a different table.

### 9.11.3 One-to-one, one-to-many, many-to-many

Different real-world relationships map naturally to different table patterns:

- **One-to-one**: each show has exactly one rating record (as a design decision). This could be stored in the same table, but keeping it separate can be convenient or reflect data sources.
- **One-to-many**: a show can have multiple genres (comedy, adventure, family). This means one show ID appears in multiple genre rows.
- **Many-to-many**: a show can have many stars, and a person can star in many shows. This typically requires a linking table (like `stars`) containing pairs of IDs.

---

## 9.12 Subqueries and JOINs: Combining Tables to Answer Real Questions

Once data is split across tables, you need tools to recombine it when querying. SQL provides two common approaches:

1. **Subqueries** (nested `SELECT` statements)
2. **JOINs** (explicitly combining tables on matching keys)

Both are widely used.

### 9.12.1 A first question: shows with rating ≥ 6.0

If you query `ratings` alone, you can find show IDs:

```sql
SELECT show_id
FROM ratings
WHERE rating >= 6.0
LIMIT 10;
```

But those IDs are not meaningful to humans. To get titles, you can use a subquery:

```sql
SELECT title
FROM shows
WHERE id IN (
    SELECT show_id
    FROM ratings
    WHERE rating >= 6.0
)
LIMIT 10;
```

This reads naturally if you think inside-out:

1. Find the show IDs with rating ≥ 6.0.
2. Select titles for shows whose IDs are in that set.

However, this still does not show the ratings next to the titles, because the rating lives in a different table.

### 9.12.2 Joining shows and ratings to get title + rating together

A `JOIN` combines tables by aligning matching rows on a condition, typically involving a primary key and foreign key:

```sql
SELECT title, rating
FROM shows
JOIN ratings ON shows.id = ratings.show_id
WHERE rating >= 6.0
LIMIT 10;
```

Here, the dot notation `shows.id` means “the `id` column in the `shows` table,” which is especially helpful when multiple tables have columns with similar names.

This produces a “wider” result that contains fields from both tables.

### 9.12.3 One-to-many joins: why duplication appears in results

When you join a one-to-many relationship, you often see repeated data in the result set.

For example, a show with multiple genres will appear multiple times when joined with the `genres` table—once per genre—because a SQL result table cannot have “gaps.” Each row in the result represents one particular match between show and genre.

A query like:

```sql
SELECT title, genre
FROM shows
JOIN genres ON shows.id = genres.show_id
WHERE shows.id = 63881;
```

might yield:

- `Catweazle | Adventure`
- `Catweazle | Comedy`
- `Catweazle | Family`

This duplication is not necessarily “waste” in the database; it is simply a consequence of representing multiple related rows in a flat result table.

---

## 9.13 Many-to-Many Relationships: Shows, People, and the Stars Linking Table

The `stars` table exists to connect shows and people. It typically contains:

- `show_id` (foreign key to `shows.id`)
- `person_id` (foreign key to `people.id`)

This structure supports the idea that:

- one show has many people,
- one person appears in many shows.

### 9.13.1 Example: finding the right “The Office”

A title might not be unique in a database. If you query:

```sql
SELECT * FROM shows WHERE title = 'The Office';
```

you may get multiple results from different years. Adding a year disambiguates:

```sql
SELECT * FROM shows
WHERE title = 'The Office' AND year = 2005;
```

### 9.13.2 Subquery approach: who starred in The Office (2005)?

To get the stars’ names, you can walk through the linking table:

1. Find the show ID for The Office (2005).
2. Find all person IDs in `stars` for that show ID.
3. Find names in `people` for those person IDs.

In SQL, that can be written as nested queries:

```sql
SELECT name
FROM people
WHERE id IN (
    SELECT person_id
    FROM stars
    WHERE show_id = (
        SELECT id
        FROM shows
        WHERE title = 'The Office' AND year = 2005
    )
);
```

This structure is conceptually straightforward: each layer produces the identifiers needed by the next layer.

### 9.13.3 Reversing the query: what shows has Steve Carell starred in?

You can also start from a person’s name and walk outward:

```sql
SELECT title
FROM shows
WHERE id IN (
    SELECT show_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Steve Carell'
    )
);
```

### 9.13.4 Joining three tables instead of nesting subqueries

You can express the same idea using explicit joins across three tables:

```sql
SELECT title
FROM shows
JOIN stars  ON shows.id = stars.show_id
JOIN people ON stars.person_id = people.id
WHERE name = 'Steve Carell';
```

And there is also a style that lists multiple tables and uses `WHERE` clauses to connect them:

```sql
SELECT title
FROM shows, stars, people
WHERE shows.id = stars.show_id
  AND people.id = stars.person_id
  AND name = 'Steve Carell';
```

These are different ways to express the same relational logic. In practice, codebases tend to standardize on a style for readability, but you will encounter all of these forms.

### 9.13.5 Writers as another relationship table

A `writers` table often mirrors `stars` structurally: it links shows and people, but the relationship represents “writing credits” rather than “starring credits.” The distinction is carried by the table name and the data it contains, even if the schema looks similar.

---

## 9.14 Performance: Indexes and the Time–Space Trade-off

A database is not only a storage format; it is an execution engine for queries. Some queries are fast, others slow, and real systems care deeply about the difference.

### 9.14.1 Timing queries with `.timer`

SQLite can report how long queries take:

```text
.timer on
```

Then you can run a query such as:

```sql
SELECT * FROM shows WHERE title = 'The Office';
```

Even a fraction of a second matters when multiplied by millions of users.

### 9.14.2 Indexes: making searches faster

An **index** is a data structure that accelerates searches on a column. You can create one with:

```sql
CREATE INDEX title_index ON shows(title);
```

This can dramatically reduce query time for searches that filter by `title`.

Under the hood, databases often implement indexes using a **B-tree** (not a binary tree). A B-tree is “short and wide”: nodes can have many children, which reduces the tree’s height and reduces how many steps are needed to locate a value. This is closely related to the general idea from data structures: better organization can turn slow linear scans into much faster logarithmic-time searches.

### 9.14.3 Indexes for foreign keys and frequently filtered columns

Primary keys are commonly indexed automatically, but foreign keys are not necessarily indexed by default. If you repeatedly filter or join on foreign keys (like `stars.show_id` or `stars.person_id`) or on frequently searched text fields (like `people.name`), indexes can help.

For example:

```sql
CREATE INDEX person_index ON stars(person_id);
CREATE INDEX show_index   ON stars(show_id);
CREATE INDEX name_index   ON people(name);
```

Adding these indexes can reduce multi-table queries from seconds to milliseconds.

### 9.14.4 The trade-off: why not index everything?

Indexes improve read performance, but they cost resources:

- **Space**: indexes take additional storage.
- **Write overhead**: inserts, updates, and deletes become slower because the database must also update index structures.

This is a classic time–space trade-off: you spend memory/disk space and maintenance work to gain speed on queries that matter.

---

## 9.15 Using SQL from Python: Combining Tools

Real applications rarely ask users to type SQL into a database prompt. Instead:

- a program (Python, Java, JavaScript, etc.) receives user input,
- the program queries the database using SQL,
- the program formats the result as a webpage, app screen, or report.

### 9.15.1 A Python interface to SQLite via the CS50 library

One convenient interface uses the CS50 Python library:

```python
from cs50 import SQL

db = SQL("sqlite:///favorites.db")

favorite = input("Favorite problem: ")

rows = db.execute(
    "SELECT COUNT(*) AS n FROM favorites WHERE problem = ?",
    favorite
)

row = rows[0]
print(row["n"])
```

Several details matter here:

- `sqlite:///favorites.db` is a common connection-string style. The triple slash is part of the convention for a local SQLite file.
- `db.execute(...)` returns a list of rows (a result set).
- `COUNT(*) AS n` names the count column `n` so it is easy to retrieve.
- The `?` is a **placeholder** for user input.

That last point is not just syntactic convenience—it is a major security feature.

---

## 9.16 Correctness at Scale: Transactions and Race Conditions

When you have many users, many servers, and many concurrent actions, correctness becomes subtle. A database is often the shared state that everyone is trying to update, and if updates are not handled carefully, you can get results that are *plausible but wrong*.

### 9.16.1 The “likes” problem and race conditions

Consider a system that tracks likes on a post. A naïve approach might do:

1. `SELECT likes FROM posts WHERE id = ?`
2. In Python, compute `likes + 1`
3. `UPDATE posts SET likes = ? WHERE id = ?`

The problem is concurrency: if multiple users like the same post at nearly the same time, multiple servers might read the same old value (say, 1,000,000), then all update it to 1,000,001—effectively losing likes.

This is a form of **race condition**: the system’s outcome depends on the timing and interleaving of operations.

A memorable analogy is the “milk in the fridge” problem:

- Person A opens the fridge, sees no milk, goes to buy milk.
- Person B opens the fridge before A returns, sees no milk, also buys milk.
- Now you have too much milk because each person acted on stale state.

In a database, you can get the opposite problem (lost increments) because multiple updates overwrite each other.

### 9.16.2 Transactions: grouping operations atomically

A common solution is a **transaction**, which groups multiple operations so they behave as one **atomic** unit: either all succeed together, or none do, and the database prevents dangerous interleavings that would corrupt the logic.

Conceptually, a program can:

- `BEGIN TRANSACTION`
- perform a sequence of reads/writes
- `COMMIT`

The idea is: do not allow another concurrent process to slip in between “read the old value” and “write the new value” in a way that causes the math to break.

Transactions are a large topic (with different isolation levels and trade-offs), but the core takeaway is simple: concurrency makes “obvious” code incorrect unless you deliberately protect multi-step updates.

---

## 9.17 Security: SQL Injection and the Importance of Placeholders

A second major real-world issue is not about speed or concurrency, but about attackers (or curious users) providing input that changes the meaning of your SQL.

### 9.17.1 The dangerous pattern: building SQL with string formatting

Suppose a developer writes:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
rows = db.execute(query)
```

This feels natural if you have recently learned Python f-strings. Unfortunately, it is unsafe.

In SQL (including SQLite):

- strings are quoted with single quotes `'...'`
- comments can begin with `--`, meaning “ignore the rest of the line”

An attacker could type a username like:

```text
mail@harvard.edu'--
```

This closes the developer’s quote and turns the remainder (including the password check) into a comment. The resulting query effectively becomes “select user where username matches,” with the password condition ignored.

This is a **SQL injection attack**: user input is injected into SQL syntax, altering the query itself.

### 9.17.2 The safe pattern: parameterized queries with placeholders

The correct defense is to use placeholders (`?` in SQLite-style parameterization) and pass parameters separately:

```sql
SELECT * FROM users WHERE username = ? AND password = ?;
```

When you do this through a proper library call (as with `db.execute(..., username, password)`), the library ensures that dangerous characters are escaped or treated as literal data rather than executable SQL syntax.

The essential habit is:

- never build SQL by concatenating user input into query strings,
- always use parameterized queries (placeholders).

---

## 9.18 Summary: What SQL Adds to Your Toolkit

By moving from CSV processing in Python to relational databases with SQL, you gain a new way to think about data and a new set of tools that dramatically reduce the amount of code required for common analytics tasks.

Key concepts from this chapter include:

- **CSV files** as a portable, plain-text “flat file” representation of tabular data, including the importance of quoting to handle commas inside fields.
- Python’s `csv.reader` and `csv.DictReader`, and why dictionaries keyed by header names are more robust than numeric indices.
- Counting patterns in Python, progressing from manual counters → dictionaries → `collections.Counter`, and using sorting with `sorted(...)`, including `key=counts.get` and `reverse=True`.
- **SQL** as a declarative language designed for asking questions of data, organized around CRUD operations: **INSERT**, **SELECT**, **UPDATE**, and **DELETE**.
- SQLite workflows for importing CSV data, viewing schemas (`.schema`), and querying with `SELECT`, `WHERE`, `LIMIT`, `COUNT`, `DISTINCT`, `GROUP BY`, and `ORDER BY`.
- Relational database design principles, including **normalization**, **primary keys**, **foreign keys**, and relationship patterns: one-to-one, one-to-many, and many-to-many.
- How to combine tables with **subqueries** and **JOINs**, including why one-to-many joins naturally produce repeated rows in result sets.
- Performance improvements using **indexes**, commonly implemented with B-trees, and the associated **time–space trade-off**.
- Practical systems concerns:
  - **transactions** for correctness under concurrency (avoiding race conditions),
  - **parameterized queries** to prevent **SQL injection**.

The larger lesson is consistent with the broader arc of programming: as data grows and systems become multi-user and long-lived, the “right tool for the job” becomes less optional and more fundamental. SQL and relational databases are one of the most enduring examples of that principle.