import pandas as pd
import pyodbc

#Gain data from SQL server, tables was imported into SQL Server from two excel file 
#excel file can be found in the same repository
sql_conn = pyodbc.connect('''DRIVER={ODBC Driver 13 for SQL Server};
                            SERVER=ALLENHO\MSSQLSERVER002;
                            DATABASE=TommyJohn;
                            Trusted_Connection=yes''') 
query = '''
select distinct t.Player, t.Position, t.Throws, t.date_of_surgery, p.weight, datediff(day, p.debut, t.date_of_surgery) as daydiff
from TJ$ t
join People$ p
on t.Player=concat(nameFirst,' ',nameLast)
where p.weight is not null and datediff(day, p.debut, t.date_of_surgery)>0 and datediff(day, p.debut, t.date_of_surgery)<7000
order by t.Player;
;
'''
df = pd.read_sql(query, sql_conn)

import matplotlib.pyplot as plt

#-----standardize the data--------------------------------------------------------
# Import the whiten function
from scipy.cluster.vq import whiten

# Use the whiten() function to standardize the data

# Scale weight and daydiff
df['scaled_weight'] = whiten(df['weight'])
df['scaled_daydiff'] = whiten(df['daydiff'])

# Plot the two columns in a scatter plot
df.plot(x='scaled_weight', y='scaled_daydiff', kind = 'scatter')
plt.show()

# Check mean and standard deviation of scaled values
print(df[['scaled_weight', 'scaled_daydiff']].describe())


#-----Hierarchical clustering ward method-----------------------------------------------

# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage
import seaborn as sns
# Use the linkage() function
distance_matrix = linkage(df[['scaled_weight', 'scaled_daydiff']], method = 'ward', metric = 'euclidean')

from scipy.cluster.hierarchy import dendrogram
# Create a dendrogram
dn = dendrogram(distance_matrix)
plt.show()

# Assign cluster labels
df['cluster_labels'] = fcluster(distance_matrix, 3, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='scaled_weight', y='scaled_daydiff', 
                hue='cluster_labels', data = df )

# Display cluster centers of each cluster
print(df[['scaled_weight', 'scaled_daydiff', 'cluster_labels']].groupby('cluster_labels').mean())

plt.show()

#-----Hierarchical clustering single method------------------------------------

# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage
import seaborn as sns

# Use the linkage() function
distance_matrix = linkage(df[['scaled_weight', 'scaled_daydiff']], method = 'single', metric = 'euclidean')

from scipy.cluster.hierarchy import dendrogram

# Create a dendrogram
dn = dendrogram(distance_matrix)
plt.show()

# Assign cluster labels
df['cluster_labels'] = fcluster(distance_matrix, 3, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='scaled_weight', y='scaled_daydiff', 
                hue='cluster_labels', data = df)

# Display cluster centers of each cluster
print(df[['scaled_weight', 'scaled_daydiff', 'cluster_labels']].groupby('cluster_labels').mean())

plt.show()

#-----Hierarchical clustering complete method------------------------------------
# Import the fcluster and linkage functions
from scipy.cluster.hierarchy import fcluster, linkage
import seaborn as sns

# Use the linkage() function
distance_matrix = linkage(df[['scaled_weight', 'scaled_daydiff']], method = 'complete', metric = 'euclidean')

from scipy.cluster.hierarchy import dendrogram

# Create a dendrogram
dn = dendrogram(distance_matrix)
plt.show()

# Assign cluster labels
df['cluster_labels'] = fcluster(distance_matrix, 3, criterion='maxclust')

# Plot clusters
sns.scatterplot(x='scaled_weight', y='scaled_daydiff', 
                hue='cluster_labels', data = df)

# Display cluster centers of each cluster
print(df[['scaled_weight', 'scaled_daydiff', 'cluster_labels']].groupby('cluster_labels').mean())

plt.show()

#-----k-means clustering and elbow plot

# Import the kmeans and vq functions
from scipy.cluster.vq import kmeans, vq

distortions = []
num_clusters = range(1, 7)

# Create a list of distortions from the kmeans function
for i in num_clusters:
    cluster_centers, distortion = kmeans(df[['scaled_weight', 'scaled_daydiff']], i)
    distortions.append(distortion)
    
# Create a data frame with two lists - num_clusters, distortions
elbow_plot = pd.DataFrame({'num_clusters': num_clusters, 'distortions': distortions})

# Creat a line plot of num_clusters and distortions
sns.lineplot(x='num_clusters', y='distortions', data = elbow_plot)
plt.xticks(num_clusters)
plt.show()

# Generate cluster centers
cluster_centers, distortion = kmeans(df[['scaled_weight', 'scaled_daydiff']], 3)

# Assign cluster labels
df['cluster_labels'], distortion_list = vq(df[['scaled_weight', 'scaled_daydiff']], cluster_centers)

# Plot clusters
sns.scatterplot(x='scaled_weight', y='scaled_daydiff', 
                hue='cluster_labels', data = df)
plt.show()

#-----experiment with random seed

from numpy import random

# Set up a random seed in numpy
random.seed([1000,2000])

# Fit the data into a k-means algorithm
cluster_centers,_ = kmeans(df[['scaled_weight', 'scaled_daydiff']], 3)

# Assign cluster labels
df['cluster_labels'], _ = vq(df[['scaled_weight','scaled_daydiff']], cluster_centers)

# Display cluster centers 
print(df[['scaled_weight', 'scaled_daydiff', 'cluster_labels']].groupby('cluster_labels').mean())

# Create a scatter plot through seaborn
sns.scatterplot(x='scaled_weight', y='scaled_daydiff', hue='cluster_labels', data=df)
plt.show()