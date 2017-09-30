# ml-ssa-birthnames

A journey into Python and Machine Learning with the birthname database of the Social Security Agency

**WORK IN PROGRESS!**

## Introduction

Not long ago, I stumbled upon a nice Tweet by [Martín Donato](https://twitter.com/martindonato/status/910019348953223169)
in which a map showed the evolution of the most popular female names in USA, by state, from 1960 to 2016.

![Map showing the year 1960](https://pbs.twimg.com/tweet_video_thumb/DKEJxHIXkAA6Sj4.jpg)

<blockquote class="twitter-tweet" data-lang="es"><p lang="es" dir="ltr">El mapa gif del día,
el nombre de mujer más popular en los distintos estados de USA por año.
<a href="https://t.co/t1WLWMknVm">pic.twitter.com/t1WLWMknVm</a></p>&mdash; Martín Donato✴
(@martindonato) <a href="https://twitter.com/martindonato/status/910019348953223169?ref_src=twsrc%5Etfw">19 de septiembre de 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Looking at the map, several questions came to mind:

* Could it be possible to predict the most used baby name in the US one, two, five or ten years ahead?
* What about doing that at state level?
* Are there any "early adopter" states where names become popular first and others that follow the trend a few years later?

In one of the comments a link to the possible source was shown: the [Social Security "Popular Names by State"](https://www.ssa.gov/OACT/babynames/state/index.html) website.
It is an amazing source of information, some of it dating back to the 19th century!

In that moment, a lightbulb lighted up above my head. The data was there, I just had to download it and see if I could find a way to answer my questions.

### The plan

I have read something about ML, but never really did anything practical with it. Also, I have never programmed in Python, although I know the syntax.

The plan I initially came up with was:

1. Read something more about ML. Some material I recommend:

	* (Book) [Discovering knowledge in data: an introduction to data mining](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0470908742.html)
	* (Book) [Data mining and predictive analytics](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-1118116194.html)
	* (Online tutorial) [Practical machine learning tutorial with Python introduction](https://pythonprogramming.net/machine-learning-tutorial-python-introduction/)
	* (Online tutorial) [TensorFlow tutorial for beginners](https://www.datacamp.com/community/tutorials/tensorflow-tutorial#gs.es_61Bs)
	* (Online tutorial) [Large-scale Linear Models with TensorFlow](https://www.tensorflow.org/tutorials/linear)
    
    Warning: You really have to be comfortable with maths and statistics in order to grasp ML.

2. Download the data. Also, store it in a useful format.

3. Transform the data. I don't know if this is really needed, but it is possible that the data has to be normalized before being fed to the ML algorithm.

4. Try some heuristics. Is it possible to apply some simple heuristics in order to predict next year's most used name? Maybe. And predict 2, 5 or 10 years ahead? I doubt it.
   What about detecting the early adopters and the followers?

5. Machine learning. I think I will go for Google's [TensorFlow](https://www.tensorflow.org/get_started/get_started).

## Downloading the data

After navigating SSA's website for a while, I decided that two datasets were of interest:

- [Top 1000 baby names at country level per year](https://www.ssa.gov/OACT/babynames/index.html), showing either number of births or percentage of total births.
- [Top 100 baby names per state and year](https://www.ssa.gov/OACT/babynames/state/index.html), showing only number of births

Other datasets that I deemed not of interest were:

- [Popularity of a name per year](https://www.ssa.gov/OACT/babynames/index.html)
- [Popular names by Territory](https://www.ssa.gov/OACT/babynames/territories.html)
- [Popular Baby Names By Decade](https://www.ssa.gov/OACT/babynames/decades/index.html)

### Webscrapping

_Note: I have not found a way to download the data directly in a nice format like CSV, JSON or the like. There is a huge dataset at [https://www.ssa.gov/data.json](https://www.ssa.gov/data.json), but I have not gone through all of it. I have looked at some random items and to be honest it does not look like it contains the birth name database. Please, let me know if there is an easier way of downloading the data._

I would like to use PHP + Guzzle but since I know that I will be needing Python -I don't even think about R,- I will do everything in Python. No more postponing learning Python!

In order to download the data, I had to resort to webscrapping. Within 10 minutes I had my downloader ready with PHP (CLI) and guzzler -downloading all the files took much longer,- but I knew that this project would require Python or R -gulp!- so I discarded it and decided that it was time to learn Python; which I had been postponing for too long.

So I had to look at the source code and decided to create a script to send an HTTP POST request for each year/state combination and also


When trying to install scrapy, I get an "Error building wheels for twisted." I don't know what a wheel is in this context.
I haven't even started coding and I already miss PHP and Composer :(

Anaconda? [Install Python on Windows (Anaconda)](https://medium.com/@GalarnykMichael/install-python-on-windows-anaconda-c63c7c3d1444)
