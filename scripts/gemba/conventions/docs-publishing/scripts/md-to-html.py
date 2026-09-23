#!/usr/bin/env python3
"""Convert a committed markdown artifact into the body the docs-publishing
convention publishes (see ../convention.md, "Publish and append", step 1).

Usage: python3 md-to-html.py ARTIFACT.md > body.html

The body is the artifact with exactly the changes step 1 lists: the
frontmatter and the H1 stripped, every paragraph and list item on one line, a
mark that cannot wrap code closed before the code and reopened after it, and
code passed verbatim. It is written as standard HTML, one top-level block per
line, for a connector that stores its structured format as received.

Covered: headings (## to ###), paragraphs, bulleted and numbered lists (nested,
with fenced blocks inside an item), tables, fenced code blocks, quotes, bold,
italic, inline code (a span may cross a line) and links. Anything else it
refuses rather than publish it wrong: an image, a heading of level 4 or
deeper, an unclosed fence. A refusal exits 2 with the reason on stderr and
nothing on stdout; an unreadable file does the same. Standard library only.
"""

import html
import re
import sys


class Refused(Exception):
    pass


MARKER = re.compile(r"^( *)([-*]|\d+\.) +(.*)$")
FENCE = re.compile(r"^( *)(`{3,})\s*([\w+-]*)\s*$")
TABLE_DELIM = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


# --- inline -----------------------------------------------------------------

def tokenize(text):
    """Split text into ('text', s), ('code', s), ('link', label, url) and
    ('delim', '*' | '**', can_open, can_close) tokens."""
    tokens, i, n = [], 0, len(text)
    buf = []

    def flush():
        if buf:
            tokens.append(("text", "".join(buf)))
            buf.clear()

    while i < n:
        c = text[i]
        if c == "`":
            run = len(text[i:]) - len(text[i:].lstrip("`"))
            close = text.find("`" * run, i + run)
            if close != -1:
                flush()
                tokens.append(("code", text[i + run:close]))
                i = close + run
                continue
            buf.append(text[i:i + run])
            i += run
            continue
        if c == "[":
            m = re.match(r"\[([^\]]+)\]\(([^)\s]+)\)", text[i:])
            if m:
                flush()
                tokens.append(("link", m.group(1), m.group(2)))
                i += m.end()
                continue
        if c == "*":
            run = 2 if text.startswith("**", i) else 1
            before = text[i - 1] if i > 0 else " "
            after = text[i + run] if i + run < n else " "
            can_open = not after.isspace()
            can_close = not before.isspace()
            if can_open or can_close:
                flush()
                tokens.append(("delim", "*" * run, can_open, can_close))
                i += run
                continue
        buf.append(c)
        i += 1
    flush()
    return tokens


def pair(tokens):
    """Match delimiters; an unmatched one becomes literal text."""
    stack, kinds = [], [None] * len(tokens)
    for idx, tok in enumerate(tokens):
        if tok[0] != "delim":
            continue
        _, d, can_open, can_close = tok
        match = next((k for k in range(len(stack) - 1, -1, -1)
                      if tokens[stack[k]][1] == d), None)
        if can_close and match is not None:
            opener = stack[match]
            del stack[match:]
            kinds[opener], kinds[idx] = "open", "close"
        elif can_open:
            stack.append(idx)
    out = []
    for idx, tok in enumerate(tokens):
        if tok[0] == "delim":
            tag = "strong" if tok[1] == "**" else "em"
            out.append((kinds[idx], tag) if kinds[idx] else ("text", tok[1]))
        else:
            out.append(tok)
    return out


def inline(text):
    """Render inline markdown. Marks open lazily, just before the text they
    wrap, and every open mark closes before a code span and reopens after it:
    the body never carries a mark around <code>."""
    out, want, have = [], [], []

    def sync():
        while have and have != want[:len(have)]:
            out.append(f"</{have.pop()}>")
        for tag in want[len(have):]:
            out.append(f"<{tag}>")
            have.append(tag)

    def close_all():
        while have:
            out.append(f"</{have.pop()}>")

    for tok in pair(tokenize(text)):
        kind = tok[0]
        if kind == "open":
            want.append(tok[1])
        elif kind == "close":
            if tok[1] in want:
                del want[len(want) - 1 - want[::-1].index(tok[1])]
        elif kind == "text":
            if tok[1]:
                sync()
                out.append(html.escape(tok[1], quote=False))
        elif kind == "code":
            close_all()
            out.append(f"<code>{html.escape(tok[1], quote=False)}</code>")
        elif kind == "link":
            sync()
            out.append(f'<a href="{html.escape(tok[2])}">{inline(tok[1])}</a>')
    close_all()
    return "".join(out)


# --- blocks -----------------------------------------------------------------

def starts_block(line):
    s = line.lstrip(" ")
    return (s.startswith("#") or s.startswith(">") or s.startswith("|")
            or FENCE.match(line) is not None or MARKER.match(line) is not None
            or s.startswith("!["))


def fence_block(lines, i, lineno):
    m = FENCE.match(lines[i])
    ind, ticks, lang = len(m.group(1)), m.group(2), m.group(3)
    body, j = [], i + 1
    while j < len(lines):
        s = lines[j]
        if s.strip() == ticks or (s.strip().startswith(ticks) and s.strip().strip("`") == ""):
            code = html.escape("\n".join(body), quote=False)
            cls = f' class="language-{lang}"' if lang else ""
            return f"<pre><code{cls}>{code}</code></pre>", j + 1
        body.append(s[ind:] if s[:ind].strip() == "" else s.lstrip(" "))
        j += 1
    raise Refused(f"unclosed code fence at line {lineno(i)}")


def split_row(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", row)]


def list_block(lines, i, lineno):
    base = indent_of(lines[i])
    ordered = not MARKER.match(lines[i]).group(2) in ("-", "*")
    items, j = [], i
    while j < len(lines):
        m = MARKER.match(lines[j])
        if not m or len(m.group(1)) != base:
            break
        if (m.group(2) not in ("-", "*")) != ordered:
            break
        content = [m.group(3)]
        k = j + 1
        while k < len(lines):
            s = lines[k]
            if s.strip() == "":
                nxt = next((t for t in lines[k + 1:] if t.strip()), None)
                if nxt is not None and indent_of(nxt) > base:
                    content.append("")
                    k += 1
                    continue
                break
            if indent_of(s) <= base:
                break
            content.append(s)
            k += 1
        items.append(content)
        j = k
        while j < len(lines) and lines[j].strip() == "":
            nxt = next((t for t in lines[j:] if t.strip()), None)
            m2 = MARKER.match(nxt) if nxt else None
            if m2 and len(m2.group(1)) == base and (m2.group(2) not in ("-", "*")) == ordered:
                j += 1
            else:
                break
    rendered = []
    for content in items:
        first, rest = content[0], content[1:]
        text = [first]
        r = 0
        while r < len(rest) and rest[r].strip() and not starts_block(rest[r]):
            text.append(rest[r].strip())
            r += 1
        tail = rest[r:]
        if tail:
            cut = min(indent_of(t) for t in tail if t.strip())
            tail = [t[cut:] for t in tail]
        child = "".join(blocks(tail, lambda x: lineno(i))) if tail else ""
        rendered.append(f"<li>{inline(' '.join(text))}{child}</li>")
    tag = '<ol start="1">' if ordered else "<ul>"
    end = "</ol>" if ordered else "</ul>"
    return tag + "".join(rendered) + end, j


def blocks(lines, lineno):
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("!["):
            raise Refused(f"unsupported image at line {lineno(i)}")
        if FENCE.match(line):
            b, i = fence_block(lines, i, lineno)
            out.append(b)
            continue
        m = re.match(r"^(#+) +(.*)$", s)
        if m:
            level = len(m.group(1))
            if level > 3:
                raise Refused(f"unsupported level-{level} heading at line {lineno(i)}")
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue
        if s.startswith("|") and i + 1 < len(lines) and TABLE_DELIM.match(lines[i + 1].strip()):
            head = split_row(s)
            rows, i = [], i + 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>")
            continue
        if s.startswith(">"):
            paras, cur = [], []
            while i < len(lines) and lines[i].strip().startswith(">"):
                t = lines[i].strip()[1:].strip()
                if t:
                    cur.append(t)
                elif cur:
                    paras.append(cur)
                    cur = []
                i += 1
            if cur:
                paras.append(cur)
            out.append("<blockquote>" + "".join(f"<p>{inline(' '.join(p))}</p>" for p in paras) + "</blockquote>")
            continue
        if MARKER.match(line):
            b, i = list_block(lines, i, lineno)
            out.append(b)
            continue
        para = []
        while i < len(lines) and lines[i].strip() and (not para or not starts_block(lines[i])):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return out


def convert(source):
    lines = source.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), None)
        if end is not None:
            start = end + 1
    while start < len(lines) and not lines[start].strip():
        start += 1
    if start < len(lines) and re.match(r"^# ", lines[start]):
        start += 1
    body = lines[start:]
    return "\n".join(blocks(body, lambda k: k + start + 1)) + "\n"


def main(argv):
    if len(argv) != 2:
        print("usage: md-to-html.py ARTIFACT.md", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            source = f.read()
    except OSError:
        print(f"md-to-html: cannot read {argv[1]}", file=sys.stderr)
        return 2
    try:
        sys.stdout.write(convert(source))
    except Refused as e:
        print(f"md-to-html: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
