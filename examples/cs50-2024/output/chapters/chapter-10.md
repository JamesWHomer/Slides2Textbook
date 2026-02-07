# Chapter 10: The Web — Building on the Internet with HTML, CSS, and JavaScript

Modern software rarely lives in isolation on a single machine. Even when you are “just using an app,” that app is usually exchanging data with services across the network, retrieving information from servers, and updating interfaces dynamically based on what it receives. This chapter introduces the foundational ideas and tools that make that possible: the Internet as a packet-switched network, the Web as a protocol layered on top of it, and the three core languages that most browsers understand—**HTML**, **CSS**, and **JavaScript**.

Two of these languages, HTML and CSS, are primarily about *presentation*: describing the structure of a page and how it should look. The third, JavaScript, is a real programming language, used to make web pages interactive by allowing code to react to user events and modify the page dynamically.

To build confidently on top of the Web, it helps to begin with the underlying plumbing. Many of the details you have been taking for granted—addresses, routers, ports, status codes, and URLs—turn out to be practical tools for debugging and for reasoning about how your own software behaves.

---

## 10.1 The Internet: Packets, Routers, and “Protocols”

At a high level, the Internet is a collection of interconnected networks that allows computers to exchange data. Historically, it began as a small experimental network called **ARPANET** in the late 1960s and 1970s. The key technical idea that scaled from “a few computers” to “the entire world” is that information is broken into small chunks called **packets**, and those packets are routed independently across a mesh of intermediate machines.

### 10.1.1 Routers: the computers whose job is to forward traffic

A **router** is a device (in practice, a specialized computer) whose purpose is to forward packets toward their destinations. When you send data to a friend across the country, or request a web page from a server, your computer typically does **not** have a direct connection to the other computer. Instead, your data passes through a sequence of routers—often more than a handful, but typically fewer than a few dozen.

A crucial design feature of the Internet is that packets can take **different paths**. Even if two computers communicate repeatedly, the packets might not all travel the same route, because routers can adapt to failures, congestion, or changes in network conditions. This ability to “route around” problems is not an accident; it is a core robustness property.

### 10.1.2 Packets: digital “envelopes”

A **packet** is a unit of transmitted information, and it is helpful to think of it as analogous to a physical envelope:

- The **outside** of the envelope contains addressing information so the network knows where to send it.
- The **inside** contains the content (the message, part of a file, part of a web page, and so on).

The Internet is largely built out of agreed-upon rules about what goes on the outside and inside of these envelopes. Those agreed-upon rules are called **protocols**.

### 10.1.3 Protocols: standardized rules for communication

A **protocol** is a shared convention that both sides understand. In everyday life, a handshake is a protocol: one person initiates, the other responds, and both agree on what the motions mean. Computer protocols work the same way: a **client** initiates, a **server** responds, and both follow a standard format so they can interpret each other correctly.

Two especially important Internet protocols are commonly used together as **TCP/IP**:

- **IP** (Internet Protocol): addressing and routing
- **TCP** (Transmission Control Protocol): reliability and ports (service identification)

---

## 10.2 IP: Addressing Computers on the Internet

### 10.2.1 IP addresses as “street addresses” for computers

To deliver a packet, the Internet needs addresses. An **IP address** identifies a destination machine (or, more precisely, a network interface).

A commonly seen format is:

```
number.number.number.number
```

For example:

```
1.2.3.4
```

This is an **IPv4** address (Internet Protocol version 4). Each of the four numbers is between **0 and 255**, which means each number fits in **8 bits** (one byte). Four bytes total means IPv4 addresses are **32 bits**, which yields about \(2^{32}\) possible addresses—roughly **4 billion**.

In modern life, with billions of humans and multiple devices per human (phones, laptops, tablets, servers, “internet of things” devices), 4 billion addresses is not enough. The Internet is therefore gradually transitioning to **IPv6**, which uses **128 bits**, yielding \(2^{128}\) possible addresses. IPv6 addresses are much longer and less human-friendly, so IPv4 remains a useful mental model even as the world migrates.

### 10.2.2 Source and destination: what IP contributes to packets

When a packet is sent, the outside must at least include:

- the **source address** (where the packet came from), and
- the **destination address** (where it is going).

This is what IP standardizes: how those addresses are represented, and how routers should forward packets to move them closer to their destination.

### 10.2.3 IP alone does not guarantee delivery

Even though IP can route packets, it does not guarantee that a packet arrives. Routers can drop packets if they are overloaded or if they run out of memory to buffer incoming traffic. In other words, the network can lose envelopes.

This is where TCP enters the picture.

---

## 10.3 TCP: Reliability and Port Numbers

**TCP** is layered on top of IP and provides two crucial services for many kinds of Internet communication.

### 10.3.1 Sequence numbers: supporting “guaranteed” delivery

If a message is large, it may be split across many packets. TCP adds **sequence numbers** so the receiver can detect missing packets and request retransmission.

You can think of this as writing “1 of 2” and “2 of 2” on envelopes. Real TCP sequence numbers are much larger than this toy example because connections may involve thousands or millions of packets, but the core idea is the same: number the pieces so they can be reassembled reliably.

TCP therefore aims to provide *reliable* communication, even though the underlying network might drop packets.

### 10.3.2 Ports: one computer, many services

A single machine might run multiple services:

- a web server,
- an email server,
- a chat server,
- a video conferencing service,
- and so on.

Even if packets arrive at the correct **IP address**, the machine still needs to know *which program* should receive them. TCP solves this with **port numbers**.

A **port** is a numeric identifier for a service on a machine. Two especially common ports are:

- **80** for HTTP (web traffic)
- **443** for HTTPS (web traffic over encryption)

Port numbers are not mathematically special; they are conventions that humans standardized long ago.

When you access a web server, your packets are addressed not only to an IP address, but also to a port—conceptually “IP address : port”.

---

## 10.4 DNS: Translating Domain Names to IP Addresses

Humans do not like typing IP addresses. We prefer names like:

- `harvard.edu`
- `yale.edu`
- `google.com`

These are **domain names**, and computers must translate them into numeric IP addresses before sending packets. That translation is performed by **DNS**: the **Domain Name System**.

### 10.4.1 DNS servers as a global dictionary

A **DNS server** is a server whose job is to answer questions of the form:

> What is the IP address for this domain name?

You can think of DNS as a globally distributed dictionary (similar in spirit to a hash table):

| Domain name      | IP address      |
|------------------|-----------------|
| harvard.edu      | …               |
| google.com       | …               |

DNS is **hierarchical**. Your computer typically asks a nearby DNS server (often operated by your ISP, your university, or your company). If that server does not know the answer, it asks other DNS servers “higher up” in the hierarchy, eventually reaching **root servers** that coordinate knowledge about top-level domains like `.com`, `.edu`, and country-code domains.

### 10.4.2 Hostnames, top-level domains, and fully qualified domain names

In a URL like:

- `www.example.com`

you can distinguish:

- `www` as a **hostname** (a conventional label for a particular server or role),
- `example` as the organization’s domain, and
- `.com` as the **top-level domain (TLD)**.

Historically, `www.` was used to signal “this is a web address,” but it is increasingly common for sites to omit it (e.g., `cs50.dev`, `cs50.ai`). Whether a site uses `www` is largely a configuration and branding choice; either can be redirected to the other.

---

## 10.5 DHCP: Automatically Configuring Devices

In early networking, a person might manually configure a computer’s network settings: which IP address to use, which DNS server to ask, and which router to send packets to. Today, most configuration happens automatically through **DHCP**: the **Dynamic Host Configuration Protocol**.

A **DHCP server** answers questions like:

- “What IP address should I use on this local network?”
- “What is my DNS server?”
- “What is my default router (gateway)?”

When you open your laptop or connect your phone to a network, your device broadcasts a request, and a nearby DHCP server replies with the configuration it should use.

---

## 10.6 HTTP and HTTPS: The Web as a Protocol

The **World Wide Web** is built on **HTTP**: the **Hypertext Transfer Protocol**. HTTP is one more protocol layered on top of TCP/IP, but this time it standardizes what goes *inside* the packets to allow a browser (the client) and a web server to communicate.

### 10.6.1 HTTP vs. HTTPS

- **HTTP** is plain text: if someone can intercept your packets, they can read the contents.
- **HTTPS** is HTTP over encryption: traffic is scrambled using cryptography so that interception does not reveal the message contents in any practical way.

This is why HTTPS is used for logins, payments, and increasingly for essentially all web traffic.

### 10.6.2 URLs: the parts of a web address

A canonical URL looks like:

```
https://www.example.com/folder/file.html
```

Key components include:

- **Scheme / protocol**: `https` (or `http`)
- **Hostname and domain**: `www.example.com`
- **Path**: `/folder/file.html`

The path often corresponds conceptually to a file or folder on the server, though modern servers often hide file extensions (`.html`) for cleaner URLs.

A URL can also include a **query string** (discussed later), which begins with `?` and contains key–value pairs.

---

## 10.7 GET and POST: Two Common Ways to Make Requests

HTTP supports multiple request “methods,” but two of the most important are:

- **GET**: request information (the common method when clicking links and visiting pages)
- **POST**: submit information (common for forms that send data such as passwords, uploads, or payment details)

For much of this chapter, GET is sufficient, because we are learning the mechanics of requesting pages and sending simple form inputs.

---

## 10.8 HTTP Messages: Requests, Responses, Headers, and Status Codes

When you type a URL into a browser and press Enter, your browser sends an HTTP **request** message to the server. The server sends back an HTTP **response** message.

### 10.8.1 A simple HTTP request

A request resembles:

```text
GET / HTTP/2
Host: www.harvard.edu
...
```

Important parts:

- `GET` is the method.
- `/` is the path (the “default” page at the root).
- `HTTP/2` is the protocol version (you may also see `HTTP/1.1` and increasingly HTTP/3).
- `Host: ...` is a **header**, a key–value line that helps the server understand what the client wants.

The `Host` header matters because a single physical server can host multiple websites. The host header lets the server know which site’s content to return.

### 10.8.2 A simple HTTP response

A response resembles:

```text
HTTP/2 200 OK
Content-Type: text/html
...
```

Important parts:

- `200` is a **status code** indicating success.
- `Content-Type: text/html` tells the browser what kind of content it received (here, HTML).

### 10.8.3 Inspecting HTTP with `curl`

A convenient command-line tool for observing HTTP responses is `curl`. For example:

```bash
curl -I https://www.harvard.edu/
```

The `-I` flag requests only headers (not the full page content), making it easier to focus on status codes and metadata.

### 10.8.4 Browser Developer Tools: Network inspection

Modern browsers include **developer tools**, often with a **Network** tab that shows every HTTP request made while loading a page. This is useful because loading a single page typically triggers dozens of requests: the initial HTML plus images, CSS files, JavaScript files, fonts, and more.

### 10.8.5 Status codes: what the numbers mean

HTTP status codes communicate what happened. Common examples include:

- **200 OK**: the request succeeded.
- **301 Moved Permanently**: the server is redirecting you to a new URL.
  - For example, visiting `https://harvard.edu/` might redirect to `https://www.harvard.edu/`.
- **404 Not Found**: the requested path does not exist on the server.
- **403 Forbidden**: you are not allowed to access the resource (often due to missing authentication).
- **500 Internal Server Error**: the server encountered a bug or misconfiguration (a “server-side failure,” often analogous in spirit to “something crashed”).
- **418 I’m a teapot**: an April Fool’s joke status code that exists as a piece of internet folklore; some servers may still recognize it.

Status codes beginning with:

- **3xx** often relate to redirection,
- **4xx** generally indicate a client-side problem (bad request, forbidden, not found),
- **5xx** generally indicate a server-side problem.

---

## 10.9 HTML: Structuring Web Pages with Tags and Attributes

**HTML** (Hypertext Markup Language) is a **markup language**, not a general-purpose programming language. It describes the *structure* of a document: headings, paragraphs, lists, tables, links, forms, and so on.

HTML is built from two core ideas:

- **Tags** (like `<p>` or `<title>`)
- **Attributes** (like `lang="en"` or `href="https://..."`)

### 10.9.1 A minimal HTML page

A simple example:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>hello, title</title>
  </head>
  <body>
    hello, body
  </body>
</html>
```

Key concepts:

- `<!DOCTYPE html>` is the **document type declaration**, typically copied and pasted; it signals modern HTML (HTML5).
- `<html lang="en">` begins the HTML document and declares the language of the page content.
- `<head>` contains metadata such as the `<title>`.
- `<body>` contains the main visible content in the viewport.

An **attribute** is written as `key="value"`. The language of HTML heavily uses key–value pairs, but with syntax different from other languages.

Many tags come in pairs:

- an opening tag: `<title>`
- a closing tag: `</title>`

The content between them forms an **element**.

### 10.9.2 Running a local web server in a development environment

If your HTML file lives locally on your computer, you can often open it directly by double-clicking it. In a cloud development environment (such as a hosted code space), you typically run a web server to serve files to your browser.

A simple development server is:

```bash
http-server
```

This starts a server that listens for HTTP requests. In many setups, it uses port **8080** by default (instead of 80 or 443), because those standard ports are often already in use or restricted.

When you visit the server’s URL, you may see a **directory listing**, which is simply a web page showing files in the current folder. Clicking a file like `hello.html` causes the browser to request it, and the server responds with that file’s contents.

### 10.9.3 HTML ignores most whitespace

A common surprise is that extra newlines and spaces in HTML do not necessarily appear on the page. HTML generally **collapses sequences of whitespace** into a single space. This is why writing three “paragraphs” separated only by blank lines still looks like one continuous block.

To create actual paragraphs, you use the paragraph tag:

```html
<p>First paragraph...</p>
<p>Second paragraph...</p>
<p>Third paragraph...</p>
```

---

## 10.10 Common HTML Elements: Headings, Lists, Tables, Images, Video, Links

HTML provides many tags. A few appear constantly in real pages.

### 10.10.1 Headings: `<h1>` through `<h6>`

Headings provide structure and default styling:

```html
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
```

`<h1>` is the largest by default, and sizes decrease through `<h6>`.

### 10.10.2 Lists: unordered and ordered

An **unordered list** uses `<ul>` with list items `<li>`:

```html
<ul>
  <li>foo</li>
  <li>bar</li>
  <li>baz</li>
</ul>
```

An **ordered list** uses `<ol>`:

```html
<ol>
  <li>foo</li>
  <li>bar</li>
  <li>baz</li>
</ol>
```

The browser handles numbering automatically, which is useful if you insert items in the middle.

### 10.10.3 Tables: rows and cells

A basic table uses:

- `<table>` as the container
- `<tr>` for table rows
- `<td>` for data cells

For example, a numeric keypad layout can be represented by rows and cells. For more structured tables (like a phonebook), HTML often distinguishes:

- `<thead>` for the header section
- `<tbody>` for the data section

This is especially useful for styling and semantics.

### 10.10.4 Images: `<img>` with `src` and accessibility via `alt`

An image tag includes a source file:

```html
<img src="bridge.png" alt="Photo of bridge">
```

Two key attributes:

- `src`: which image file to load
- `alt`: **alternative text** used by screen readers and displayed if the image fails to load

Including `alt` text is a best practice for accessibility.

### 10.10.5 Video: `<video>` and `<source>`

Embedding video looks like:

```html
<video controls muted>
  <source src="video.mp4" type="video/mp4">
</video>
```

Notable details:

- Some attributes (like `controls` and `muted`) are **boolean attributes**: they do not need `= "true"`; the presence of the word enables the feature.
- The `type` attribute uses a MIME/content-type style string such as `video/mp4`.

### 10.10.6 Links: the anchor tag `<a>`

A hyperlink uses the **anchor** tag:

```html
<a href="https://www.harvard.edu/">Harvard</a>
```

The human-visible text does not have to match the `href`. This flexibility powers ordinary web design, but it also enables **phishing**: displaying a trustworthy-looking URL while linking somewhere else.

---

## 10.11 Metadata: `<meta>` Tags for Mobile and Link Previews

The `<head>` of a page can contain metadata beyond the title.

### 10.11.1 Mobile-friendly viewport settings

A common meta tag for mobile friendliness is:

```html
<meta name="viewport" content="initial-scale=1, width=device-width">
```

This helps the browser scale content appropriately on phones and tablets.

### 10.11.2 Social media link previews (“Open Graph” style metadata)

Web pages can include metadata that social platforms use to generate rich previews when a link is pasted. Such tags specify:

- the title shown in the preview,
- a short description,
- and an image.

This gives the page author control over how the page appears when shared.

---

## 10.12 Forms and Query Strings: Sending Input with GET

A **form** is the basic HTML mechanism for collecting user input and sending it to a server.

### 10.12.1 A search form that sends data to Google

A simplified version:

```html
<form action="https://www.google.com/search" method="get">
  <input name="q" type="search" placeholder="query" autocomplete="off" autofocus>
  <input type="submit" value="Google Search">
</form>
```

Important ideas:

- `action` is the URL that will receive the form submission.
- `method="get"` means the browser will encode the form input into the URL’s query string.
- The input’s `name` is the **key** used in the query string. Google expects the key `q`.

If the user types `cats`, the resulting request URL becomes:

```
https://www.google.com/search?q=cats
```

### 10.12.2 Query strings as key–value pairs

A query string starts with `?` and contains `key=value` pairs. Multiple pairs are separated with `&`, such as:

```
/search?q=cats&lang=en
```

This is a simple but powerful web convention: it is one of the primary ways data is passed from a browser to a server using GET.

### 10.12.3 Useful input attributes: `placeholder`, `autocomplete`, `autofocus`, and `type`

- `placeholder` shows hint text in the input before typing.
- `autocomplete="off"` disables the browser’s suggestions (useful sometimes, though often autocomplete is user-friendly).
- `autofocus` places the cursor in the field automatically.
- `type` influences validation and user experience:
  - `type="text"` (default)
  - `type="search"` (may add features like a clear “x” in some browsers)
  - `type="email"` (asks the browser to enforce an email-like format)

---

## 10.13 Client-Side Validation and Regular Expressions (Regex)

Browsers can validate input before sending it to a server, which can improve user experience by catching mistakes early.

### 10.13.1 Email validation with `type="email"`

If you use:

```html
<input type="email">
```

most browsers will reject submissions that lack an `@` or otherwise clearly fail to resemble an email address.

### 10.13.2 Restricting formats with `pattern=...`

You can add a `pattern` attribute containing a **regular expression** (regex). For example, to require an address ending in `.edu`:

```html
<input
  name="email"
  type="email"
  placeholder="email"
  pattern=".+@.+\.edu"
  autocomplete="off"
  autofocus
>
```

A few regex building blocks used here:

- `.` matches (almost) any single character
- `+` means “one or more occurrences”
- `\.` escapes a dot so it means a literal period instead of “any character”

So `.+@.+\.edu` roughly means:

- one or more characters,
- then an `@`,
- then one or more characters,
- then a literal `.edu`.

Real email validation is more complicated than this; full email regexes can become long and intimidating. The important takeaway is that regex is a powerful pattern language for matching and validating strings.

### 10.13.3 Why client-side validation is not security

Client-side validation is **not trustworthy** as a security measure, because the user controls their browser. Browser developer tools allow a user to:

- inspect the HTML and CSS,
- edit the page locally,
- remove attributes like `pattern`,
- and then submit values that the original HTML tried to reject.

Client-side validation is best understood as:

- good for user experience,
- not sufficient for enforcing rules or protecting systems.

Server-side checks are still required to ensure correctness and security.

### 10.13.4 Validating HTML syntax with the W3C validator

To check whether your HTML is syntactically valid, a widely used tool is the W3C validator:

- `https://validator.w3.org`

It can analyze HTML you paste, upload, or point to by URL, and report errors and warnings.

---

## 10.14 CSS: Making Pages Look Better (and More Consistent)

**CSS** stands for **Cascading Style Sheets**. CSS controls presentation: font sizes, colors, spacing, alignment, borders, layout, and more.

In CSS you again see key–value pairs, but in a different syntax:

```css
property: value;
```

CSS is applied by selecting HTML elements (or groups of elements) and attaching properties to them.

### 10.14.1 Inline styles: the `style="..."` attribute

You can attach CSS directly to an element:

```html
<p style="font-size: large; text-align: center;">John Harvard</p>
```

This works, but it tends to produce repetition and clutter in larger projects.

### 10.14.2 Cascading: applying styles to parents affects children

Rather than centering each element individually, you can center everything inside `<body>`:

```html
<body style="text-align: center;">
  ...
</body>
```

This illustrates the “cascading” idea: styles applied to a parent often flow down to its children.

### 10.14.3 Semantic HTML tags: `<header>`, `<main>`, `<footer>`

HTML5 includes tags that communicate meaning:

```html
<header>John Harvard</header>
<main>Welcome to my homepage!</main>
<footer>&copy; John Harvard</footer>
```

These tags may not change appearance by themselves, but they improve semantics for:

- search engines (SEO),
- screen readers (accessibility),
- and developers reading the code.

The copyright symbol can be written using an **HTML entity**, such as:

```html
&copy;
```

(One way to represent it is by numeric entities as well, e.g., a code corresponding to the copyright symbol.)

### 10.14.4 Style blocks: using `<style>` in the head

Instead of inline styles, you can put CSS in a `<style>` tag:

```html
<head>
  <style>
    body { text-align: center; }
    header { font-size: large; }
    main { font-size: medium; }
    footer { font-size: small; }
  </style>
</head>
```

This separates content (HTML) from presentation (CSS), improving readability and maintainability.

### 10.14.5 Classes: reusable groups of properties

You can define reusable class-based styles:

```css
.centered { text-align: center; }
.large { font-size: large; }
.medium { font-size: medium; }
.small { font-size: small; }
```

…and apply them in HTML with the `class` attribute:

```html
<body class="centered">
  <header class="large">John Harvard</header>
  <main class="medium">Welcome to my homepage!</main>
  <footer class="small">&copy; John Harvard</footer>
</body>
```

A **class selector** begins with a dot (`.`) in CSS.

### 10.14.6 IDs: selecting a unique element

Sometimes you want to style one specific element. You can give it an `id`:

```html
<a id="harvard" href="https://www.harvard.edu/">Harvard</a>
<a id="yale" href="https://www.yale.edu/">Yale</a>
```

Then style by ID:

```css
#harvard { color: red; }
#yale { color: blue; }
```

An **ID selector** begins with a hash (`#`) in CSS.

### 10.14.7 Pseudo-classes: styling states like `:hover`

CSS can select not just elements but *states*. For example, to remove underlining by default but show it on hover:

```css
a { text-decoration: none; }
a:hover { text-decoration: underline; }
```

This is common on desktop sites, where a mouse cursor can hover. It is less meaningful on mobile devices.

### 10.14.8 External style sheets: linking a `.css` file

For larger projects, CSS is commonly placed in a separate file, such as `home.css`, and linked:

```html
<link href="home.css" rel="stylesheet">
```

This enables reusing a single style sheet across many pages and collaborating more cleanly (one person can focus on HTML content while another focuses on CSS design).

### 10.14.9 Using third-party CSS frameworks: Bootstrap

Writing good CSS can take time, and many common interface patterns have already been solved by others. **Bootstrap** is a popular CSS framework that provides a large set of predefined classes.

A page can include Bootstrap by linking to its CSS:

```html
<link
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
  rel="stylesheet"
>
```

Then, HTML elements can be given Bootstrap classes, such as:

- `btn` and `btn-light` for buttons
- table-related classes for styled tables

For example, a search page can look significantly more polished by applying Bootstrap classes rather than writing custom CSS from scratch. The conceptual pattern is the same as your own `.centered` or `.large` classes—Bootstrap simply provides many more of them, along with careful design choices.

### 10.14.10 Learning from real sites via developer tools

Browser developer tools often show the CSS rules currently applied to an element and where they came from. This makes it possible to:

- experiment with style changes live (locally in your browser),
- discover which CSS rules affect a specific element,
- and trace a computed value back to the relevant style sheet rule.

---

## 10.15 JavaScript: Programming in the Browser

**JavaScript** is a full programming language that runs in the browser (and can also run on servers). In the browser, JavaScript’s most prominent role is to make pages interactive by:

- responding to user actions (clicks, typing, submissions),
- reading and modifying the HTML structure of the page, and
- changing styles dynamically.

### 10.15.1 The DOM: the page as a tree in memory

When the browser parses HTML, it builds an internal tree representation called the **DOM**: the **Document Object Model**. You can think of it as the in-memory version of the HTML structure (a tree of nodes: elements and text).

JavaScript can query and manipulate this tree, which is why many modern web apps can update dynamically without a full page reload.

### 10.15.2 Script tags and functions

JavaScript is embedded using a `<script>` tag:

```html
<script>
  function greet() {
    alert("hello, " + document.querySelector("#name").value);
  }
</script>
```

A few key ideas appear here:

- JavaScript defines functions with the keyword `function`.
- The browser provides an `alert(...)` function that shows a pop-up.
- `document.querySelector(...)` selects an element from the DOM using a CSS-like selector.
  - `#name` refers to an element with `id="name"`.
- `.value` retrieves the value of an input element.

### 10.15.3 Responding to form submission: `onsubmit` (inline) vs event listeners

One way to handle a form submit is to put JavaScript directly in HTML:

```html
<form onsubmit="greet(); return false;">
  <input id="name" autocomplete="off" autofocus>
  <input type="submit">
</form>
```

Here, `return false` prevents the browser from performing the form’s default submission behavior (which would usually send a request and reload/navigate).

However, mixing JavaScript into HTML attributes is often avoided in larger codebases. A more typical approach is to attach an event listener in JavaScript:

```html
<script>
  document.querySelector("form").addEventListener("submit", function (event) {
    alert("hello, " + document.querySelector("#name").value);
    event.preventDefault();
  });
</script>
```

Key ideas:

- `addEventListener("submit", ...)` tells the browser what code to run when the event happens.
- `event.preventDefault()` prevents the default form submission.

### 10.15.4 Waiting for the DOM to load: `DOMContentLoaded`

Sometimes you want to ensure the page has been fully parsed into the DOM before running code. Browsers provide a `DOMContentLoaded` event:

```html
<script>
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("form").addEventListener("submit", function (event) {
      alert("hello, " + document.querySelector("#name").value);
      event.preventDefault();
    });
  });
</script>
```

This pattern ensures the relevant elements exist before JavaScript tries to select them.

---

## 10.16 JavaScript and CSS Together: Dynamic Styling

JavaScript can change CSS properties by modifying an element’s `style` object. A simple demonstration is changing the page’s background color in response to button clicks.

### 10.16.1 Buttons that change the background color

HTML might include:

```html
<button id="red">R</button>
<button id="green">G</button>
<button id="blue">B</button>
```

JavaScript might do:

```js
let body = document.querySelector("body");

document.querySelector("#red").addEventListener("click", function () {
  body.style.backgroundColor = "red";
});

document.querySelector("#green").addEventListener("click", function () {
  body.style.backgroundColor = "green";
});

document.querySelector("#blue").addEventListener("click", function () {
  body.style.backgroundColor = "blue";
});
```

Notice the CSS property name changes form:

- In CSS: `background-color`
- In JavaScript: `backgroundColor`

The hyphen would otherwise be interpreted as subtraction in JavaScript, so the convention is to use **camelCase** for such property names.

Developer tools can show these style changes occurring live, which is valuable for understanding and debugging dynamic behavior.

---

## 10.17 Timers and Effects: Recreating “Blink” with `setInterval`

Even if a feature is not built into HTML as a tag, JavaScript can recreate effects by manipulating styles over time.

A “blink” effect can be created by toggling `visibility` repeatedly:

- `visible`
- `hidden`

A timer can be scheduled with:

```js
window.setInterval(blink, 500);
```

This calls the function `blink` every 500 milliseconds. A subtle but important point is that you pass the *function name* (a reference to the function), not the result of calling it. That is why you write `blink`, not `blink()`.

---

## 10.18 Autocomplete: Updating the DOM in Response to Typing

Many modern interfaces react immediately to user input. Autocomplete is one example: as the user types, a list of suggestions updates.

A common pattern involves:

- listening for keyboard events such as `keyup`,
- filtering a list of possible words,
- and dynamically generating list items (`<li>`) inside an existing `<ul>`.

A JavaScript program can build a string of HTML and then insert it into the DOM using something like an element’s `innerHTML`. In effect, JavaScript is generating new HTML “on the fly,” updating the in-memory DOM tree so the page changes without a reload.

This technique is powerful, but it also demands careful design in real systems, because generating HTML dynamically has security implications if user-provided data is inserted unsafely. (The broader theme is the same as earlier: input is tricky, and trust boundaries matter.)

---

## 10.19 Geolocation: Browser APIs and Privacy Implications

Browsers provide powerful APIs beyond HTML and CSS. One striking example is **geolocation**. If a user grants permission (and has location services enabled), JavaScript can obtain the user’s approximate latitude and longitude with a browser-provided object:

- `navigator.geolocation.getCurrentPosition(...)`

This enables applications like ride-sharing and maps, but it also illustrates an important reality: client-side code can access sensitive information if users allow it, and developers have a responsibility to understand both the functionality and the privacy implications of what they build.

---

## 10.20 Summary: From Packets to Pages

This chapter connected the Web’s surface-level experience—typing URLs, clicking links, submitting forms—to the deeper mechanisms that make it work.

Key ideas include:

- **Packet routing** through **routers**, enabling robust communication even when paths change.
- **TCP/IP** as the foundational pair of protocols:
  - **IP** for addressing and routing via IP addresses,
  - **TCP** for reliability (sequence numbers) and service targeting (ports like 80 and 443).
- **DNS** as a distributed naming system translating domain names into IP addresses.
- **DHCP** as the protocol that configures devices automatically with network settings.
- **HTTP/HTTPS** as the web’s application protocol, including:
  - requests and responses,
  - headers,
  - status codes like 200, 301, 404, and 500,
  - diagnostic tooling via `curl` and browser developer tools.
- **HTML** as a markup language for document structure, including tags, attributes, and common elements like paragraphs, headings, lists, tables, images, video, and links.
- **Forms** and **query strings** as a simple but central mechanism for sending input to servers via GET.
- **Regular expressions** via the `pattern` attribute for client-side validation, paired with the crucial warning that **client-side checks are not security** because users can modify HTML locally.
- **CSS** as a styling language with selectors, properties, cascading behavior, classes, IDs, pseudo-classes like `:hover`, external style sheets, and frameworks like **Bootstrap**.
- **JavaScript** as the browser’s programming language, enabling event-driven interactivity, DOM manipulation, dynamic styling, timers, autocomplete behavior, and access to browser APIs like geolocation.

With these foundations in place, you are prepared to start building software that feels like “real” modern applications: interfaces that are networked, interactive, and layered—where the browser becomes a runtime environment, and the Internet becomes the medium through which your programs communicate.