from sklearn.model_selection import train_test_split
import os
from glob import glob
import numpy as np
import imghdr
from scipy.misc import imread
import multiprocessing as mp

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def check_image(image):
    file_type = imghdr.what(image)
    if file_type == 'jpeg':
        if len(imread(image).shape) == 3:
            return True
    return False

def check_and_move(triple):
    folder, file_path, category = triple
    if not check_image(file_path):
        return

    name = file_path.split('/')[-1]
    os.rename(file_path, '{}/{}/{}'.format(folder, category, name))


def generate_cats_and_dogs():
    if os.path.isdir('train') or os.path.isdir('test'):
        print("It seems the dataset has already been generated (remove 'train' and 'test' folders to generate it again)")
        return

    dog = 0
    cat = 1
    test_size=0.2

    os.system("curl -O 'https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip'")
    os.system("tar -xzf 'kagglecatsanddogs_3367a.zip'")
    os.rename('PetImages', 'images/')
    os.remove('kagglecatsanddogs_3367a.zip')
        
    cats = glob('images/Cat/*.jpg')
    dogs = glob('images/Dog/*.jpg')

    X = cats + dogs
    y = [cat for _ in cats] + [dog for _ in dogs]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    for folder in ['train', 'test']:
        create_folder(folder)
        for subfolder in ['{}/{}'.format(folder, category) for category in np.unique(y)]:
            create_folder(subfolder)

    with mp.Pool(mp.cpu_count()) as pool:
        train = ['train' for _ in X_train]
        pool.map(check_and_move, list(zip(train, X_train, y_train)))
        test = ['test' for _ in X_test]
        pool.map(check_and_move, list(zip(test, X_test, y_test)))

    os.system('rm -rf images')
