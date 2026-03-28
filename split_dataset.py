import os
import shutil
import random

# Original dataset location
source_dir = "datasets/dataset-resized"

# Output dataset for YOLO
train_dir = "datasets_split/train"
val_dir = "datasets_split/val"

# Train/validation split
split_ratio = 0.8

classes = os.listdir(source_dir)

for cls in classes:

    cls_path = os.path.join(source_dir, cls)

    if not os.path.isdir(cls_path):
        continue

    images = os.listdir(cls_path)
    random.shuffle(images)

    split_index = int(len(images) * split_ratio)

    train_images = images[:split_index]
    val_images = images[split_index:]

    os.makedirs(os.path.join(train_dir, cls), exist_ok=True)
    os.makedirs(os.path.join(val_dir, cls), exist_ok=True)

    for img in train_images:
        src = os.path.join(cls_path, img)
        dst = os.path.join(train_dir, cls, img)
        shutil.copy(src, dst)

    for img in val_images:
        src = os.path.join(cls_path, img)
        dst = os.path.join(val_dir, cls, img)
        shutil.copy(src, dst)

print("Dataset split completed successfully")
