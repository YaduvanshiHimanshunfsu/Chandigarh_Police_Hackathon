import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import (
    Dense, GlobalAveragePooling2D,
    Dropout, BatchNormalization
)
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint,
    ReduceLROnPlateau
)

# ============================================
# PATHS
# ============================================
DATASET_PATH = r"../../mobilenetV2/dataset"  # Relative to ml/ — adjust if dataset is elsewhere
MODEL_PATH   = r"../backend/models"          # Output: mobilenet_v2_base.h5 lands here

# Create model folder
os.makedirs(MODEL_PATH, exist_ok=True)

# ============================================
# SETTINGS
# ============================================
IMAGE_SIZE  = (224, 224)  # MobileNetV2 input size
BATCH_SIZE  = 32          # Images per training batch
EPOCHS      = 50          # Maximum training rounds
LEARNING_RATE = 0.0001    # How fast model learns

# ============================================
# STEP 1 - PREPARE DATA
# Data Augmentation = create variations
# of training images to prevent overfitting!
# ============================================
print("="*50)
print("STEP 1 - Preparing data...")
print("="*50)

# Training data with augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,          # Normalize 0-255 to 0-1
    rotation_range=10,       # Rotate slightly
    width_shift_range=0.1,   # Shift horizontally
    height_shift_range=0.1,  # Shift vertically
    shear_range=0.1,         # Shear slightly
    zoom_range=0.1,          # Zoom slightly
    horizontal_flip=True,    # Flip horizontally
    fill_mode='nearest'      # Fill empty pixels
)

# Validation and test data
# NO augmentation — just normalize!
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training images
train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',     # 2 classes: genuine/tampered
    shuffle=True
)

# Load validation images
val_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'validation'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

# Load test images
test_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'test'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

print(f"\nClass mapping: {train_generator.class_indices}")
print(f"Training images:   {train_generator.samples}")
print(f"Validation images: {val_generator.samples}")
print(f"Test images:       {test_generator.samples}")

# ============================================
# STEP 2 - BUILD MODEL
# Use MobileNetV2 as base
# Add our own detection layers on top!
# ============================================
print("\n" + "="*50)
print("STEP 2 - Building model...")
print("="*50)

# Load MobileNetV2 with ImageNet weights
# include_top=False means we add our own top!
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze base model layers first
# Don't change what MobileNetV2 already knows!
base_model.trainable = False

# ----------------------------------------
# Add our custom detection layers on top
# ----------------------------------------
x = base_model.output

# GlobalAveragePooling reduces to 1D
x = GlobalAveragePooling2D()(x)

# Dense layer learns tamper patterns
x = Dense(256, activation='relu')(x)

# BatchNormalization stabilizes training
x = BatchNormalization()(x)

# Dropout prevents overfitting (30%)
x = Dropout(0.3)(x)

# Another dense layer
x = Dense(128, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)

# Final output layer
# Sigmoid = outputs 0 to 1 probability
output = Dense(1, activation='sigmoid')(x)

# Create complete model
model = Model(
    inputs=base_model.input,
    outputs=output
)

print(f"Model built successfully!")
print(f"Total layers: {len(model.layers)}")

# ============================================
# STEP 3 - COMPILE MODEL
# Tell model HOW to learn!
# ============================================
print("\n" + "="*50)
print("STEP 3 - Compiling model...")
print("="*50)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=LEARNING_RATE
    ),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Model compiled!")

# ============================================
# STEP 4 - SET UP CALLBACKS
# These monitor training and help!
# ============================================
callbacks = [

    # Stop training if no improvement for 10 epochs
    EarlyStopping(
        monitor='val_accuracy',
        patience=10,
        restore_best_weights=True,
        verbose=1
    ),

    # Save best model automatically
    ModelCheckpoint(
        filepath=os.path.join(MODEL_PATH, 'best_model.h5'),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),

    # Reduce learning rate if stuck
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-7,
        verbose=1
    )
]

# ============================================
# STEP 5 - TRAIN MODEL
# ============================================
print("\n" + "="*50)
print("STEP 5 - Training model...")
print("This will take some time!")
print("="*50)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=callbacks,
    verbose=1
)

# ============================================
# STEP 6 - EVALUATE ON TEST SET
# Final honest score!
# ============================================
print("\n" + "="*50)
print("STEP 6 - Evaluating on test set...")
print("="*50)

test_loss, test_accuracy = model.evaluate(
    test_generator,
    verbose=1
)

print(f"\nTest Accuracy: {test_accuracy*100:.2f}%")
print(f"Test Loss:     {test_loss:.4f}")

# ============================================
# STEP 7 - DETAILED REPORT
# ============================================
print("\n" + "="*50)
print("STEP 7 - Detailed classification report...")
print("="*50)

# Get predictions
predictions = model.predict(test_generator)
predicted_classes = (predictions > 0.5).astype(int)
true_classes = test_generator.classes

print("\nClassification Report:")
print(classification_report(
    true_classes,
    predicted_classes,
    target_names=['Genuine', 'Tampered']
))

print("\nConfusion Matrix:")
cm = confusion_matrix(true_classes, predicted_classes)
print(cm)
print(f"\nTrue Negatives  (Genuine correctly identified):  {cm[0][0]}")
print(f"False Positives (Genuine wrongly flagged):        {cm[0][1]}")
print(f"False Negatives (Tampered missed):                {cm[1][0]}")
print(f"True Positives  (Tampered correctly caught):      {cm[1][1]}")

# ============================================
# STEP 8 - SAVE TRAINING GRAPHS
# ============================================
print("\n" + "="*50)
print("STEP 8 - Saving training graphs...")
print("="*50)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Accuracy graph
ax1.plot(history.history['accuracy'],     label='Training')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Model Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()

# Loss graph
ax2.plot(history.history['loss'],     label='Training')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Model Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()

graph_path = os.path.join(MODEL_PATH, 'training_graphs.png')
plt.savefig(graph_path)
print(f"Graphs saved to: {graph_path}")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*50)
print("TRAINING COMPLETE!")
print("="*50)
print(f"\nBest model saved to: {MODEL_PATH}\\best_model.h5")
print(f"Training graphs:     {MODEL_PATH}\\training_graphs.png")
print(f"\nFinal Test Accuracy: {test_accuracy*100:.2f}%")

if test_accuracy >= 0.90:
    print("🎉 Excellent! Model is ready for deployment!")
elif test_accuracy >= 0.80:
    print("✅ Good model! Can be improved with more data!")
else:
    print("⚠️ Model needs improvement — consider more training data!")