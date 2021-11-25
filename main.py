import os
from operator import itemgetter
from time import sleep

from picamera import PiCamera
from PIL import Image
from RPi import GPIO

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

def set_button(PIN): 
    GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)




def main():

    set_button(PIN_NUMBER)
    while True:
        input_state = GPIO.input(PIN_NUMBER)
        if input_state == False:
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
            time.sleep(2)

if __name__ == '__main__':
    main()
