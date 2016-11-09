import numpy as np
import requests
import math



class ComparisonHelper:
	
	'''
		The compare function in this class collects user data from getUrl, calculates the similarity with
		the help of a sigmoid function, which returns a value between 0 and 1, and posts the data to
		postUrl
	'''
	def compare(self, getUrl, postUrl userId):
		r = requests.get(url)		
		#each feature will have value -1 or 1. The features are marked 1 if the attendee possesses this feature (e.g. art)
		featuresList = r.json()['features']
		attendeeIdList = r.json()['id']
		similarityList = []
		userIdIndex = None

		#this loop get the userIdIndex
		for i, attendeeId in enumerate(attendeeIdList):
			if attendeeIdList[i] == userId: 
				userIdIndex = attendeeId
				break

		if userIdIndex == None:
			print "Error! You have not registered this event yet!"
			return

		#transform to np array for inner product
		userFeatures = np.asarray(featuresList[userIdIndex])

		for i, attendeeId in enumerate(attendeeIdList):
			if attendeeId == userId: continue
			attendeeFeatures = np.asarray(featuresList[i])
			difference = np.inner(userFeatures, attendeeFeatures)
			similarity = sigmoid(difference) #return similarity value between 0/1
			similarityList.append(similarity)

		for i in len(featuresList):
			features = featuresList[i]
			attendeeId = attendeeIdList[i]
			similarity = similarityList[i]
			data = {}
			data['features'] = features
			data['attendeeId'] = attendeeId
			data['similarity'] = similarity
			r = requests.post(postUrl, data)

def sigmoid(z):
	return 1/(1+ math.exp(-z)) 