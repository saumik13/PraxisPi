import os
from operator import itemgetter
from time import sleep

from picamera import PiCamera
from PIL import Image

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


def main():
    capture()

    try:
        outputs = predict()
    except ValueError:
        print(f'Couldn\'t find image file')
        return

    predictions = outputs['predictions']
    max_label = max(predictions, key=itemgetter('confidence'))['label']
    label = LABELS[max_label]

    print(f'Predicted: {label}')


if __name__ == '__main__':
    main()
