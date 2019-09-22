import numpy as np
import os
import imutils

import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image


from models.research.object_detection.utils import label_map_util

from models.research.object_detection.utils import visualization_utils as vis_util

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

MODEL_NAME = 'inference_graph'
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = 'training/label_map.pbtxt'

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)


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

import cv2
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, 40) 
try:
    with detection_graph.as_default():
        with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                  'num_detections', 'detection_boxes', 'detection_scores',
                  'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                      tensor_name)
                count = 0
                width = None
                height = None
                while True:
                    ret, image_np = cap.read()
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    # Actual detection.
                    output_dict = {}
                    output_dict = run_inference_for_single_image(image_np, detection_graph)
                    # Visualization of the results of a detection.
                    # vis_util.visualize_boxes_and_labels_on_image_array(
                    #     image_np,
                    #     output_dict['detection_boxes'],
                    #     output_dict['detection_classes'],
                    #     output_dict['detection_scores'],
                    #     category_index,
                    #     instance_masks=output_dict.get('detection_masks'),
                    #     use_normalized_coordinates=True,
                    #     line_thickness=8)
                    (H,W) = image_np.shape[:2]
                    (ymin, xmin, ymax, xmax) = output_dict['detection_boxes'][0]
                    (startX, endX, startY, endY) = (xmin * W, xmax * W, 
                              ymin * H, ymax * H)
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
			            angle = 0
			            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
			            img_dst = cv2.warpAffine(cop, rotation_matrix, cop.shape[:2],
						                         flags=cv2.INTER_LINEAR,
						                         borderMode=cv2.BORDER_TRANSPARENT)
			            cv2.imshow("hi", cv2.cvtColor(img_dst, cv2.COLOR_BGRA2RGBA))


                    cv2.imshow('object_detection', image_np)


                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                    count += 1
except Exception as e:
    print(e)
    cap.release()


