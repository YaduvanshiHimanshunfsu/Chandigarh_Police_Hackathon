import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping, ModelCheckpoint,
    ReduceLROnPlateau
)

# ============================================
# PATHS
# ============================================
DATASET_PATH = r"../../mobilenetV2/dataset"  # Relative to ml/ — adjust if dataset is elsewhere
MODEL_PATH   = r"../backend/models"          # Loads mobilenet_v2_base.h5, saves mobilenet_v2_finetuned.h5

# ============================================
# SETTINGS
# ============================================
IMAGE_SIZE    = (224, 224)
BATCH_SIZE    = 16          # Slightly reduced for stability
FINE_TUNE_EPOCHS = 30       # Additional epochs
# Very small learning rate for fine tuning!
# Too high = destroys existing knowledge!
FINE_TUNE_LR  = 0.00001

# ============================================
# STEP 1 - LOAD EXISTING MODEL
# ============================================
print("="*50)
print("STEP 1 - Loading existing trained model...")
print("="*50)

model = load_model(
    os.path.join(MODEL_PATH, 'best_model.h5')
)
print("Model loaded successfully!")
print(f"Total layers: {len(model.layers)}")

# ============================================
# STEP 2 - UNFREEZE LAST 30 LAYERS
# ============================================
print("\n" + "="*50)
print("STEP 2 - Unfreezing last 30 layers...")
print("="*50)

# First freeze everything
for layer in model.layers:
    layer.trainable = False

# Then unfreeze last 30 layers only
for layer in model.layers[-30:]:
    layer.trainable = True

# Count trainable layers
trainable = sum(
    1 for layer in model.layers
    if layer.trainable
)
print(f"Trainable layers: {trainable}")
print(f"Frozen layers:    {len(model.layers) - trainable}")

# ============================================
# STEP 3 - RECOMPILE WITH LOWER LEARNING RATE
# Very important! Low LR prevents destroying
# what model already learned!
# ============================================
print("\n" + "="*50)
print("STEP 3 - Recompiling with low learning rate...")
print("="*50)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=FINE_TUNE_LR
    ),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
print(f"Learning rate: {FINE_TUNE_LR}")
print("Recompiled successfully!")

# ============================================
# STEP 4 - PREPARE DATA
# ============================================
print("\n" + "="*50)
print("STEP 4 - Preparing data...")
print("="*50)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'train'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'validation'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

test_generator = val_datagen.flow_from_directory(
    os.path.join(DATASET_PATH, 'test'),
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

print(f"Training images:   {train_generator.samples}")
print(f"Validation images: {val_generator.samples}")
print(f"Test images:       {test_generator.samples}")

# ============================================
# STEP 5 - FINE TUNE TRAINING
# ============================================
print("\n" + "="*50)
print("STEP 5 - Fine tuning model...")
print("This will take some time!")
print("="*50)

callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=8,
        restore_best_weights=True,
        verbose=1
    ),
    ModelCheckpoint(
        filepath=os.path.join(
            MODEL_PATH, 'best_model_finetuned.h5'
        ),
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=4,
        min_lr=1e-9,
        verbose=1
    )
]

history = model.fit(
    train_generator,
    epochs=FINE_TUNE_EPOCHS,
    validation_data=val_generator,
    callbacks=callbacks,
    verbose=1
)

# ============================================
# STEP 6 - EVALUATE
# ============================================
print("\n" + "="*50)
print("STEP 6 - Evaluating fine tuned model...")
print("="*50)

test_loss, test_accuracy = model.evaluate(
    test_generator,
    verbose=1
)

print(f"\nFine Tuned Test Accuracy: {test_accuracy*100:.2f}%")
print(f"Fine Tuned Test Loss:     {test_loss:.4f}")

# ============================================
# STEP 7 - DETAILED REPORT
# ============================================
print("\n" + "="*50)
print("STEP 7 - Detailed report...")
print("="*50)

predictions       = model.predict(test_generator)
predicted_classes = (predictions > 0.5).astype(int)
true_classes      = test_generator.classes

print("\nClassification Report:")
print(classification_report(
    true_classes,
    predicted_classes,
    target_names=['Genuine', 'Tampered']
))

cm = confusion_matrix(true_classes, predicted_classes)
print("Confusion Matrix:")
print(cm)
print(f"\nTrue Negatives  (Genuine correctly identified):  {cm[0][0]}")
print(f"False Positives (Genuine wrongly flagged):        {cm[0][1]}")
print(f"False Negatives (Tampered missed):                {cm[1][0]}")
print(f"True Positives  (Tampered correctly caught):      {cm[1][1]}")

# ============================================
# STEP 8 - COMPARE WITH PREVIOUS MODEL
# ============================================
print("\n" + "="*50)
print("STEP 8 - Comparison with previous model...")
print("="*50)
print(f"Previous accuracy: 69.70%")
print(f"Fine tuned accuracy: {test_accuracy*100:.2f}%")
improvement = (test_accuracy*100) - 69.70
print(f"Improvement: +{improvement:.2f}%")

# ============================================
# STEP 9 - SAVE GRAPHS
# ============================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(history.history['accuracy'],     label='Training')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Fine Tuning Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()

ax2.plot(history.history['loss'],     label='Training')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Fine Tuning Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()

graph_path = os.path.join(
    MODEL_PATH, 'finetuning_graphs.png'
)
plt.savefig(graph_path)
print(f"\nGraphs saved to: {graph_path}")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*50)
print("FINE TUNING COMPLETE!")
print("="*50)
print(f"\nBest model saved: {MODEL_PATH}\\best_model_finetuned.h5")
print(f"Previous accuracy:    69.70%")
print(f"Fine tuned accuracy:  {test_accuracy*100:.2f}%")

if test_accuracy >= 0.90:
    print("🎉 Excellent! Model is ready for deployment!")
elif test_accuracy >= 0.80:
    print("✅ Good improvement! Model ready for Flask app!")
elif test_accuracy >= 0.70:
    print("📈 Some improvement! Consider Google Colab for more!")
else:
    print("⚠️ No improvement — try adjusting layers unfrozen!")