---
title:  My Blogging Workflow
updated: 2017-06-30 14:46:28
---

- [Emacs Blog Workflow](#org0c0398f)


<a id="org0c0398f"></a>

# Emacs Blog Workflow

Blogging with jekyll and org mode cloning the repo

```sh
git clone https://github.com/vishnudevtj/vishnudevtj.github.io.git
```

I keep a note.org file which contains all my notes , also have a org capute for note which inserts the notes . When i need to post my note as a blog . The required region is selected , and it is exported with [ox-gfm](https://github.com/larstvei/ox-gfm) exporter , since jekyll uses the github flavoured Markdown . Using the [Yasnippet](http://github.com/joaotavora/yasnippet) , the frontmatter of the post is inserted

    # -*- mode: snippet -*-
    # name: Jekyll FrontMatter
    # key: front
    # --
    ---
    title: ${`(capitalize (replace-regexp-in-string "[0-9][0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]" "" (replace-regexp-in-string "-" " " (file-name-base))))`}
    updated: ${`(format-time-string "%Y-%m-%d %H:%M:%S" (current-time))`}
    ---

this snippet insets the title [from the file name] and update time

Jekyll is installed using Docker

```sh
docker pull jekyll/jekyll
```

There is a cool package for emacs called [Prodigy](https://github.com/rejeep/prodigy.el) which is used to manage external services .

So prodigy is used to fire up the docker container . [Magit](https://magit.vc/) is used to upload the changes to github

Entered on <span class="timestamp-wrapper"><span class="timestamp">&lt;2017-06-28 Wed&gt;</span></span>
