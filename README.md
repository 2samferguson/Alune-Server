# Alune Server
Alune Server is a back-end web application built in Flask and deployed with AWS Elastic Beanstalk. The server manages and processes the data used for ML model construction / training. Match statistics and model parameters are stored in the `data` folder and hosted at specified web addresses through `application.py`

# Model Training
Individual match data is acquired through the [Riot Games APIs](https://developer.riotgames.com/), which provides a database of over 1 billion match instances. However, API restraints and other compute limitations reduced the number of samples I was able to utilize through this avenue. When attempting to train Logistic Regression / Deep Learning models through the traditional optimized gradient descent methods, computational resources limited my sample size to 100,000 match instances, which was not sufficient to achieve convergence on the match prediction task.

Fortunately, there are certain tools that undertake most of the computational grunt-work by providing basic statistics across a very large number of matches. This includes [LoLalytics](https://lolalytics.com/), which among other features counts the number of instances that every (champion-role) x (champion-role) pair appears on a team within each patch cycle, partitioned by win/loss response. With 160 champions across 5 roles, this provides us with 640,000 unique statistical features computed across about 10 million games per patch.

To construct the model, `grabdata.py` first collects match statistics across 800 different LoLalytics pages, and processes the data into four NumPy tensors of shape (160, 160, 5, 5). Then, `model.py` uses ideas from classical statistical theory to propagate these tensors through a series of transformations into suitable parameters for an ML model. Here, the `np.einsum()` method is used for generalized tensor (linear algebra) operations. The resulting architecture is equivalent to that of a logistic regression model with around 25,000 parameters.

This method far outperformed my initial training attempts when validated against the original test set, and appeared to achieve convergence on the match prediction task. Since most of the computational work was outsourced and the initial statistical features came pre-processed, training time stayed constant regardless of the number of samples, which allowed me to effectively 100x the size of my original dataset.




