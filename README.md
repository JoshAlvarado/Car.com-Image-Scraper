# Car.com Image Scraper

## Overview
The Car.com Image Scraper is a dedicated tool designed to automate the collection of vehicle images from various listings on cars.com. This tool is specifically tailored to gather a diverse dataset for training machine learning models capable of identifying and classifying vehicles by their model codes. It supports features like filtering by interior/exterior images, removing duplicates, and ensuring high-quality images without banners.

## Features
- **Customizable Download**: Users can specify the number of images to download, stopping automatically once the target is reached.
- **Interior/Exterior Separation**: The scraper distinguishes between interior and exterior shots, organizing them into separate directories.
- **Banner Removal**: While primarily focusing on downloading images without banners, this functionality can be enhanced with a separate script for banner removal.
- **Support for Multiple Model Codes**: Allows for scraping images across multiple links corresponding to different car model codes.
- **Quality Control**: Integrates with a YOLO model to ensure downloaded images have a high confidence level of containing a car, and the car occupies a significant portion of the image.

## Current Repository Files
- `.gitignore`: Configured to exclude JPG images from the repository to keep it clean.
- `CarsScraper.py`: The main script for scraping images from cars.com.
- `CleanDataset.py`: Removes duplicates and filters out images where a car is not detected with a confidence level of 0.6 or above, or does not occupy at least 30% of the image area.
- `DebugClean.py`, `DebugThreshold.py`: Utility scripts for debugging and optimizing the cleaning process.
- `proxychecker.py`: Checks and verifies proxies to ensure uninterrupted scraping.
- `README.md`: Provides project documentation and instructions.
- `yolov5s.pt`: YOLOv5 small model for detecting cars in images.

## Enhancements and Future Work
- **Banner Detection and Removal**: Enhance the scraper or post-processing scripts to automatically detect and remove banners from images, potentially using advanced image processing techniques or deep learning models.
- **Improved Dataset Curation**: Implement additional checks for image quality, including resolution, lighting conditions, and occlusions, to ensure the dataset's utility for training robust machine learning models.
- **Scalability**: Optimize the scraper for efficiency and scalability, allowing for faster downloads and processing of large volumes of images.
- **User Interface**: Develop a user-friendly interface for configuring the scraper's settings, making it accessible to users with varying levels of technical expertise.

## Getting Started
To start using the Car.com Image Scraper, ensure you have Python installed on your system and clone this repository. Navigate to the repository directory and install the required dependencies:

```bash
pip install -r requirements.txt
