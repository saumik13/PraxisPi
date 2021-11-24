import os
from operator import itemgetter
from time import sleep

from picamera import PiCamera
from PIL import Image
import RPi.GPIO as GPIO

from model import TFLiteModel
from settings import IMAGE_PATH, LABELS, LED_ACTIVATION_TIME, PINS


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


def LED(high_label):
    set_GPIO()

    pin = PINS[high_label]

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    sleep(LED_ACTIVATION_TIME)
    GPIO.output(pin, GPIO.LOW)


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
