# unspooler
**Research-grade URL expansion for Python.**

unspooler is a Python module that expands shortened URLs (e.g. by bit.ly, goo.gl, tiny.cc, etc.) quickly and efficiently. It extracts each URL in a dataset once and only once, decreasing execution time and bandwidth usage. It can also resume partially complete jobs so you don't have to start from scratch if something interrupts execution.

**System requirements**

* Python 3, and that's it.

**Installation**

```python
pip install unspooler
```

Or drop the main file into whatever directory you want--all its dependencies are in the Python standard library.

**Quick start**

```python
from unspooler import *
shortlinks = ['http://tinyurl.com/2unsh','http://bit.ly/1dNVPAW'] #examples from http://www.getlinkinfo.com
shorts = unspool_easy(shortlinks)
print(shorts['urls'])
```

**Detailed documentation**
