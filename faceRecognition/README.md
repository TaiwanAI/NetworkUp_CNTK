Guidance
=============

This feature is based on OpenFace(https://cmusatyalab.github.io/openface/)


### How it works

This feature contains two functions, getRep and infer. The first function identifies faces in the image, and perform forward network pass to extract a vector of features of the image, while the second one uses these features to compare the detected faces and the faces stored in the database and find the best match. After these two procedures, the returned information will be displayed on the frame in real-time with attendee of over 70% similarity with the user marked green, otherwise marked white.
