# Blog @ blog.itconsense.com

Go there ...

https://blog.itconsense.com

Build
=====

Clone from repository

```bash
 $ git clone git@github.com:tomgross/blog.toms-projekte.de.git
```

Get theme in submodules
```bash
 $ git submodule init
 $ git submodule update
```

Install Pelican blog generator

```bash
 $ pip install pelican
```

Generate blog

```
 $ pelican -t themes/Flex/ content
```
