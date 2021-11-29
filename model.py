import json
import os

import numpy as np
import tflite_runtime.interpreter as tflite

EXPORT_MODEL_VERSION = 1


class WasteModel:
    def __init__(self):
        with open(os.path.join(model_dir, 'signature.json'), 'r') as f:
            self.signature = json.load(f)

        self.model_file = os.path.join(
            model_dir, self.signature.get('filename'),
        )

        self.interpreter = tflite.Interpreter(model_path=self.model_file)
        self.interpreter.allocate_tensors()

        signature_inputs = self.signature.get('inputs')
        signature_outputs = self.signature.get('outputs')

        input_details = {
            detail.get('name'): detail
            for detail in self.interpreter.get_input_details()
        }
        self.model_inputs = {
            key: {**sig, **input_details.get(sig.get('name'))}
            for key, sig in signature_inputs.items()
        }
        output_details = {
            detail.get('name'): detail
            for detail in self.interpreter.get_output_details()
        }
        self.model_outputs = {
            key: {**sig, **output_details.get(sig.get('name'))}
            for key, sig in signature_outputs.items()
        }

    def predict(self, image):
        input_data = self.process_image(
            image, self.model_inputs.get('Image').get('shape'),
        )

        self.interpreter.set_tensor(
            self.model_inputs.get('Image').get('index'), input_data,
        )
        self.interpreter.invoke()

        outputs = {
            key: self.interpreter.get_tensor(value.get('index')).tolist()[0]
            for key, value in self.model_outputs.items()
        }

        return self.process_output(outputs)

    def process_image(self, image, input_shape):
        width, height = image.size

        if image.mode != 'RGB':
            image = image.convert('RGB')

        if width != height:
            square_size = min(width, height)
            left = (width - square_size) / 2
            top = (height - square_size) / 2
            right = (width + square_size) / 2
            bottom = (height + square_size) / 2

            image = image.crop((left, top, right, bottom))

        input_width, input_height = input_shape[1:3]

        if image.width != input_width or image.height != input_height:
            image = image.resize((input_width, input_height))

        image = np.asarray(image) / 255.0

        return image.reshape(input_shape).astype(np.float32)

    def process_output(self, outputs):
        out_keys = ['label', 'confidence']

        for key, val in outputs.items():
            if isinstance(val, bytes):
                outputs[key] = val.decode()

        confs = list(outputs.values())[0]
        labels = self.signature.get('classes').get('Label')
        output = [dict(zip(out_keys, group)) for group in zip(labels, confs)]

        return output
