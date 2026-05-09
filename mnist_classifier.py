"""
CCS 2226 – Foundations of AI  |  Task One: MNIST Dataset
=========================================================
(a) Download and load the MNIST dataset
(b) Train a classifier to distinguish digits 0–9

Requirements:
    pip install tensorflow matplotlib numpy scikit-learn

Run:
    python mnist_classifier.py
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# ─────────────────────────────────────────────
# (a) DOWNLOAD & LOAD THE MNIST DATASET
# ─────────────────────────────────────────────
print("=" * 60)
print("  CCS 2226  |  Task One – MNIST Digit Classifier")
print("=" * 60)

print("\n[1/5]  Downloading MNIST dataset …")

# Keras downloads MNIST automatically (~11 MB) on first run
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

print(f"       Training samples : {X_train.shape[0]:,}")
print(f"       Test samples     : {X_test.shape[0]:,}")
print(f"       Image shape      : {X_train.shape[1:]}  (28 × 28 pixels, grayscale)")
print(f"       Classes          : digits 0 – 9")

# ─────────────────────────────────────────────
# VISUALISE SAMPLE IMAGES
# ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 10, figsize=(16, 4))
fig.suptitle("MNIST – Sample Images (one per digit class)", fontsize=14, fontweight='bold')

for digit in range(10):
    # Pick first training image for this digit
    idx = np.where(y_train == digit)[0][0]
    for row in range(2):
        ax = axes[row, digit]
        if row == 0:
            ax.imshow(X_train[np.where(y_train == digit)[0][row]], cmap='gray')
        else:
            ax.imshow(X_train[np.where(y_train == digit)[0][1]], cmap='gray')
        ax.set_title(f"Digit {digit}", fontsize=9)
        ax.axis('off')

plt.tight_layout()
plt.savefig("mnist_samples.png", dpi=150, bbox_inches='tight')
plt.show()
print("       Saved → mnist_samples.png")

# ─────────────────────────────────────────────
# (b) PRE-PROCESS DATA
# ─────────────────────────────────────────────
print("\n[2/5]  Pre-processing …")

# Normalise pixel values from [0, 255] to [0.0, 1.0]
X_train = X_train.astype("float32") / 255.0
X_test  = X_test.astype("float32")  / 255.0

# Reshape: add channel dimension → (samples, 28, 28, 1)
X_train = X_train[..., np.newaxis]
X_test  = X_test[..., np.newaxis]

# One-hot encode labels  e.g.  3  →  [0,0,0,1,0,0,0,0,0,0]
y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat  = keras.utils.to_categorical(y_test,  10)

print(f"       X_train shape    : {X_train.shape}")
print(f"       X_test  shape    : {X_test.shape}")

# ─────────────────────────────────────────────
# BUILD THE CNN MODEL
# ─────────────────────────────────────────────
print("\n[3/5]  Building Convolutional Neural Network …")

model = keras.Sequential([
    # --- Block 1 ---
    keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                        input_shape=(28, 28, 1), name='conv1'),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Dropout(0.25),

    # --- Block 2 ---
    keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2'),
    keras.layers.BatchNormalization(),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Dropout(0.25),

    # --- Fully-connected head ---
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='softmax', name='output')   # 10 classes
], name="MNIST_CNN")

model.summary()

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ─────────────────────────────────────────────
# TRAIN
# ─────────────────────────────────────────────
print("\n[4/5]  Training …")

early_stop = keras.callbacks.EarlyStopping(
    monitor='val_accuracy', patience=3, restore_best_weights=True
)

history = model.fit(
    X_train, y_train_cat,
    epochs=15,
    batch_size=128,
    validation_split=0.1,
    callbacks=[early_stop],
    verbose=1
)

# ─────────────────────────────────────────────
# EVALUATE
# ─────────────────────────────────────────────
print("\n[5/5]  Evaluating on test set …")

test_loss, test_acc = model.evaluate(X_test, y_test_cat, verbose=0)
print(f"\n       Test Accuracy : {test_acc * 100:.2f}%")
print(f"       Test Loss    : {test_loss:.4f}")

# Detailed classification report
y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
print("\n── Per-class classification report ──────────────────")
print(classification_report(y_test, y_pred,
                             target_names=[f"Digit {i}" for i in range(10)]))

# ─────────────────────────────────────────────
# PLOT TRAINING HISTORY
# ─────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle("Training History", fontsize=14, fontweight='bold')

ax1.plot(history.history['accuracy'],     label='Train')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(history.history['loss'],     label='Train')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("training_history.png", dpi=150, bbox_inches='tight')
plt.show()
print("       Saved → training_history.png")

# ─────────────────────────────────────────────
# CONFUSION MATRIX
# ─────────────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=range(10), yticklabels=range(10))
plt.title("Confusion Matrix – Test Set", fontsize=14, fontweight='bold')
plt.xlabel("Predicted Digit")
plt.ylabel("True Digit")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches='tight')
plt.show()
print("       Saved → confusion_matrix.png")

# ─────────────────────────────────────────────
# VISUALISE PREDICTIONS
# ─────────────────────────────────────────────
fig, axes = plt.subplots(3, 10, figsize=(18, 6))
fig.suptitle("Model Predictions on Test Images  ✓ correct  ✗ wrong",
             fontsize=13, fontweight='bold')

shown = {d: 0 for d in range(10)}
col = 0
for i in range(len(X_test)):
    true  = y_test[i]
    pred  = y_pred[i]
    if shown[true] == 0 and col < 10:
        for row_offset, img_idx in enumerate(
            [np.where(y_test == true)[0][j] for j in range(3)]
        ):
            ax = axes[row_offset, true]
            ax.imshow(X_test[img_idx, :, :, 0], cmap='gray')
            p = y_pred[img_idx]
            correct = (p == true)
            colour  = 'green' if correct else 'red'
            symbol  = '✓' if correct else '✗'
            ax.set_title(f"True:{true}  Pred:{p} {symbol}",
                         fontsize=7, color=colour)
            ax.axis('off')
        shown[true] = 1
        col += 1
    if col == 10:
        break

plt.tight_layout()
plt.savefig("predictions.png", dpi=150, bbox_inches='tight')
plt.show()
print("       Saved → predictions.png")

# ─────────────────────────────────────────────
# SAVE MODEL
# ─────────────────────────────────────────────
model.save("mnist_cnn_model.keras")
print("\n  Model saved → mnist_cnn_model.keras")
print("\n" + "=" * 60)
print("  Task One complete. All outputs saved.")
print("=" * 60)
