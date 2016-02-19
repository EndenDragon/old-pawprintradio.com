# The Mane Frame Radio Website Repository
**By [EndenDragon](http://twitter.com/EndenDragon) | [http://mane-frame.com](http://mane-frame.com)**

This is the Mane Frame Radio's website. It is currently actively developed by the web developer, EndenDragon. The site is built using Flask as the foundation on Python 2.7.9. Contributing some code, or write some paragraphs are greatly appreciated.

**The readme will be updated periodically**

## Table of Contents
* [Required Dependencies](#required-dependencies)
* [Optional Dependencies](#optional-dependencies)
* [Installation Instructions](#installation-instructions)
* [Significant Files Breakdown](#significant-files-breakdown)
* [Contributers](#contributers)
* [Copyright](#copyright)

## Required Dependencies:
**(Get the latest version when possible, unless specified)**
* internet connection
* python 2.7.9 +
* Flask `pip install Flask`
* Flask-SQLAlchemy `pip install Flask-SQLAlchemy`
* MySQLdb `apt-get install python-mysqldb`

## Optional Dependencies
* Adobe Photoshop CS6 ~or above (To beable to view the website sketches)
* [Atom.io](https://atom.io/) (Awesome modern code editor)
* Discord App (To scream at EndenDragon in case there is a problem on his side)

## Installation Instructions
1. Gather the required dependencies
2. Download the zip tarball or clone the repository
3. Locate `SAMPLE mysql-login.json` and make a copy, removing the `SAMPLE` from the filename.
4. Fill out the mysql details in `mysql-login.json` and save the file. This is for the requests system, and the app cannot run without it.
5. Repeat step 3 and 4 with `SAMPLE config.json` file, copying it to `config.json`, and edit the contents.
6. Locate any of the `.py` files within the folder and run them using python. For example: `python main.py` (from mane-site)
7. Open up a web browser and point to the ip address shown in the window

## Significant Files Breakdown
```
* mane-frame.com/
|    * mane-site/
|    |    * main.py
|    |    * xml2dict.py
|    |    * crossdomainfuncs.py
|    |    * static/
|    |    |    * css/
|    |    |    |    * custom.css
|    |    |    * templates/
|    |    |    |    * about.html
|    |    |    |    * blog.html
|    |    |    |    * contact.html
|    |    |    |    * donate.html
|    |    |    |    * events.html
|    |    |    |    * footer.html
|    |    |    |    * header.html
|    |    |    |    * index.html
|    |    |    |    * menu.html
|    |    |    |    * player.html
|    |    |    |    * sidebar.html
|    |    |    |    * team.html
|    * mane-site-static/
|    |    * css/
|    |    |    * custom.css
|    |    * img/
|    |    |    * staff/
|    |    * index.html
|    |    * about.html
|    |    * team.html
|    |    * blog.html
|    |    * donate.html
|    |    * events.html
|    * comingsoon/
|    |    * templates/
|    |    |    * index.html
|    |    * index.py
|    |    |    * static/
|    |    |    |   * silverleaf.png
|    * staff/
|    |    * list & bio.txt
|    * Site Drawings/
|    |    * mane-frame.psd
|    * test/
|    |    * ajax-pageload/
|    |    |    * mfr-ajax-pageload-demo.py
|    |    * menubar/
|    |    |    * menubar.html
|    |    * OAuth/
|    |    |    * oauth.py
|    |    * player/
|    |    |    * mfr-player-demo.py
|    * mfr-imgs/
```
## Contributers
**To shed some light into who helped me along the way!**
* Dusk
* ShadowPony
* unicodingunicorn
* Krillik
* Vapid Pixel
* toothydeerrrrrr
* neonstrobelights

## Copyright
Everything is All Rights Reserved by Mane Frame Radio unless specified.