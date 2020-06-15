# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import time
import datetime
from awsfileshare import upload_to_aws
from sendmsg import sendmessage 
import cv2

encodings='./encodings.pickle'


consec = ["Unknown","sree","mohanlal"]
consecc=[35,35,35]
lastSent = None

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open('encodings.pickle', "rb").read())

# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(0).start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()
	intruder = False
	names = []

	timestamp = datetime.datetime.now()
	ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")

	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=750)
	r = frame.shape[1] / float(rgb.shape[1])

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame, then compute
	# the facial embeddings for each face
	boxes = face_recognition.face_locations(rgb,model='hog')
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],encoding)
		name = "Unknown"
		# check to see if we have found a match
		if True in matches:

			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched

			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)

		
		names.append(name)
	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
		top = int(top * r)
		right = int(right * r)
		bottom = int(bottom * r)
		left = int(left * r)
		for name in names:
			if names == None :
				break
			i=consec.index(name)
			if consecc[i]==35 :
				imgname=name
				imglocalfilename = imgname + str(timestamp) + ".jpeg"
				cv2.imwrite("uploadtos3/" + imglocalfilename,frame)
				url = upload_to_aws("uploadtos3/" + imglocalfilename, 'projectasiet', imglocalfilename)
				consecc[i]=0
				if name=="Unknown" :
					sendmessage(url)
			elif consecc[i]!=80:
				consecc[i]=consecc[i]+1
			else:
				continue
	cv2.imshow("Frame", frame)
	k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    	if k == 27:
        	break
		
cv2.destroyAllWindows()
vs.stop()
