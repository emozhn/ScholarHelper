# My Research Automatic Helper

Some scripts that help you automatic your research process!

simply use python -m xxx to call these scripts.

## ``chase_arxiv``
This srcipt can help fetch papers from Arxiv recent week.

You can specify your interested subareas and key words to filter the titles.
Below code is on top of this script, as you can specify it!

```python
subareas = ["AI", "LG", "RO"]
key_words = ["plan", "motion", "decision", "reinforcement", 
            ("generat", "plan"), ("reinforcement", "plan"), ("decision", "gpt"), 
            ("decision", "transformer"), ("plan", "transformer"), ("plan", "diffusion")]
HEADER = "Your own header"
```

For ``subareas``, every word in the list will be search. (eg "AI" indicates artificial intelligence, you may refer to arxiv to get the subareas.)

For ``key_words``, each element is a rule:
-   if the element is a string (eg "plan"), titles containing the string will be chosen.
-   if it is a tuple (eg ("generat", "plan")), titles contain both strings will be chosen.
Titles that hit any one of rules in ``key_words`` will be chosen.

``HEADER`` is copy from your own browser.

## ``find_citation``
This script will help extract paper titles from json file export from DBLP.org, it will fetch the citation of each paper.
Then sort them based on citations and out put title and citations.

```python
LINK_PREFIX = "https://scholar.google.com/scholar?q="
PATTERN = re.compile(r'Cited by \d+')
HEADER = "Your own header"
USE_DRIVER = True
```
You need to specify your own header from your web browser.
If ``USE_DRIVER`` is set ``True``, you need to install selenium to fetch information from google scholar. 

## ``fetch_from_dblp``
The json export can only export 1000 items at most, sometimes you may need more than that, so you can use this script to fetch all papers from the ``TARGET_LINK``.

If you have other cool ideas, welcome to raise pull request~