import os
from time import sleep

from picamera import PiCamera
from PIL import Image

from model import TFLiteModel

IMAGE_PATH = './temp.jpg'


def capture():
    camera = PiCamera()
    camera.start_preview()
    sleep(5)
    camera.capture(IMAGE_PATH)
    camera.stop_preview()


def predict():
    model_dir = os.getcwd()

    if os.path.isfile(IMAGE_PATH):
        image = Image.open(IMAGE_PATH)
        model = TFLiteModel(model_dir)
        model.load()
        outputs = model.predict(image)
        print(f"Predicted: {outputs}")
    else:
        print(f"Couldn't find image file {args.image}")


def main():
    capture()
    predict()
    
    
if __name__ == '__main__':
    main()
