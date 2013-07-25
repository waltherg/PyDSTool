# Introduction

Apart from [modifications](https://github.com/waltherg/PyDSTool/commits/fix-pycont-vanderpol) 
I needed to apply to the source code -- see log of this branch -- 
these are the additional steps I needed to take to get this example to run.

# PyCont_vanDerPol.py

## pyconfig-32.h

Error message I noticed running the example:

```bash
Finding limit cycle using AUTO
In file included from /usr/include/python2.7/Python.h:8:0,
                 from /usr/users/cbu/waltherg/git/pydstool/PyDSTool/PyDSTool/PyCont/auto/src/include/auto_c.h:215,
                 from /usr/users/cbu/waltherg/git/pydstool/PyDSTool/PyDSTool/PyCont/auto/module/../src/fcon.c:7:
/usr/include/python2.7/pyconfig.h:4:25: fatal error: pyconfig-32.h: No such file or directory
compilation terminated.
```

You will notice that `/usr/include/python2.7/pyconfig.h` says this:

```c
#if __WORDSIZE == 32
#include "pyconfig-32.h"
#elif __WORDSIZE == 64
#include "pyconfig-64.h"
```

And on my 64-bit system `pyconfig-32.h` is not present.

However, instead of setting `__WORDSIZE` somewhere, all you need to do is
[remove the `-m32` flag in `PyDSTool/ContClass.py`](https://github.com/waltherg/PyDSTool/commit/7e13fd417fd5c00cce7a4010d9cfb40c5249a9b3).

**This example works now**
