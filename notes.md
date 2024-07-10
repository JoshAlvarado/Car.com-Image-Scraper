# July 9, 2024, 6:37 PM (PDT)
## Progress and Findings:

Today, I began manually reviewing the 7,000 images identified as "good" and deleting any that are not of the W205 model or those that slipped through the initial filtering. This process is time-consuming, but I am confident it will result in a better quality dataset for model training. 

By refining the dataset to only include relevant images, I aim to improve the model's accuracy and performance. This meticulous effort is crucial for ensuring that the model is trained on the most accurate and representative data. 

My next steps involve finalizing this manual review and then proceeding with training the model. Additionally, I plan to explore the potential use of synthetic data to further enhance the dataset.


# July 8, 2024, 12:38 AM (PDT)
## Progress and Findings:

Today, I finally cleaned the dataset. I found that the parameters provided by the hyperparameter optimization script were robust enough to automate the process effectively. In a folder of 1,000 random images pulled from the original dataset, only about 10 were car doors, while the rest were correctly classified as good images. Based on these results, I decided to clean the entire dataset using these parameters.

Here are the final statistics from the cleaning script:

- **Total time taken:** 18,862.99 seconds
- **Total images processed:** 45,192
- **Images kept:** 7,204
- **Duplicate images deleted:** 11,935
- **Unloadable images deleted:** 44
- **Images deleted for not meeting criteria:** 26,009


# June 25, 2024, 9:39 PM (PDT)
## Progress and Findings:

Today, I continued debugging the parameters. I am extremely satisfied with the images classified as "good" and those considered "bad" for discarding. However, I noticed that YOLO sometimes detects objects like steering wheels, resulting in uneven bounding boxes. This is because YOLO recognizes a car regardless of whether the image is of the interior or exterior.

To address this, I am considering implementing a method to verify whether the bounding box could represent a car based on its dimensions. For example, if the bounding box is longer vertically than horizontally, it is unlikely to be a car. My next goal is to explore this approach further and hopefully proceed with cleaning the database. I also plan to start researching the next steps after cleaning the dataset, possibly delving into synthetic data.


# June 23, 2024, 7:00 AM (PDT)
## Progress and Findings:

Today, I updated the YOLO model I was using from YOLOv5s to YOLOv5x, which has significantly better accuracy for detecting cars. I've definitely noticed an improvement when debugging the parameters. Additionally, I'm increasing the number of images in my "bad" and "good" folders and raising the number of tests conducted from 50 to a higher count for better parameter optimization.

I'm also continuing to read about the differences between YOLOv5 and YOLOv8. I've set the Optuna trials to 200, and it is expected to take approximately 10 hours. My next step in the project is to apply these optimized parameters to my raw dataset to create a clean dataset.


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
