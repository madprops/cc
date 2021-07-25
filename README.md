### This is meant to be a z implementation that better meets my needs

Git clone this somewhere then add this to .bashrc:

```
source /path/to/ezkl/ezkl.sh
```

Then `source ~/.bashrc`

Now use cd normally to remember paths

And use z to jump to locations

`cd /some/path`

`z something`

![](https://i.imgur.com/IFp9xtB.jpg)

It forgets paths (from paths.txt) that don't seem to exist anymore.

It's possible to use multiple keywords to specify path hierarchy:

"z code tetris" matches paths like `~/code/tetris`. 

There's a `--paths` flag to print all paths.