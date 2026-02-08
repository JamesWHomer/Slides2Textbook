# Chapter 11: Flask — Building Dynamic Web Applications with Python

In the previous chapter, we treated the browser primarily as a viewer for **static files**: HTML documents, CSS style sheets, JavaScript programs, and media assets that already existed on disk before any user ever visited the site. A simple web server such as `http-server` is perfectly suited to that world, because its job is essentially to map a URL path to a file on the server and then return that file’s bytes as an HTTP response.

Modern web experiences, however, are rarely that static. When you search on Google, no engineer has prewritten an HTML file for every possible query. When you open Gmail, no one has pre-generated a web page for the precise set of emails that will be relevant to you at this moment. Instead, a modern web application takes **input**, performs **logic**, often consults **data storage** (such as a database), and then produces **output**—frequently generating HTML dynamically, and increasingly exchanging data in machine-readable formats such as JSON.

This chapter introduces **Flask**, a popular Python “microframework” for building web applications. The term *framework* here means two things at once:

1. **Code** you can reuse (functions and libraries that solve common problems, like parsing query strings or issuing redirects), and  
2. **Conventions** you adopt (standard file names, folder structures, and patterns for organizing your application).

Flask is called a *microframework* because it is comparatively small and lightweight; it solves a core set of web-application problems without forcing you into an unusually large or complex system. There are larger frameworks (for example, Django), but Flask provides a clean way to learn concepts that transfer well to other environments.

---

## 11.1 From URLs-as-Filenames to URLs-as-Routes

When you serve static content, it is natural to think of URLs as mapping directly to files:

- `/` often maps to a default file such as `index.html`.
- `/folder/` might map to `folder/index.html`.
- `/folder/file.html` maps to a specific file.

Once you write your own server logic, you can treat everything after the domain name more abstractly. Instead of thinking “this path must correspond to a real file,” you can think:

- Everything after the domain is a **path**, and in web-application terminology that path is often called a **route**.
- A route is simply a string such as `/`, `/greet`, `/register`, or `/search`.
- A route is associated with **code**, not necessarily with a file.

This shift is one of the core mental changes when moving from static sites to web applications: a path is no longer just a location on disk; it is an entry point into your program.

---

## 11.2 Flask’s Typical Project Layout

Flask does not require one particular layout, but it strongly encourages conventions that make projects predictable. A common structure is:

- `app.py`  
  The main Python program (the “controller” logic) that defines routes and what they do.

- `templates/`  
  A folder containing HTML templates (often with placeholders and control flow). Flask expects templates here by convention.

- `static/`  
  A folder for files served “as-is,” such as `.css`, `.js`, and images. These are called *static* not because they never change during development, but because the server does not dynamically generate them per-request.

- `requirements.txt`  
  A list (one per line) of third-party libraries your project depends on, so that installation is repeatable.

These conventions matter because they reduce “where did we put that file?” friction, especially when collaborating, debugging, or returning to a project later.

---

## 11.3 Your First Flask Application: A Route That Returns Text

A minimal Flask program begins by importing Flask and creating an “app” object:

```python
from flask import Flask

app = Flask(__name__)
```

The argument `__name__` is a special Python variable that evaluates to the current module’s name, and it is a conventional way to let Flask know where your application code lives without hard-coding filenames.

To associate a URL route with code, Flask uses a *decorator* syntax: `@app.route(...)`. Conceptually, you are telling Flask, “When someone requests this path, call this function.”

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hello, world"
```

If you run this application with Flask’s development server (commonly via `flask run`), visiting the server’s `/` path produces the response body `hello, world`.

At this stage, notice what is happening: you are not serving an HTML file at all. You are producing a response body directly from Python. The browser will display it, but “View Page Source” will show that this is not HTML—just plain text.

This is already an application in the sense that **code** is generating output, but it is not yet producing the kind of structured web pages we typically want.

---

## 11.4 Returning HTML with `render_template`

Flask’s `render_template` function solves a common need: “Take an HTML file from my templates folder and return it as the HTTP response.”

A typical `app.py` might import three frequently used pieces from Flask:

```python
from flask import Flask, render_template, request
```

- `Flask` creates the app object.
- `render_template` loads an HTML template from `templates/` and returns it to the browser.
- `request` represents the incoming HTTP request (headers, parameters, method, and more).

If your project has:

- `app.py`
- `templates/index.html`

then you can do:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

Now the browser receives a full HTML document (whatever is in `templates/index.html`), and “View Page Source” will show that HTML.

At this point you have still built something that could have been served statically, but you have placed yourself in a position to make it dynamic, because a Python function is now in control of the response.

---

## 11.5 Query Strings and `request.args`: Input via GET

One of the simplest ways a browser sends input to a server is the **query string**, appended to the URL after a `?`, with key–value pairs separated by `&`:

- `/greet?name=David`
- `/search?q=cats`
- `/search?q=cats&lang=en`

When the browser uses the HTTP method **GET**, these key–value pairs appear in the URL. Flask parses them for you and exposes them as a dictionary-like object:

- `request.args`

For example, if you want to greet the user by name, you might place a placeholder in your HTML template:

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>hello</title>
    <meta name="viewport" content="initial-scale=1, width=device-width">
  </head>
  <body>
    hello, {{ name }}
  </body>
</html>
```

The double curly brace syntax `{{ ... }}` is not Python and not HTML; it comes from a templating language called **Jinja**, which Flask uses for templates. In Jinja, `{{ name }}` means: “Insert the value of the variable `name` here.”

In Python, you can obtain the query parameter and pass it into the template:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args["name"]
    return render_template("index.html", name=name)
```

Now, visiting:

- `/?name=David`

will render:

- `hello, David`

### 11.5.1 Defensive coding: missing keys and HTTP 400

The line:

```python
name = request.args["name"]
```

assumes that the `name` parameter exists. If it does not, the request can fail, and you may see an HTTP error such as **400** (a client-side error indicating a “bad request” situation for your application’s expectations).

Two common strategies avoid this failure:

#### Strategy A: Explicit conditional logic

```python
if "name" in request.args:
    name = request.args["name"]
else:
    name = "world"
```

#### Strategy B: `.get()` with a default

Python dictionaries support `.get(key, default)`. Flask’s `request.args` supports a similar pattern:

```python
name = request.args.get("name", "world")
```

This yields `"world"` if the key does not exist.

### 11.5.2 Passing variables into templates

Flask’s `render_template` accepts named parameters:

```python
return render_template("index.html", name=name)
```

It is common to see `name=name`, which can look redundant, but it is simply “parameter name” on the left and “Python variable value” on the right.

---

## 11.6 Forms as a User Interface for Parameters

Typing query strings into the URL bar is not a realistic user interface. The web’s standard input mechanism is an HTML **form**.

A simple greeting form might look like this:

```html
<form action="/greet" method="get">
  <input name="name" type="text" placeholder="Name" autocomplete="off" autofocus>
  <button type="submit">Greet</button>
</form>
```

When the user submits this form, the browser navigates to:

- `/greet?name=David`

But this introduces a key design point: **if your HTML form’s action points to `/greet`, then your Flask app must implement a `/greet` route**. Otherwise, the browser will show **404 Not Found**, because your server has no code associated with that path.

A common pattern is therefore:

- `/` displays a page containing the form (input)
- `/greet` processes input and displays results (output)

For example:

```python
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return render_template("greet.html", name=name)
```

Where `templates/greet.html` might contain:

```html
hello, {{ name }}
```

---

## 11.7 Avoiding Duplication with Template Inheritance (`layout.html`)

If `index.html` and `greet.html` are both full HTML documents, they will likely share a large amount of boilerplate: doctype, `<html>`, `<head>`, `<title>`, meta viewport, and so on.

Duplicating that boilerplate is a design smell: if you change the title or add CSS, you must update multiple files.

Jinja supports **template inheritance**, commonly organized around a `layout.html` file that defines the shared structure and a named block where each page inserts custom content.

A conventional `templates/layout.html` might include:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>hello</title>
    <meta name="viewport" content="initial-scale=1, width=device-width">
  </head>
  <body>
    {% block body %}{% endblock %}
  </body>
</html>
```

Here, `{% block body %}{% endblock %}` is a Jinja construct that defines a placeholder for a *block* of HTML, not just a single variable.

Then `templates/greet.html` can “extend” the layout:

```html
{% extends "layout.html" %}

{% block body %}
  hello, {{ name }}
{% endblock %}
```

And `templates/index.html` can do the same:

```html
{% extends "layout.html" %}

{% block body %}
  <form action="/greet" method="get">
    <input name="name" placeholder="Name" autocomplete="off" autofocus>
    <button type="submit">Greet</button>
  </form>
{% endblock %}
```

This looks “uglier” at first because it introduces template syntax, but it scales far better: shared page structure lives in one place, while each page contributes only what is unique.

---

## 11.8 POST, Privacy, and `request.form`

Using GET has a property that is sometimes a feature and sometimes a problem:

- The URL becomes **stateful**: you can copy it, paste it, and someone else can reproduce the same page.
- But input appears in the URL, browser history, auto-complete, logs, and screenshots.

For non-sensitive inputs (like a search query), GET is often fine. For sensitive inputs (like passwords or credit card numbers), GET is inappropriate.

The alternative is **POST**, which sends form data in the HTTP request body rather than in the URL.

Changing:

```html
<form method="get">
```

to:

```html
<form method="post">
```

prevents the parameter from appearing in the URL. However, it also changes what your Flask route must support:

- If your route only accepts GET (the default), but the browser sends POST, the server will respond with **405 Method Not Allowed**.

### 11.8.1 Allowing POST with `methods=[...]`

Flask routes accept a `methods` parameter:

```python
@app.route("/greet", methods=["POST"])
def greet():
    ...
```

If a route needs both behaviors—displaying a form (GET) and processing it (POST)—you can support both:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    ...
```

### 11.8.2 Reading POST data with `request.form`

When using GET, form data is available in `request.args`. When using POST, Flask makes it available in `request.form`.

So a POST-based greeting handler might look like:

```python
@app.route("/greet", methods=["POST"])
def greet():
    name = request.form.get("name", "world")
    return render_template("greet.html", name=name)
```

A subtle point arises here: `request.args` and `request.form` are both tied to “form submission” in the human sense, but Flask uses different properties depending on whether the browser used GET or POST.

---

## 11.9 Consolidating Related Functionality into One Route

A small app can afford separate routes for “show form” and “process form,” but as applications grow, doubling the number of routes can become noisy.

A common alternative is to use a single route that behaves differently depending on the request method:

```python
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        return render_template("greet.html", name=name)

    return render_template("index.html")
```

Here:

- GET `/` renders the form.
- POST `/` processes the form submission.

If you make this change, you must also adjust your form’s `action`. If the route is now `/`, then the form should submit to `/` (or omit `action` entirely, which causes the browser to submit to the current page’s route).

---

## 11.10 A Template Bug: Empty Strings and Jinja Conditionals

Even when you provide a default value in `.get("name", "world")`, a form can still submit a key with an **empty value** (the empty string). In that case, the key exists, so your default is not used, and you might display:

- `hello, ` (with nothing after the comma)

One approach is to handle this in the template using Jinja’s control flow:

```html
hello,
{% if name %}
  {{ name }}
{% else %}
  world
{% endif %}
```

In Jinja:

- `{% if ... %}` introduces logic.
- `endif` closes the block.
- A non-empty string is “truthy,” while the empty string is treated as “falsey,” which makes this conditional a natural way to choose between a provided name and a fallback.

This illustrates an important idea: templates are not only for substitution; they can contain lightweight logic such as conditionals (and, as we will see next, loops).

---

## 11.11 Case Study: Frosh IMs Registration (Forms, Validation, and Templates)

A simple “registration” web application is a useful way to synthesize HTML forms, Flask routes, validation, and templates.

### 11.11.1 The registration form: text input + select menu

A registration page might include:

- A name text field
- A sport selector
- A submit button

In HTML, a dropdown menu is a `<select>` element containing `<option>` elements:

```html
<select name="sport">
  <option value="basketball">basketball</option>
  <option value="soccer">soccer</option>
  <option value="ultimate frisbee">ultimate frisbee</option>
</select>
```

A user-experience issue is that the first option is selected by default, which can cause accidental registrations (or bias users toward the first option).

One workaround is to add a placeholder-like option that is selected by default but cannot be chosen afterward:

```html
<select name="sport">
  <option disabled selected value="">Sport</option>
  ...
</select>
```

This is essentially a “hack” to emulate placeholder behavior in a control that does not have a true `placeholder` attribute.

### 11.11.2 Client-side validation with `required` (and why it’s not security)

HTML allows client-side validation, such as requiring a field:

```html
<input name="name" required>
```

This improves user experience, but it is not a security feature. A user can open developer tools, remove `required`, and submit anyway. Therefore:

- Client-side checks are helpful for usability.
- **Server-side validation is mandatory** for correctness and security.

### 11.11.3 Implementing the `/register` route and handling mistakes

If a form uses `method="post"`, the corresponding Flask route must accept POST:

```python
@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name"):
        return render_template("failure.html")

    if not request.form.get("sport"):
        return render_template("failure.html")

    return render_template("success.html")
```

During development, if you forget to return something on some path through your function, Flask will produce a server-side error (often shown in the browser as **500 Internal Server Error**) and the terminal running Flask will show a traceback explaining what went wrong (for example, that your function did not return a valid response).

This is a practical debugging reality of web development: the browser shows you *a status code*, while the terminal often shows you *the actual exception and message*.

### 11.11.4 Better error pages: passing messages into templates

Instead of returning a generic failure page, you can render an error template and pass a specific message:

```python
return render_template("error.html", message="Missing name")
```

Then `error.html` can display:

```html
<p>{{ message }}</p>
```

This pattern mirrors how real sites provide specific feedback when a form submission fails.

---

## 11.12 Never Trust the Client: Validating Allowed Sports Server-Side

Even if your HTML only offers three sports, a user can modify the form in developer tools and submit a different value (for example, “football”). If your server only checks that *some* value exists, bogus values will pass validation.

A robust approach is to maintain an authoritative list of allowed sports in Python and validate against it.

```python
SPORTS = ["basketball", "soccer", "ultimate frisbee"]
```

Then validate:

```python
sport = request.form.get("sport")
if sport not in SPORTS:
    return render_template("error.html", message="Invalid sport")
```

### 11.12.1 Eliminating duplication: generating the select options from the same list

If `SPORTS` is the authoritative list, it is better to generate the dropdown from that list rather than hard-code options in HTML.

In `app.py`:

```python
@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)
```

In `index.html`:

```html
<select name="sport">
  <option disabled selected value="">Sport</option>

  {% for sport in sports %}
    <option value="{{ sport }}">{{ sport }}</option>
  {% endfor %}
</select>
```

Now the same data structure controls:

- What the user can choose (UI)
- What the server will accept (validation)

This dramatically reduces the chance of inconsistencies.

---

## 11.13 Radio Buttons vs. Checkboxes (and Handling Multiple Values)

HTML offers multiple ways to represent choices:

- **Radio buttons** (`type="radio"`) are mutually exclusive: you can choose exactly one.
- **Checkboxes** (`type="checkbox"`) are inclusive: you can choose zero or more.

Using Jinja, you can generate a set of inputs from a list:

```html
{% for sport in sports %}
  <input name="sport" type="radio" value="{{ sport }}"> {{ sport }}
{% endfor %}
```

Changing `radio` to `checkbox` allows multiple sports to be selected:

```html
{% for sport in sports %}
  <input name="sport" type="checkbox" value="{{ sport }}"> {{ sport }}
{% endfor %}
```

However, when multiple checkboxes share the same name, the server receives **multiple values for the same key**. In Flask, `request.form.get("sport")` is no longer appropriate, because it returns only one value.

Instead, you must obtain a list of all submitted values. In Flask, this is done with `getlist`:

```python
sports_selected = request.form.getlist("sport")
```

You can then validate each selected sport:

```python
for sport in request.form.getlist("sport"):
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")
```

A practical lesson lives here as well: frameworks have their own method names and conventions, and it is normal to consult documentation when you need a detail such as “how do I retrieve multiple values for the same field?”

---

## 11.14 Redirects and HTTP 302: Sending the User to Another Route

Often, after processing form data, you do not want to render a page directly; you want to send the user elsewhere (for example, to a list of registrants). In HTTP terms, this is a **redirect**, commonly represented by status code **302 Found**, along with a `Location` header that tells the browser where to go next.

Flask provides a `redirect` function that handles this for you:

```python
from flask import redirect

return redirect("/registrants")
```

In browser developer tools (Network tab), you can often observe:

1. The POST request to `/register` returns `302 Found` with `Location: /registrants`
2. The browser automatically performs a GET request to `/registrants` and receives `200 OK`

This is a standard, intentional two-step sequence that appears throughout the web.

---

## 11.15 Storing Data in Memory vs. Persisting Data with SQL

If you store registrants in a global Python dictionary, you can generate a “registrants” page by iterating over it in a template. But storing important data in memory has serious limitations:

- If the server restarts, the dictionary is cleared.
- If you run multiple server instances, each has its own memory, and users may see inconsistent data.

To keep data across restarts and to support real scale, you persist it to disk, often with a database such as **SQLite**, using **SQL**.

### 11.15.1 A global dictionary approach (in-memory “model”)

A dictionary model might look like:

- keys: user names
- values: sports

```python
registrants = {}
registrants[name] = sport
```

Then a template can iterate and display a table of names and sports.

This works for demonstrations, but it is not durable.

### 11.15.2 A SQLite approach (persistent “model”)

Using the CS50 `SQL` library in Python, you can connect to a database:

```python
from cs50 import SQL

db = SQL("sqlite:///froshims.db")
```

A database might contain a table like:

- `id` (primary key)
- `name`
- `sport`

And registration becomes an insert:

```python
db.execute(
    "INSERT INTO registrants (name, sport) VALUES (?, ?)",
    name,
    sport
)
```

Notice the use of `?` placeholders. This is the same security principle emphasized earlier with SQL injection: you should not build SQL statements by concatenating user input into strings. Placeholders ensure proper escaping.

### 11.15.3 Primary keys and hidden inputs (deregistering)

When you need to delete a row (for example, deregister a registrant), names are not reliable identifiers. Multiple users can share a name, so you rely on the database’s unique identifier: the primary key `id`.

A template can include a small form per row with a hidden input that carries the row’s ID:

```html
<form action="/deregister" method="post">
  <input name="id" type="hidden" value="{{ registrant.id }}">
  <button type="submit">Deregister</button>
</form>
```

Then the Flask route can delete by ID:

```python
@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM registrants WHERE id = ?", id)
    return redirect("/registrants")
```

This “hidden input carrying an opaque identifier” is one of the most common patterns in web applications, because it connects a user interface (names, titles, labels) to a backend that needs a reliable key.

---

## 11.16 MVC: Model, View, Controller

A useful vocabulary for many web applications is **MVC**:

- **Model**: where data is stored (a Python dictionary in memory, or a SQL database, or both)
- **View**: what the user sees (templates, HTML, CSS, JavaScript)
- **Controller**: the application logic that connects input to output (routes and Python code in `app.py`)

You do not need to force every application into MVC, but the pattern describes a large fraction of real systems and provides a shared language for discussing design.

---

## 11.17 Sessions and Cookies: How Sites “Remember” You

HTTP is fundamentally *stateless*: each request can be processed independently. Yet websites “remember” that you are logged in, remember what is in your shopping cart, and keep track of preferences.

The mechanism that enables this is the **cookie**.

### 11.17.1 The `Set-Cookie` and `Cookie` headers

After successful login, a server can include a header like:

- `Set-Cookie: session=...`

This instructs the browser to store a key–value pair (a “hand stamp”). On subsequent requests, the browser sends:

- `Cookie: session=...`

so the server can recognize that this browser has an existing session.

A cookie value is typically a large random identifier; it generally does **not** contain the user’s password, and it often does not contain the username either. Instead, the cookie acts as a token that allows the server to look up the user’s state (login status, shopping cart contents) in server-side storage.

Cookies have privacy implications because they can also be used for tracking, but they are also the standard building block for stateful web applications.

---

## 11.18 Using Sessions in Flask (`flask_session`)

Flask provides session support, and a commonly used extension is `flask_session`, which helps store session data server-side.

A typical configuration includes:

```python
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
```

This configuration aims to:

- treat the session as not permanent (often cleared when the browser closes), and
- store session contents on the server’s filesystem rather than inside the cookie itself.

### 11.18.1 A minimal login system (name only)

A login route commonly supports:

- GET: display the login form
- POST: process the login form

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")
```

Then the homepage can check whether a name exists in the session:

```python
@app.route("/")
def index():
    name = session.get("name")
    return render_template("index.html", name=name)
```

And the template can conditionally display different content:

```html
{% if name %}
  You are logged in as {{ name }}.
  <a href="/logout">Log out</a>
{% else %}
  You are not logged in.
  <a href="/login">Log in</a>
{% endif %}
```

### 11.18.2 Logging out by clearing the session

To log out, you clear the session and redirect:

```python
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
```

This is the same basic idea used by many real websites: logging out does not “undo” HTTP, but it invalidates or clears the state associated with the cookie’s session identifier.

---

## 11.19 A Shopping Cart: Sessions + Lists + Databases

A shopping cart is just a specific kind of session state: a per-user collection of items.

A typical pattern is:

- Store a list of item IDs in `session["cart"]`
- When displaying the cart, query the database for those IDs
- Render them in a template

For example, when adding an item:

```python
if "cart" not in session:
    session["cart"] = []

id = request.form.get("id")
if id:
    session["cart"].append(id)
```

When displaying the cart, you might select all books whose IDs are in that list. Some libraries support passing a list as a placeholder so it can expand to a comma-separated list safely, rather than constructing SQL manually.

This demonstrates a broader theme: once you understand forms, routes, templates, sessions, and SQL, you can recognize many “big” applications as combinations of these small ideas.

---

## 11.20 Search and SQL Wildcards: Building an IMDb-like Query

A search feature often begins with:

- a form that sends `q=...`
- a route that queries a database
- a template that displays matching rows

A basic equality search might be too strict:

```sql
SELECT * FROM shows WHERE title = ?
```

It will only match exact titles.

To support partial matching, SQL provides `LIKE` with wildcards, typically `%`:

- `%office%` matches any title containing `office` anywhere.

To do this safely, you still use placeholders, but you build the wildcard string in Python:

```python
q = request.args.get("q", "")
shows = db.execute(
    "SELECT * FROM shows WHERE title LIKE ?",
    "%" + q + "%"
)
```

This preserves the security benefit of placeholders while still enabling wildcard search.

---

## 11.21 AJAX, `fetch`, and APIs: Updating a Page Without Reloading

Traditional web apps often work by:

1. user submits a form
2. browser navigates to a new page
3. server generates and returns a full HTML document

Modern apps increasingly update parts of the page without full reloads. A classic term for this approach is **AJAX** (originally “Asynchronous JavaScript And XML”), though today it usually just means “JavaScript makes background HTTP requests.”

### 11.21.1 A dynamic search box that updates as you type

Instead of a form with a submit button, you can use:

- an `<input>` box
- an empty `<ul>` list
- JavaScript that listens to typing and fetches results

A conceptual flow is:

1. Listen for an input event
2. Request `/search?q=...`
3. Receive response data
4. Insert response into the page (DOM manipulation)

A simplified pattern looks like:

```js
let input = document.querySelector("input");

input.addEventListener("input", async function () {
  let response = await fetch("/search?q=" + input.value);
  let text = await response.text();
  document.querySelector("ul").innerHTML = text;
});
```

If the server returns HTML fragments (like a set of `<li>` elements), `innerHTML` can drop them into the existing `<ul>`.

Browser developer tools (Network tab) reveal what is happening: each keystroke can trigger an HTTP request, even though the URL in the address bar does not change and the whole page does not reload.

### 11.21.2 JSON as a more standard API format

Returning HTML fragments works, but it is not the most standardized way to exchange data between programs. A more common modern approach is to return **JSON** (JavaScript Object Notation), which resembles Python lists and dictionaries but follows strict rules such as using double quotes for strings.

Flask can convert Python data structures to JSON with `jsonify`:

```python
from flask import jsonify

@app.route("/search")
def search():
    q = request.args.get("q", "")
    shows = db.execute(
        "SELECT * FROM shows WHERE title LIKE ?",
        "%" + q + "%"
    )
    return jsonify(shows)
```

Now the server’s response is structured data rather than HTML. A front end can then generate its own HTML from that JSON, or use it in other ways. This separation—where the backend provides an API and the frontend consumes it—is increasingly common in large applications, and it is also the conceptual bridge to using third-party APIs (where the server you are querying belongs to someone else).

---

## 11.22 Summary

Flask provides a practical way to synthesize many of the web concepts introduced earlier—HTTP methods, routes, forms, templates, databases, and JavaScript—into complete applications.

Key ideas from this chapter include:

- A **route** is a path like `/greet` or `/search` that maps to code, not necessarily a file.
- `render_template` returns HTML from `templates/`, enabling dynamic generation of web pages.
- `request.args` contains GET parameters (query string); `request.form` contains POSTed form data.
- GET is **visible in the URL** and therefore stateful and shareable, but inappropriate for sensitive input; POST hides data from the URL.
- Flask routes must explicitly support POST using `methods=[...]`, otherwise you will see **405 Method Not Allowed**.
- Jinja supports:
  - variable interpolation with `{{ ... }}`
  - control flow with `{% if %}`, `{% for %}`, and their corresponding endings
  - template inheritance with `layout.html`, `{% block %}`, and `{% extends %}`
- Client-side validation (like `required`) improves user experience but is not security; **server-side validation is essential**.
- **Redirects** are commonly implemented with HTTP **302** and a `Location` header; Flask’s `redirect` automates this.
- Persisting data with **SQL** and a database (instead of Python globals) avoids losing data when the server restarts.
- Primary keys and hidden form fields (`<input type="hidden">`) are a standard way to connect UI elements to database rows.
- **Sessions** and **cookies** implement “memory” across requests; Flask’s session support makes per-user state (logins, carts) tractable.
- Modern “no reload” interfaces use JavaScript `fetch` (AJAX-style) to call server endpoints repeatedly and update the DOM dynamically.
- APIs often return **JSON**, and Flask’s `jsonify` helps turn Python data into that standardized format.

With these pieces, you can recognize the structure underneath many familiar systems—from registration sites to shopping carts, from login flows to search engines—and you can begin building your own applications that combine Python logic, HTML templates, SQL persistence, and responsive browser-based interfaces.