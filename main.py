import os
from operator import itemgetter
from time import sleep

from picamera import PiCamera
from PIL import Image
import RPi.GPIO as GPIO

from model import TFLiteModel
from settings import IMAGE_PATH, LABELS

def capture():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture(IMAGE_PATH)
    camera.stop_preview()


def predict():
    if not os.path.isfile(IMAGE_PATH):
        raise ValueError('Path is not a file')

    image = Image.open(IMAGE_PATH)
    model = TFLiteModel(os.getcwd())
    model.load()

    return model.predict(image)

def set_GPIO(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Using same pins as outlined on Haris' tutorial 
    # LED turning off after 3 seconds

def LED(waste_material): 
    set_GPIO()
    if waste_material == "plastic": 
        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(18, GPIO.LOW)
    elif waste_material == "e-waste":
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(17, GPIO.LOW)
    elif waste_material == "glass":
        GPIO.setup(22, GPIO.OUT)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(22, GPIO.LOW)
    elif waste_material == "cardboard":
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(27, GPIO.LOW)
    elif waste_material == "trash":
        GPIO.setup(5, GPIO.OUT)
        GPIO.output(5, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(5, GPIO.LOW)
    elif waste_material == "paper":
        GPIO.setup(6, GPIO.OUT)
        GPIO.output(6, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(6, GPIO.LOW)
    elif waste_material == "metal":
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(16, GPIO.LOW)


def main():
    capture()

    try:
        outputs = predict()
    except ValueError:
        print(f'Couldn\'t find image file')
        return

    predictions = outputs['predictions']
    max_low_label = max(predictions, key=itemgetter('confidence'))['label']
    high_label = LABELS[max_low_label]

    print(f'Predicted: {high_label}')
    LED(high_label)

if __name__ == '__main__':
    main()
