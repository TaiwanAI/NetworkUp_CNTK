#!/usr/bin/env python2
# Created: Nov/8/2016
# Author: Kung-hsiang, Huang
# Some of the code in this file is reused from ./democlassifier_webcam.py from openface



import time

start = time.time()

import argparse
import cv2
import os
import pickle
import requests
import numpy as np
np.set_printoptions(precision=2)
from sklearn.mixture import GMM
import openface
from sklearn.svm import SVC
fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')
serverAttendeeRoot = "https://NetworkUp/Attendee"

class Arg:
    def __init__(self, dlibFacePredictor = os.path.join(
            dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"),
    networkModel=os.path.join(
            openfaceModelDir,
            'nn4.small2.v1.t7'),    imgDim = 96, captureDevice = 0, width = 320, height = 240, threshold= 0.5, classifierModel = SVC(kernel = 'rbf', C= 5), cuda = False):
    self.dlibFacePredictor = dlibFacePredictor
    self.networkModel = networkModel
    self.imgDim = imgDim
    self.captureDevice = captureDevice
    self.width = width
    self.height  = height
    self.classifierModel = classifierModel
    self.cuda = cuda

'''
    getRep returns the feature of each faces
'''
def getRep(bgrImg, net):
    start = time.time()
    if bgrImg is None:
        raise Exception("Unable to load image/frame")

    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    

    start = time.time()

    # Get the largest face bounding box
    # bb = align.getLargestFaceBoundingBox(rgbImg) #Bounding box

    # Get all bounding boxes
    bb = align.getAllFaceBoundingBoxes(rgbImg)

    if bb is None:
        # raise Exception("Unable to find a face: {}".format(imgPath))
        return None
    start = time.time()

    alignedFaces = []
    for box in bb:
        alignedFaces.append(
            align.align(
                args.imgDim,
                rgbImg,
                box,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))
    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    start = time.time()

    reps = []
    for alignedFace in alignedFaces:
        reps.append(net.forward(alignedFace))
    # print reps
    return reps

'''
    infer() returns the predicted people in the frame as well as 
    the corresponding information (e.g. summary of shared posts and similarty between he/she and you) stored in server.
'''
def infer(img, args):
    #assume all attendee profile pictures have been downloaded into ./attendee/, with attendee id being file name
    image_list = []
    id_list = []
    for filename in glob.glob('attendee/*.png'): #assuming gif
        im=Image.open(filename)
        id_list.append(filename)
        image_list.append(im)


    net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
    reps = getRep(img, net) #return the detected and aligned faces in the video frame
    persons = []
    infos = []
    similarities = []
    for rep in reps:
        try:
            rep = rep.reshape(1, -1)
        except:
            print "No Face detected"
            return (None, None, None)
        start = time.time()

        for attendee_img in image_list:
            d = rep-getRep(attendee_img, net)
            distances.append(np.dot(d,d))
        # print predictions
        minI = np.argmin(distances) #Returns the indices of the maximum values along an axis.
        attendee_id = id_list[minI]
        url = serverAttendeeRoot + "/" + attendee_id
        r = requests.get(url)
        person = r.json()['name']
        info = r.json()['info']
        similarity = r.json()['similarity']
        persons.append(person)
        infos.append(info)
        similarities.append(similarity)
        
    return (persons, infos,similarities)


if __name__ == '__main__':
    


    args = Arg()

    align = openface.AlignDlib(args.dlibFacePredictor)
    net = openface.TorchNeuralNet(
        args.networkModel,
        imgDim=args.imgDim, cuda = args.cuda)

    # Capture device. Usually 0 will be webcam and 1 will be usb cam.
    video_capture = cv2.VideoCapture(args.captureDevice)
    video_capture.set(3, args.width) 
    video_capture.set(4, args.height) 


    while True:
        ret, frame = video_capture.read()
        persons, infos, similarities = infer(frame, args)
        if persons == None: continue
        for i, value in enumerate(similarities):
            #if the similarities between you and this attendee is greater than 0.7, mark green
            if similarities[i] > 0.7: 
                cv2.putText(frame, "Name: {} Info: {}".format(person, info),
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            #otherwise, mark white
            else:
                cv2.putText(frame, "Name: {} Info: {}".format(person, info),
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.imshow('', frame)
        # quit the program on the press of key 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
