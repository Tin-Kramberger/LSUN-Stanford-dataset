# LSUN-Stanford car dataset

This repository contains the official dataset and code of the following paper:
> **LSUN-Stanford Car Dataset: Enhancing Large-Scale Car Image Datasets Using Deep Learning for Usage in GAN Training**<br>
> **Abstract:** Currently there is no publicly available adequate dataset that could be used for training Generative Adversarial Networks (GANs) on car images. All available car datasets differ in noise, pose, and zoom levels. Thus, the objective of this work was to create an improved car image dataset that would be better suited for GAN training. To improve the performance of the GAN, we coupled the LSUN and Stanford car datasets. A new merged dataset was then pruned in order to adjust zoom levels and reduce the noise of images. This process resulted in fewer images that could be used for training, with increased quality though. This pruned dataset was evaluated by training the StyleGAN with original settings. Pruning the combined LSUN and Stanford datasets resulted in 2,067,710 images of cars with less noise and more adjusted zoom levels. The training of the StyleGAN on the LSUN-Stanford car dataset proved to be superior to the training with just the LSUN dataset by 3.7% using the Fréchet Inception Distance (FID) as a metric. Results pointed out that the proposed LSUN-Stanford car dataset is more consistent and better suited for training GAN neural networks than other currently available large car datasets.

### Citing LSUN-Stanford car dataset

If you find LSUN-Stanford car dataset useful in your research, please cite:

    @article{KrambergerPotocnik2020,
        author = {Kramberger, Tin and Poto{\v{c}}nik, Bo{\v{z}}idar},
        Title = {LSUN-Stanford Car Dataset: Enhancing Large-Scale Car Image Datasets Using Deep Learning for Usage in GAN Training},
        issn = {2076-3417},
        journal = {Applied Sciences},
        Year = {2020},
        month = {jul},
        number = {14},
        publisher = {Multidisciplinary Digital Publishing Institute},
        volume = {10},
        doi = {10.3390/app10144913},
        url = {https://www.mdpi.com/2076-3417/10/14/4913}
    }


All resources are available on Google Drive folder on this [link](https://drive.google.com/drive/folders/10L49FrRzlBKyacKNZl4nPdil5JBWBlFh?usp=sharing).

### Dependency

Install MySQL: https://www.mysql.com/downloads/

Install Python: https://www.python.org/downloads/

Install Python dependencies: Pillow, mysql-connector-python:
```bash
pip install Pillow
pip install mysql-connector-python
```

###How to use the dataset

1. Download LSUN car dataset from link: http://dl.yf.io/lsun/objects/car.zip and use provided script to export the images to desired folder.
2. Download Stanford car dataset from links: http://imagenet.stanford.edu/internal/car196/cars_train.tgz and http://imagenet.stanford.edu/internal/car196/cars_test.tgz
3. Export the Stanford car dataset images to the same folder chosen in step 1 in 'cars_train' and 'cars_test' sub folders.
4. Download our MySQL database from link: https://drive.google.com/drive/folders/10L49FrRzlBKyacKNZl4nPdil5JBWBlFh
5. Extract the SQL script from zip file and import the database using script for example:
    ```bash
    mysql -u username -p db_name < db-dump.sql
    ```
6. Use provided python script from repository to crop images to desired size for example:
    ```bash
    Python ExportImagesFromDataset.py --dataset_dir "c:/images" --width 400 --height 300 --host "localhost" --username "username" --password "password" --database "db_name" --output_dir "C:/exported" --multiple_box True --multiple_box_overlapping_person True
    ```
