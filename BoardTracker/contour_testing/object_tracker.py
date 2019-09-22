# USAGE
# python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
from centroidtracker import CentroidTracker
from CircuitBoardTrackingTesting import show, findRect
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from PIL import Image

import numpy as np
import os
import imutils


def run_inference_for_single_image(image, graph):
    if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

    # Run inference
    output_dict = sess.run(tensor_dict,
                            feed_dict={image_tensor: np.expand_dims(image, 0)})

    # all outputs are float32 numpy arrays, so convert types as appropriate
    output_dict['num_detections'] = int(output_dict['num_detections'][0])
    output_dict['detection_classes'] = output_dict[
        'detection_classes'][0].astype(np.uint8)
    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
    output_dict['detection_scores'] = output_dict['detection_scores'][0]
    if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
    return output_dict

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)

# load our serialized model from disk
print("[INFO] loading model...")
#net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# net = cv2.dnn.readNetFromTensorflow("./frozen_inference_graph.pb", "./label_map.pbtxt")
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
test = cv2.imread("board.jpg")

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(2.0)

width = None
height = None
count = 0

# loop over the frames from the video stream
while True:
    # read the next frame from the video stream and resize it
    frame = vs.read()

    # if the frame dimensions are None, grab them
    if W is None or H is None:
        (H, W) = frame.shape[:2]

	# construct a blob from the frame, pass it through the network,
	# obtain our output predictions, and initialize the list of
	# bounding box rectangles
    # blob = cv2.dnn.blobFromImage(frame, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    # print ("HI")
    # net.setInput(blob)
    # detections = net.forward()
    rects = findRect(frame)


    # # loop over the detections
    # for i in range(0, detections.shape[2]):
    #     # filter out weak detections by ensuring the predicted
    #     # probability is greater than a minimum threshold
    #     if detections[0, 0, i, 2] > 0.5:
    #         # compute the (x, y)-coordinates of the bounding box for
    #         # the object, then update the bounding box rectangles list
    #         box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
    #         rects.append(box.astype("int"))
    #         # draw a bounding box surrounding the object so we can
    #         # visualize it
    #         (startX, startY, endX, endY) = box.astype("int")
    #         cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    print (rects)
    # update our centroid tracker using the computed set of bounding box rectangles
    flag = False
    if len(rects) == 1:
        (startX, startY, endX, endY) = rects[0]
        if width == None:
            width = abs(endX - startX)
            height = abs(endY - startY)
        elif count <= 50:
            width = (abs(endX - startX) + width) // 2
            height = (abs(endY - startY) + height) // 2
        else:
            test = cv2.resize(test, (width, height))
            cX = int((startX + endX) / 2.0)
            cY = int((startY + endY) / 2.0)
            #cop = frame.copy()
            #cop[:] = (255,255,255)
            #cop[int(cY - height/2):int(cY - height/2) + height, int(cX - width/2):int(cX - width/2) + width] = test
            #flag = True
            cop = frame.copy()
            cop[:] = (255, 255, 255)
            center = (cX, cY)
            size = (width, height)
            angle = 45.0
            scale = 0.5
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
            img_dst = cv2.warpAffine(cop, rotation_matrix, size,
			                         flags=cv2.INTER_LINEAR,
			                         borderMode=cv2.BORDER_TRANSPARENT)
            cv2.imshow("hi", cv2.cvtColor(img_dst, cv2.COLOR_BGRA2RGBA))



    #rects = findRect(frame)
    objects = ct.update(rects)
    # loop over the tracked objects
    for (objectID, centroid) in objects.items():
        # draw both the ID of the object and the centroid of the
        # object on the output frame
        text = "ID {}".format(objectID)
        cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)


    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    count += 1
    if flag:
        show("board", cop, False, True)


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()