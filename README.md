# Watchbot
A deep learning based surveillance system
build using dlib resnet and face_recognition library.

Code is done in python.

Execution commands:

1.python gather.py #gathers face examples from live video. Threshold has been set to 30 therefore collect around 30 images by segmenting frames from video and saves them to dataset folder inside subfolder

2.python encode_faces.py #makes face encodings of the faces in th dataset and saves them to encodings.pickle file

3.python recognize.py #recognizes faces in live stream. If face does not exist in dataset sends sms and uploads to aws s3. if face is in dataset uploads to aws s3.
