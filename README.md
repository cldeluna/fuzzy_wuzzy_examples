### Fuzzy Wuzzy was a Python Module

An example of using the fuzzywuzzy module to match data sets.

I was recently given a list of locations that I had to analyze.
For the analysis, I needed data that was not in the original list (lets call that the source list).   Luckily I had a larger data set (lets call that the detailed list) that included the source list, which did have all the additional data I needed.  Even better, both lists had an "Address" column so I figured it would be a simple matter of looking up each location in my source list in the larger detailed list and picking out the additional data that I needed.

...or so I thought...

As as drilled down to the 




Helpful Links

How this module came to be 
https://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/


PiPy
https://pypi.org/project/fuzzywuzzy/

GeeksforGeeks FuzzyWuzzy Python library
https://www.geeksforgeeks.org/fuzzywuzzy-python-library/

Data Camp
https://www.datacamp.com/community/tutorials/fuzzy-string-python

Combining Datasets with Fuzzy Matching by Roland Jeannier
https://medium.com/@rtjeannier/combining-data-sets-with-fuzzy-matching-17efcb510ab2

