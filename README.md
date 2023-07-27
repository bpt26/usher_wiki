# docs for UShER
Codebase for [the UShER wiki](https://usher-wiki.readthedocs.io/en/latest/).

## notes for maintainers of these docs
### compiling locally
1. `pip install -r requirements.txt`
2. `cd docs`
3. `make linkcheck`
4. `make html`

Docs will be created in a new folder named `build`, and you can clean up afterwards with `make clean`.

### tips for using RST
* [RST reference docs](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
* When creating internal links, use `:ref:` or `:doc:` to make a relative path to the page rather than making a hyperlink to the absolute URL, which may change over time. [See sphinx's docs](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#ref-role) on how to use those.
  * Images that link to an internal page are a possible exception since there's no other way to make that kind of thing work, but we don't have any of those yet
* RST can't really do nested formatting (eg it can do **bold** and *italics* but not ***bold italics***)
* RST takes Python's concept of meaningful whitespace and runs with it, so sometimes you need a blank newline after certain declarations (`:orphan:` and `:hidden:` for example)

### common warnings/errors
* `document isn't included in any toctree` -- "toctree" is the table-of-contents sidebar which appears on the left when the docs are compiled. If you want the file to appear in this sidebar, add it to the toctree declaration in index.rst. If you don't want it to end up on the sidebar, add `:orphan:` plus a blank newline at the top of the document.
  * The `toctree` declaration not only builds the sidebar on the left hand side of the webpage, it also will create a table of contents in the body of the text itself. The docs currently use the `:hidden:` declaration to hide this body-toc -- note that `:hidden:` does not hide the sidebar toc.
* `Title underline too short` -- RST is picky about this, just roll with it.
* `Duplicate explicit target name` -- [this is another weird RST quirk](https://github.com/sphinx-doc/sphinx/issues/3921), which can be solved by including two underscores instead of one when referencing other pages
* Some websites (Zendesk-based docs, doi.org, etc) consistently break `linkcheck`, so if you have an external link that you know is working, but it can't pass linkcheck, just add the URL to linkcheck_ignore in conf.py