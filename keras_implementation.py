import matplotlib.pyplot as plt
import keras_ocr
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path

#Loaded path to file to be converted from env
load_dotenv()

#Save file to property
path = os.getenv('FILE_READ_PATH')

pages = convert_from_path(path)


# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# Get a set of three example images
images = [
    keras_ocr.tools.read(pages)
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)