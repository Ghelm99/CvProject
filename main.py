import cv2

# Neural network
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size = (416, 416), scale=1/255)

# Classes
classes = []
with open("dnn_model/classes.txt", "r") as file_object:
  for class_name in file_object.readlines():
    class_name = class_name.strip()
    classes.append(class_name)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Object detection
while True:
  ret, frame = capture.read()
  
  (class_ids, scores, bboxes) = model.detect(frame) 
  
  for class_id, score, bbox in zip(class_ids, scores, bboxes):
    (x, y, w, h) = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(frame, str(classes[class_id]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
  cv2.imshow('Webcam', frame)
  if cv2.waitKey(1) == ord('q'):
    break
  
capture.release()
cv2.destroyAllWindows()


