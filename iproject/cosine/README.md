# cmpe-256-individual-project

### Quick Start for running the Subreddit recommender engine

1: Use python3 and install the packages in requirements.txt
```
  $ pip3 install -r requirements.txt
```
2: Add Reddit developer account OAuth details to praw.ini. 
```
  $ client_id=####
  $ client_secret=####
  $ password=####
  $ username=####
```
3: Collect some data. It will be saved as mongodb bson file. An example is dumped in dump/ directory
```
  $ python3 dataset.py
```
4: Run the recommender. It is also available as jupyter notebook kNN.ipynb
```
  $ python3 kNN.py
```
