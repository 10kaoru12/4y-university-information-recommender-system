from surprise import SVDpp
from surprise import Dataset, Reader
from surprise.model_selection import cross_validate


# Load the movielens‐100k dataset (download it if needed), 
reader = Reader(line_format='user item rating', sep=' ')
dataset = Dataset.load_from_file('./sushi3-2016/sushi3b.5000.10.score_converted', reader = reader)
trainset = dataset.build_full_trainset()

# We'll use the famous NMF algorithm. 
algo = SVDpp()
algo.fit(trainset)

# Run 5‐fold cross‐validation and print results
cross_validate(algo, dataset, measures=['RMSE', 'MAE'], cv=5, verbose=True)