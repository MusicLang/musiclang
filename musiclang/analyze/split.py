import glob
import shutil
import os
import random
class SplitTrainTest:


    def __init__(self, input_pattern, output_directory, train_ratio=0.95):

        self.input_pattern = input_pattern
        self.output_directory = output_directory
        self.train_ratio = train_ratio

    def split(self):
        try:
            shutil.rmtree(self.output_directory)
        except:
            pass
        os.makedirs(self.output_directory, exist_ok=True)
        create_train_val_split(self.input_pattern, self.output_directory, self.train_ratio)
        """
        Create train and val datasets
        """
        # Create train and val dataset
        train_output = os.path.join(self.output_directory, "train")
        val_output = os.path.join(self.output_directory, "val")
        prepare_dataset(train_output, os.path.join(self.output_directory, 'train.txt'))
        prepare_dataset(val_output, os.path.join(self.output_directory, 'val.txt'))

def prepare_dataset(directory, output_file):
    file_pattern = os.path.join(directory, "*.txt")
    files = glob.glob(file_pattern)
    end_of_text = '<|endoftext|>'
    texts = []
    for file in files:
        with open(file, encoding="utf-8") as f:
            text = f.read()
            text = text.replace('\n', '')
        # Add start-of-text and end-of-text symbols
        text = text + end_of_text
        texts.append(text)

    full_text = "\n".join(texts)
    full_text = full_text.replace('\t', '')
    full_text = full_text.replace(' ', '')
    with open(output_file, 'w') as f:
        f.write(full_text)

def create_train_val_split(input_directory, output_directory, train_val_ratio=0.8):
    file_pattern = input_directory
    files = glob.glob(file_pattern)
    random.shuffle(files)

    train_size = int(len(files) * train_val_ratio)
    train_files = files[:train_size]
    val_files = files[train_size:]

    train_output = os.path.join(output_directory, "train")
    val_output = os.path.join(output_directory, "val")

    os.makedirs(train_output, exist_ok=True)
    os.makedirs(val_output, exist_ok=True)

    for file in train_files:
        shutil.copy(file, os.path.join(train_output, os.path.basename(file)))

    for file in val_files:
        shutil.copy(file, os.path.join(val_output, os.path.basename(file)))
