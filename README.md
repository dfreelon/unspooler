# unspooler
**Research-grade URL expansion for Python.**

```unspooler``` is a Python module that expands shortened URLs (e.g. by [bit.ly](https://bit.ly), [goo.gl](https://goo.gl), [tiny.cc](http://tiny.cc), etc.) quickly and efficiently. It extracts each URL in a dataset once and only once, decreasing execution time and bandwidth usage. It can also resume partially complete jobs so you don't have to start from scratch if something interrupts execution.

System requirements
-------------------
* Python 3
* [requests](http://docs.python-requests.org/en/master/)

Installation
------------
```python
pip install unspooler
```

Quick start
-----------
```python
from unspooler import *
shortlinks = ['Here is one shortlink: http://tinyurl.com/2unsh',
'And here is another: http://bit.ly/1dNVPAW'] #examples from http://www.getlinkinfo.com
unspooled = unspool_easy(shortlinks)
print(unspooled['urls'])
```

Detailed documentation
----------------------
```unspooler``` offers two primary functions: ```unspool_easy``` (easy) and ```unspool``` (advanced). The former is, as its name implies, easier to use, but has the distinct disadvantage of not allowing resumption of interrupted jobs. ```unspool``` is slightly more complex to use but allows resuming. The longer your job, the more I recommend using ```unspool``` over ```unspool_easy```.

Here's how you'd run the above job with ```unspool```:

```python
from unspooler import *
shortlinks = ['Here is one shortlink: http://tinyurl.com/2unsh',
'And here is another: http://bit.ly/1dNVPAW'] #examples from http://www.getlinkinfo.com
unspooled = {}
for i in unspool(shortlinks):
    unspooled.update(i)
print(unspooled['urls'])
```

If this job is interrupted, the ```unspooled``` variable will contain all unshortened data up to the point of interruption. You can then simply re-run ```unspool``` with ```resume_dict=unspooled``` and it will resume at the last unprocessed string. You can even reuse ```unspooled``` in the loop (actually you should do this; any new variable you use there will collect only data starting at the last resume point).

**Input**

```unspooler```'s primary functions accept two types of input: a single string containing URL data (embedded in a larger string or not), or an iterable containing such strings. They will attempt to extract and unshorten any shortlinks they find within these strings via regex; non-shortlink text is discarded. Whenever they come across a previously-encountered URL, they pull the unshortened link from the output dict instead of querying the unshortening service again. This improves performance over unshortening programs that don't use such a cache.

**Parameters**

```unspool``` and ```unspool_easy``` offer the following parameters:

* ```txt_data```: A string or iterable of strings containing shortlinks.
* ```short_domains```: List of shortlink domains to unshorten. The default list can be found on line 7 of unspooler.py. 
* ```resume_dict```: See explanation above.
* ```save_file```: When nonblank, specifies a text file to save unshortened and shortened links.
* ```save_dups```: If ```save_file``` is nonblank and ```save_dups``` is ```True```, duplicate URLs will be saved to the output file. 
* ```keep_query_strings```: A list of domains from which query strings (denoted by question marks) will not be removed. Contains only youtube.com by default.
* ```verbose```: When set to ```True```, displays program progress information.

To avoid errors, ```resume_dict``` is a parameter of ```unspool_easy``` but it is non-functional.

**Output**

```unspooler```'s output is a dict containing five items:

* ```urls```: A dict in which the keys are the shortened URLs and the values are the expanded URLs. Contains all URLs unshortened during the current session.
* ```curr_urls```: A dict in which the keys are the shortened URLs and the values are the expanded URLs. Contains only URLs in the current string.
* ```ct```: A dict in which the keys are the original URLs and the values are the numbers of times each URL was detected in the dataset.
* ```skip_urls```: A list of the URLs that generated errors when unspooler attempted to unshorten them.
* ```index```: The current index number of the iterable entered into unspooler (for resumption purposes).
