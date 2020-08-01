Introduction:

Try to find out how MLB players' weight affect the time between their debut and Tommy John surgery date

Methods:

Gather data from Lahman's baseball database's 'People' table and list of players who underwent Tommy John surgery from Wikipedia

Use SQL Server to prepare the data

Use Python(Spyder) to perform cluster analysis(heirarchical and k-means)

Results:

1.Heirarchical clustering:

Dendrogram and scatterplot can all be found in png files

cluster centers for ward method->                
                scaled_weight  scaled_daydiff
cluster_labels                               
1                    9.563979        2.938938
2                   11.259209        0.900693
3                    9.742926        0.829481


cluster centers for single method-> 
                scaled_weight  scaled_daydiff
cluster_labels                               
1                    8.271679        4.527003
2                   13.426493        1.395061
3                   10.185661        1.202330

cluster centers for complete method-> 
                scaled_weight  scaled_daydiff
cluster_labels                               
1                    9.594348        3.022018
2                   11.675427        1.502052
3                   10.062185        0.771779


2.k-means clustering result:

elbow plot and scatterplot can all be found in png files

cluster centers for random seed

                scaled_weight  scaled_daydiff
cluster_labels                               
0                    9.678264        2.783786
1                   11.241075        0.929718
2                    9.685297        0.712585
