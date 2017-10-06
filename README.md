# ml-ssa-birthnames

A journey into Python and Machine Learning with the birthname database of
the US Social Security Agency

**WORK IN PROGRESS!**

## Introduction

Not long ago, I stumbled upon a nice Tweet by
[Martín Donato](https://twitter.com/martindonato/status/910019348953223169)
in which an animated gif showed a map of USA with the evolution of the most
popular female names by state, from 1960 to 2016.

<blockquote class="twitter-tweet" data-lang="es"><p lang="es" dir="ltr">El
mapa gif del día, el nombre de mujer más popular en los distintos estados
de USA por año.
<a href="https://t.co/t1WLWMknVm">pic.twitter.com/t1WLWMknVm</a></p>&mdash;
Martín Donato✴ (@martindonato)
<a href="https://twitter.com/martindonato/status/910019348953223169?ref_src=twsrc%5Etfw">19
de septiembre de 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Looking at the map, several questions came to mind:

* Would it be possible to predict the most used baby name at country level
one, two, five or ten years ahead?
* And at state level?
* Are there any "early adopter" states where names become popular first and
others that follow the trend a few years later?

In one of the comments a link to the possible source was shown: the [Social
Security "Popular Names by State"](https://www.ssa.gov/OACT/babynames/state/index.html)
website. It is an amazing source of information, some of it dating back to
the 19th century!

In that moment, a lightbulb lighted up above my head. The data was there, I
just had to download it and see if I could find a way to answer my questions.

### The plan

I have read something about ML, but never really did anything practical with
it. Also, I have never programmed in Python, although I know the syntax.

The plan I initially came up with was:

1. Read something more about ML. Some material I recommend:

	* (Book) [Discovering knowledge in data: an introduction to data mining](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-0470908742.html)
	* (Book) [Data mining and predictive analytics](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-1118116194.html)
    * (Basic theory) https://medium.com/towards-data-science/the-7-steps-of-machine-learning-2877d7e5548e
	* (Online tutorial) [Practical machine learning tutorial with Python introduction](https://pythonprogramming.net/machine-learning-tutorial-python-introduction/)
	* (Online tutorial) [TensorFlow tutorial for beginners](https://www.datacamp.com/community/tutorials/tensorflow-tutorial#gs.es_61Bs)
	* (Online tutorial) [Large-scale Linear Models with TensorFlow](https://www.tensorflow.org/tutorials/linear)
    
    Warning: You really have to be comfortable with maths and statistics in
    order to grasp ML.
    
    Please, let me know about any other learning material _for beginners_ on
    ML with Python.

2. Download the data. Also, store it in a useful format that allows us to
visualize and play with it locally.

3. Understand the data. Decide how to use it in order to be able to answer
our questions.

4. Transform the data. We may need to remove some features -_columns_ in
Excel terminology,- give numerical values to categorical ones or normalize
them. More on this later.

5. Try some heuristics. Is it possible to apply some simple heuristics in
order to predict next year's most used name? Maybe.
And predict 2, 5 or 10 years ahead? I doubt it.
What about detecting the early adopters and the followers? No idea.

6. Machine learning. I think I will go for Google's
[TensorFlow](https://www.tensorflow.org/get_started/get_started).

## Gathering the data

After navigating SSA's website for a while, I decided that two datasets were
of interest:

- [Top 1000 baby names at country level per year](https://www.ssa.gov/OACT/babynames/index.html),
showing either number of births or percentage of total births.
- [Top 100 baby names per state and year](https://www.ssa.gov/OACT/babynames/state/index.html),
showing only number of births.

Other datasets that I deemed not of interest were:

- [Popularity of a name per year](https://www.ssa.gov/OACT/babynames/index.html)
- [Popular names by territory](https://www.ssa.gov/OACT/babynames/territories.html)
- [Popular baby names by decade](https://www.ssa.gov/OACT/babynames/decades/index.html)

### Downloading the data (web scraping)

_Note: I have not found a way to download the data directly in a nice format
like CSV, JSON or the like. There is a huge dataset at
[https://www.ssa.gov/data.json](https://www.ssa.gov/data.json), but I have
not gone through all of it. I have looked at some random items and to be
honest it does not look like it contains the birth name database. Please,
let me know if there is an easier way of downloading the data._

In order to download the data, I had to resort to [web scrapping](https://en.wikipedia.org/wiki/Web_scraping).
Time to program my first Python script!

I had Python 3.5 installed in my computer from some time
ago. I tried to install `scrapy` with `pip` but I got an "Error building
wheels for twisted." It looks like I need the Visual C++ compiler toolchain
installed. No, no, no.

I hadn't even started coding and I was already missing PHP and Composer :(

Instead of fighting with Visual C++, I opted for
installing [Anaconda](https://www.anaconda.com/what-is-anaconda/),
an all-batteries-included Python package. I followed the instructions in
[Install Python on Windows](https://medium.com/@GalarnykMichael/install-python-on-windows-anaconda-c63c7c3d1444),
choosing the latest version 3.6.

To build the scraper I used `scrapy`. To store the data locally I used
`sqlite3` (included by default with Python) as lightweight database,
`yoyo-migrations` to create the table schemas and `sqlalchemy` as ORM.

```bash
conda install scrapy sqlalchemy
pip install yoyo-migrations

yoyo new -m "Create state level table"

yoyo.ini
src/SsaScraper.py
```

You can see the code of the scraper in [src/SsaSpider.py](src/SsaSpider.py).

## Understanding the data

How much data do we have? (As of 2017, with data from 1960 to 2016.)

2 genres * 57 years * ((1 country * 1000 names/country) + (51 states * 100 names/state)) = 695,400 genre-name-year combinations

For each genre-name-year, we have two values: 

- position, from 1 to 1000 or 1 to 100
- number of births

Add delta with same gender-name of previous year? No... or yes?

Mix genders? No.

Use everything? No. For each genre-name-year, take into account data of previous x years. 2? 5? 10?

Groups of 2 years: 56. Of 5 years: 53. Of 10 years: 48. Not a huge dataset for training.

Normalize? Yes.

## Preparing the data
