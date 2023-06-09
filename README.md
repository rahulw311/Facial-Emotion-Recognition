# Facial Emotion Recognition (FER)
Suggestions for Music Using Facial Emotion Recognition

This is a project on Facial Emotion Recognition. This has been implemented using OpenCV for face detection and feature extraction along with the the FisherFaces algorithm.
FisherFaces is an improvement over EigenFaces and uses Principal Component Analysis (PCA) and Linear Discriminant Analysis (LDA). This algorithm follows the concept that all the parts of face are not equally important or useful for face recognition. When we look at a face we look at the places of maximum variation so that we can recognise that person. For example from nose to eyes there is a huge variation in everyone's face. Fisherfaces algorithm extracts principle components that separates one individual from another. So, now an individual's features can't dominate another person's features.

The CK+ dataset has been used in this case as our training dataset. It can be found at the link- https://www.kaggle.com/datasets/shawon10/ckplus

This dataset contains images on 7 emotions- anger, contempt, disgust, fear, happy, sadness and surprise. However in the case of this project for the sake of simplicity only 4 emotions are considered - anger, sadness, happy and a 4th feeling was described as neutral.

The model also has a function which if run, can be used to continually add images to the training data in order to increase the accuracy of the model over time.

I have also provided a pre-trained model in the files which can be loaded as well.

A simple GUI has been designed using tkinter to act as the front end of this application.

As for the music, I have defined a .xlsx sheet where a list of songs was populated with links to the files on the system for each of the 4 emotions mentioned above which would then be shuffled and added to the queue to be run. (Not uploaded by me and has to be done manually when sourcing the code).

Please download all the necessary libraries and dependencies before using the project.

A detailed report can be found on this project in the documents as well.
