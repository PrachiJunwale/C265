# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')
def load_form():
    return render_template('upload.html')


# Function to upload image and redirect to new webpage
@app.route('/gray', methods=['POST'])   #pass output of program in same html file i.e in the url as “/gray”.
def upload_image():
    file = request.files['file']  #we are referring to input tag(in HTML) named as "file",  to get selected image file on it
    filename = secure_filename(file.filename)  #it is the function of werkzeug library which will check the image and secure the file from the unwanted virus

    file_data = make_grayscale(file.read()) # call function written below
    #below line will oprn static folder and file for write operation
    with open(os.path.join('static/', filename),
              'wb') as f:
        f.write(file_data)

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)  #update message and filename in html file to show it on browser


#class 265
def make_grayscale(input_image):

    image_array = np.fromstring(input_image, dtype='uint8') #np.fromstring() is a numpy function which converts the image into a pixel array.

    print('Image Array:',image_array)

    # decode the array into an image
    #cv2.imdecode() converts the image pixels back to image and compresses it to further apply the required grayscale task on it
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
    print('Decode values of Image:', decode_array_to_img)

    # Make grayscale
    # we will apply the cv2.cvtColor() function of opencv to convert the image into black and white by using cv2.COLOR_RGB2GRAY
    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img) #cv.imencode is used to encodes the original format of the image to maintain its original height and width even after modifying the pixel values 
    print('Status:',status)

    return output_image


@app.route('/display/<filename>')   #need to display the image on the same html file
def display_image(filename):
    return redirect(url_for('static', filename=filename))


# run our Flask Web App locally on localhost. 
if __name__ == "__main__":
    app.run()


