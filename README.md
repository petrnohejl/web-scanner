Web Scanner
===========

Web Scanner is a simple script, which reads and parses certain web page.
It returns desired part of the web page, which is saved as a HTML file.
It is useful for keeping web page history (e.g. Google Play app review stats).

Web Scanner utility is supposed to run on the server. It saves HTML file
periodically in specified intervals. URL of page and time interval are set
in constants on the top of the webscanner.py script.

Summarize utility takes all HTML files with Google Play app review stats
and creates text file with data in table. This table can be easily copied
for example to Google Doc.


Usage
=====

Web Scanner is a console application and is written in Python 2.7. To run it,
you must have installed Python interpreter, which can be downloaded
at www.python.org.

```bash
$ nohup python webscanner.py &    # run webscanner script on the server
$ python summarize.py             # run summarize script
```


Developed by
============

* [Petr Nohejl](http://petrnohejl.cz)
* Martin Skala


License
=======

    Copyright 2012 Petr Nohejl
    Copyright 2012 Martin Skala

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
