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

unspooler offers two primary functions: ```unspool_easy``` (easy) and ```unspool``` (advanced). The former is, as its name implies, easier to use, but has the distinct disadvantage of not allowing resumption of interrupted jobs. ```unspool``` is slightly more complex to use but allows resuming. The longer your job, the more I recommend using ```unspool``` over ```unspool_easy```.

Here's how you'd do the above job with ```unspool```:

```python
from unspooler import *
shortlinks = ['http://tinyurl.com/2unsh','http://bit.ly/1dNVPAW'] #examples from http://www.getlinkinfo.com
shorts = {}
for i in unspool(shortlinks):
    shorts.update(i)
print(shorts['urls'])
```

If this job is interrupted, the ```shorts``` variable will contain all unshortened data up to the point of interruption. You can then simply re-run ```unspool``` with ```resume_dict=shorts``` and it will quickly skip past all the links it has previously processed and resume at the last unprocessed link.
