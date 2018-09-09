# git-branch-history

Keep an history of recently checked out git branch in order to go back easily.

Example:
```sh
$ git checkout -b improvement
Switched to a new branch 'improvement'
$ git checkout -b bugfix
Switched to a new branch 'bugfix'
$ git branch-history
0        bugfix
1        improvement
$ git branch-history 1
Switched to branch 'improvement'
```

The branch history is stored in a YAML file called `.git-branch-checkout-history` located in the repository top level directory.

# Installation

git-branch-history requires `pyyaml`.

### Installation from source

```sh
$ pip install git+https://github.com/ramanduh/git-branch-history.git
```

### Hook configuration

A git post-checkout hook should be enabled in order to add the checked out branch to the history db.

Here is an example of `.git/hooks/post-checkout`:

```
#!/bin/sh

if [ $3 -eq 1 ]; then
        git branch-history -p `git symbolic-ref --short HEAD` || exit 2
fi
```

You may need to change the file permission in order to be executable:
```sh
chmod +x .git/hooks/post-checkout
```

### Add a global alias

```sh
git config --global alias.bh branch-history
```


License
----

MIT

 :+1:
