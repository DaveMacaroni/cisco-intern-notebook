# git Basics



### clone

To clone a repository:

```
git clone https://github.com/DaveMacaroni/Notes.git
```



### branch

To create a local branch:

```
git checkout -b mybranch
```

To show the current branch:

```
git branch

* 05092020 <= the current branch has an asterisk
  master
```

To switch branches locally:

```
git checkout mybranch
```



### commit

To add files to commit:

```
git add myfile # OR
git add * # will add all files/directories
```

To commit the added files to the current branch:

```
git commit -m "add notes on git and markdown"
```



### push

To see remote repository:

```
git remote -v
```

To push the current branch to the upstream repository:

```
git push -u origin 05092020 # origin is an alias to the github server followed by the name of the branch
```



### stash

> NOTE: This is risky compared to using a commit to save your work, it is useful for quickly switching branches

To stash current changes in the current branch instead of committing them:

```
git stash
```

Once you stash your changes you can switch branches and when you come back and want to restore them:

```
git stash pop
```



