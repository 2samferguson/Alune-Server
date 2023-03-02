# Alune Server
Alune Server is a back-end web application built in Flask and deployed with AWS Elastic Beanstalk. The server manages and processes the data used for model construction and training. Match statistics and model parameters are stored in the `data` folder and hosted at specified web addresses through `application.py`

# Model Training
Individual match data is acquired through the [Riot Games APIs](https://developer.riotgames.com/), which provides a database of over 1 billion match instances. However, API restraints and other compute limitations reduced the number of samples I was able to utilize through this avenue. When attempting to train Logistic Regression / Deep Learning models through the traditional optimized gradient descent methods, computational resources limited my sample size to 100,000 match instances, which was not sufficient to achieve convergence on the match prediction task.

Fortunately, there are certain tools that undertake most of the computational grunt-work by providing basic statistics across a very large number of matches. This includes [LoLalytics](https://lolalytics.com/), which among other features counts the number of instances that every (champion-role) x (champion-role) pair appears on a team within each patch cycle, partitioned by win/loss response. With 160 champions across 5 roles, this provides us with 640,000 statistical features computed across about 10 million games per patch.

To create the model, `grabdata.py` first collects match statistics across 800 different LoLalytics pages, and processes the data into NumPy tensors of shape (160, 160, 5, 5). Then, `model.py` uses ideas from classical statistical theory to propagate these tensors through a series of transformations into suitable model parameters. Here, the `np.einsum()` method is used for generalized tensor (linear algebra) operations. The resulting architecture uses a fixed first-layer encoding and has a single weight layer with around 25,000 parameters.

Since most of the heavy computational work was outsourced, training time stayed constant regardless of the number of samples, which allowed the model to effectively learn from 100x more instances than in my original training set. This method was successful in achieving convergence on the match prediction task, and through this metric the resulting model also surpassed human (expert) performance in evaluating team compositions.



