# June 20, 2024, 11:27 PM (PDT)
## Progress and Findings:

Today, I continued my research and debugging of the data cleaning process. I've been experimenting with different approaches to applying hyperparameter optimization. Currently, I'm using Optuna to fine-tune and understand the best results for my model.

I created two folders: one containing images that I handpicked as suitable for training the model, and another with images that are not suitable. The plan is to run Optuna to adjust the parameters and evaluate which configuration yields the best classification accuracy. This iterative process is helping to automate the parameter tuning and ensure the highest quality data is used for training.


# June 18, 2024, 10:35 PM (PDT)
## Progress and Findings:

Today, I continued my research and debugging of the data cleaning process. I came up with the idea of using a hyperparameter optimization algorithm to determine the optimal confidence and bounding box (bbox) ratio thresholds. To implement this, I created two folders: one containing images that I handpicked as suitable for training the model, and another with images that I deemed unsuitable.

The plan is to run the algorithm to adjust the parameters and evaluate which configuration yields the best classification accuracy. This process will help automate the parameter tuning, ensuring that the model is trained with the highest quality data. I aim to complete this process by tomorrow.

# June 17, 2024, 6:45 PM (PDT)
## Progress and Findings:

Today, I spent a significant amount of time debugging my data cleaning script to ensure I wouldn't lose any valuable data or retain any bad data. I created a script that selects 100 random images from the dataset I compiled from cars.com. Based on my defined parameters, the script then sorts the images into either a "cleaned" folder or a "discarded" folder.

After running the script, I manually reviewed the images in both folders to identify any that were incorrectly classified. This process allowed me to fine-tune my parameters multiple times. During these iterations, I also discovered a logic error in my script. By addressing this error and updating my parameters, I was able to improve the accuracy of my data cleaning process.
