import os
from operator import itemgetter
from time import sleep

from picamera import PiCamera
from PIL import Image
from RPi import GPIO

from model import TFLiteModel
from settings import IMAGE_PATH, LABELS, LED_ACTIVATION_TIME, PINS, BUTTON_PIN


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


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    for pin in PINS.values():
        GPIO.setup(pin, GPIO.OUT)


def LED(pin):
    GPIO.output(pin, GPIO.HIGH)
    sleep(LED_ACTIVATION_TIME)
    GPIO.output(pin, GPIO.LOW)


def main():
    setup()

    while True:
        input_state = GPIO.input(BUTTON_PIN)

        if not input_state:
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
            LED(PINS[high_label])
            sleep(2)


if __name__ == '__main__':
    main()
