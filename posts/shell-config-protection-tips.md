---
title: "🤦‍♂️ I accidentally deleted my shell config: Three tips for preventing it happening again"
author: "Rens Dimmendaal"
date: "2022-02-01"
tags: ["TIL"]
draft: false
---

*Originally posted on [twitter](https://x.com/R_Dimm/status/1484888366495711232).*

Yesterday I messed up 🤦‍♂️ I accidentally deleted my shell config file.

It was a brain fart. I wanted to open the file with vim. Instead I typed rm.

```bash
rm ~/.zshrc
```

It happened in the office. I felt so stupid. My colleagues made a fun of me. But they also showed me a cool tool to avoid making this mistake again.

So here's how to protect yourself against accidentally deleting config files:

## #1. Backup your config files with dotbot

My biggest mistake was not having a backup of my config files.

I knew about 'bare git repositories' but that seemed a lot of work at the time.

Yesterday I learned about dotbot, which makes backing up your config files a bit easier.

I can't do it justice in this post. But if you don't backup your config files yet, then I recommend you check it out! There's a nice template repo to get started.

## #2. Use 'trash' not 'rm' to remove files

When you use 'rm' your to delete files and folders your data is really gone.

Install 'trash' and use that command to move items to the bin instead.

```bash
brew install trash
```

With the trash command you can retrieve the files from the recycling bin afterwards. Whenever you want to free up disk space you can empty your bin with a single command.

## #3. Anti-tip: Don't alias 'rm'

So "rm" is stuck in my muscle memory.

That's why I was tempted to follow a tip from Stack Overflow to to alias it to a warning:

```bash
alias rm="echo Use 'trash', or the full path i.e. '/bin/rm'"
```

However, as a commentor pointed out that, there's a risk that it will break some scripts that use 'rm'. So I'm staying away from that suggestion.

To wrap up. Don't be like me: don't accidentally delete your config files and do back them up. 