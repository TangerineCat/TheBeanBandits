Author: Justin Leong
Based on code by: Edward Johns (e.johns@imperial.ac.uk)
Project Website: http://visual.cs.ucl.ac.uk/pubs/interactiveMachineTeaching/

This code will enable you to perform both teaching and testing, given a set of labelled images.

-----------------------------------------------------------------------------------------------------

This code was based on:

Python v2.7.8 (installed via Anaconda 2.1.0)
Django v1.7

No knowledge of Django is necessary to get the working demo (Butterflies) running.
However, customising it to your specific needs will require basic Python, Django and MySQL knowledge.

-----------------------------------------------------------------------------------------------------

Installation instructions:

1. $ cd Datasets
2. $ python chinese_parser.py
3. $ cd ../machine_teaching
4. $ python manage.py migrate
5. $ python manage.py runserver 0.0.0.0:8000

The working demo should then by opening a browser and entering: A.B.C.D:8000/teacher
Make sure that port 8000 allows data in if you want external access to the website.
You can reset the database by entering: $ python manage.py flush

-----------------------------------------------------------------------------------------------------

Using your own dataset (e.g. a dataset of cats, with 4 classes, each with 50 images)

1. Decide on a name for your dataset (e.g. cats)
2. Create a folder at Datasets/cats
3. Create a 1-by-4 NumPy array at Datasets/cats/class_names.npy, with each element the name of one of the 4 classes
4. Create a 1-by-4 NumPy array at Datasets/cats/class_num_images.npy, with each element the number of images for that class.
5. Create a 50-by-4 NumPy matrix at Datasets/cats/ground_truth.npy, with element (i,j) set to 1 if image i is of class j, otherwise set to 0. 
6. Create a 50-by-50 NumPy matrix at Datasets/cats/weight_matrix.npy, with element (i,j) set to the Gaussian Random Field weight between images i and j. This can be determined by computing the distance in a chosen feature space and then applying an exponential decay.
7. Create a folder at machine_teaching/teacher/static/teacher/images/cats
8. Copy all the images to this folder
9. Create a 1-by-50 NumPy array at Datasets/cats/class_names.npy, with each element the path for that image file. Each element should be prefixed by "teacher/images", e.g. "teacher/images/cats/cat56.jpg"
10. In machine_teaching/teacher/views.py, change line 27 to: dataset_name = 'cats'
11. On this file, lines 29 and 30 then allow you to specify the number of teaching and testing images.

-----------------------------------------------------------------------------------------------------
