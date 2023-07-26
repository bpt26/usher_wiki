# docs for UShER
Codebase for [the UShER wiki](https://usher-wiki.readthedocs.io/en/latest/).

## notes for maintainers of these docs
### compiling locally
1. `pip install -r requirements.txt`
2. `cd docs`
3. `make linkcheck`
4. `make html`

Docs will be created in a new folder named `build`, and you can clean up afterwards with `make clean`.

### tips
* [RST reference docs](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
* RST can't really do nested formatting (eg it can do **bold** and *italics* but not ***bold italics***)
* Add new pages to index.rst to ensure it ends up on the sidebar on the left
* Currently compiles with `-W`, so warnings become errors

### common warnings/errors
* `document isn't included in any toctree` -- "toctree" is the table-of-contents sidebar which appears on the left when the docs are compiled. Add the page in question to index.rst so it can be added to the toctree.
* `Title underline too short` -- RST is picky about this, just roll with it
* `Duplicate explicit target name: "here".` -- [this is another weird RST quirk](https://github.com/sphinx-doc/sphinx/issues/3921), which can be solved by including two underscores instead of one when referencing other pages
* Some websites (Zendesk-based docs, doi.org, etc) consistently break `linkcheck`, so if you have an external link that you know is working, but it can't pass linkcheck, just add the URL to linkcheck_ignore in conf.py