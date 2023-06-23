# How-pieces-are-put-together

How to use the tool:

1. Clone the repo
2. Create a virtual environment
```
$ python3 -m venv env
```
3. Activate the virtual environment
```
$ source env/bin/activate
```
4. Install the requirements
```
$ pip install -r requirements.txt
```
5. Make the script executable
```
$ chmod +x dataset_generation.py
```

Usage:
```
usage: Dataset generator [-h] [-a] [-w] [-j] [-p] source_directory

positional arguments:
  source_directory  The directory, where the source images are located

options:
  -h, --help        show this help message and exit
  -a, --all         Generate all the types of distortion (alternative to -w -j -p)
  -w, --wavy        Generate wavy images
  -j, --jigsaw      Generate jigsaw images
  -p, --pixelated   Generate pixelated images
```
