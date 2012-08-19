Web Scanner
===========

Web Scanner is an easy script, which reads and parses certain web page.
It returns desired part of the web page, which is saved as an HTML file.
It is useful for keeping web page history (e.g. Google Play app review stats).

Web Scanner utility is supposed to run on the server. It saves HTML file
periodically in specified intervals. URL of page and time interval are set
in constants on the top of the webscanner.py script.

Summarize utility takes all HTML files with Google Play app review stats
and creates text file with data in table. This table can be easily copied
for example to Google Doc.


Usage
=====

Web Scanner is a console application (must be run in the command line)
and is written in Python 2.7. To run it, you must have installed Python
interpreter, which can be downloaded at: www.python.org.

* nohup python webscanner.py & - run webscanner script on the server
* python summarize.py - run summarize script


Developed by
============

* [Petr Nohejl](http://petrnohejl.cz)
* [Martin Skala](http://sanero.cz)


License
=======

    Copyright (C) 2012 Petr Nohejl, petrnohejl.cz
    Copyright (C) 2012 Martin Skala, sanero.cz

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
    
    This program comes with ABSOLUTELY NO WARRANTY!
