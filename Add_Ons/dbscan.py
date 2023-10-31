from sklearn.datasets import make_blobs
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN

# 1. Generate more random sample data (2D points).
X, _ = make_blobs(n_samples=300, centers=5, cluster_std=0.60, random_state=91)

# 2. Apply the DBSCAN algorithm.
db = DBSCAN(eps=0.5, min_samples=10)
labels = db.fit_predict(X)

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# 3. Visualize the clusters.
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
plt.title(f"Estimated number of clusters: {n_clusters_}")
plt.show()
