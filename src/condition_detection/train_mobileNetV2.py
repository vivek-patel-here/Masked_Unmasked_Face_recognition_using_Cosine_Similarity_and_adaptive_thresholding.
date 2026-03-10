import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
        print("Using Apple Metal GPU")
    except:
        pass
else:
    print("Running on CPU")


DATASET_PATH = "Data/mask_dataset"

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)


base = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

x = base.output
x = GlobalAveragePooling2D()(x)
output = Dense(2, activation="softmax")(x)

model = Model(inputs=base.input, outputs=output)


for layer in base.layers:
    layer.trainable = False

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


with tf.device('/GPU:0'):
    model.fit(
        train,
        validation_data=val,
        epochs=10
    )


model.save("models/mask_detector.keras")
print("Mask detector model saved.")