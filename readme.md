# macstats

simple python osx app that shows system usage in menu bar / touch bar

only shows something if it is above limit

- cpu (>75%)
- network (>1 MB/sec)
- disk (>1 MB/sec)

feel free to extend

building:
```
python3 setup.py py2app
open dist/macstats.app
```
