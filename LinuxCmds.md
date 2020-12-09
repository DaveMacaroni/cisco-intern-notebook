# This is a guide to linux commands

### Navigation
**To know where you are**
```
pwd
```

**To see files**
```
ls
```
Add ``` -a``` to see hidden files

**To go to a directory**
```
cd *Directory Name*
```
If there is a space add ```\``` before it  
To go back a folder use ```cd..```  
To return home use ```cd```

### File commands
**To make a directory**
```
mkdir
```
Use ```\ ``` when making a directory with a space

**To remove a directory**
```
rmdir
```
```rmdir```can only delete empty directory, else use ```rm```

**To delete files**
```
rm
```
**To make a file**
```
touch
```
Remember to add file type extension

**To copy a file**
```
cd
```
Syntax is ```cd *File* *Location of Copy*```

**To move a file**
```
mv
```
Same syntax as cd  
Can also rename file ```mv *Old* *New*```

**To locate a file**
```
locate
```
Add ```-i``` to ignore upper/lower case sensitivity  
If there a multiple keywords sepereate with star: ```locate *Hello*World*```

### Misc

**Display contents**
```
cat
```

**Open editor**
```
vi
```
Add file extension when making new files with this

**Do command with administrator power**
```
sudo
```
Can use ```su``` to take root and stay in power

**Zip or unzip**

```zip``` or ```unzip```

**Install packages**

```apt-get```

