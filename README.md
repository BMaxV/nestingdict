# nestingdict
An easily nesting dict.

I needed a container for message passing. I wanted it to easily nest and clean up, for easy debugging, probably not so much for performance. This is what I pieced together. It basically works like an easy to manage file system:

 - you can write to any nesting without creating the keys explicitly:

```
d=MySpecialDict()
d["1"]["2"]["3"]="4"
```



 - there is a special mypop method that will pop the value from the specified level, and removed empty dicts and paths:

```
d["1"]["2"]="5"
d.mypop(["1","2","3"],"4")
d == {'1': {'2': '5'}}
```

- there is another method that will write to the dict with the same format as mypop:


```
d.mysetter(["a","b","c"],"d")
d == {'1': {'2': '5'}, 'a': {'b': {'c': 'd'}}}
```

You can pop not emptied dicts as well. 

In other words, it doesn't distinguish between "files" and "directories", `mypop` is `rm -rf` for the specified level.

That seems dangerous to me right now but there are cases where you'd want to just throw everything away behind some label. Because it's not an actual file system it shouldn't be too dangerous.

There is an optional argument to turn this behavior off though, if disabled, an error will be thrown.
