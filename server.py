from flask import Flask, request, render_template, abort
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import numpy as np
from waitress import serve

app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # SERVER-SIDE VALIDATION
    # Check if a file was uploaded
    if 'image' not in request.files:
        abort(400, 'No file uploaded.')

    file = request.files['image']

    # Check if the file is one of the allowed types/extensions
    if file.filename == '':
        abort(400, 'No selected file.')

    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'jpeg', 'jpg', 'png', 'webp'}):
        abort(400, 'Allowed image types are -> jpeg, jpg, png, webp')
    # END OF SERVER-SIDE VALIDATION

    # Read the uploaded image file
    image_file = file.read()

    # Convert image bytes to numpy array
    nparr = np.frombuffer(image_file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Perform object detection
    bbox, label, conf = cv.detect_common_objects(
        img, confidence=0.2, model='yolov3-tiny')

    # Draw bounding boxes and labels on the image
    output_image = draw_bbox(img, bbox, label, conf)

    # Save the output image to the static/outputs directory
    cv2.imwrite('static/outputs/output.jpg', output_image)

    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
