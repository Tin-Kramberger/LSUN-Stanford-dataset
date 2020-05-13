# LSUN-Stanford car dataset

This repository contains the official dataset and code of the following paper:
> **LSUN-Stanford car dataset: Enhancing a Large-scale Car Image Datasets using Deep Learning for usage in GAN training**<br>
> **Abstract:** _Objective_: Currently there is no publicly available adequate dataset that could be used for training Generative Adversarial Networks (GAN) on car images. All available car datasets differ in noise, pose, and zoom levels. Thus, the objective of this work is to create an improved car image dataset that would be better suited for GAN neural networks training. _Methods_: To improve the performance of GAN neural network we have coupled LSUN and Stanford car datasets. A new merged dataset was then pruned in order to adjust zoom levels and reduce a noise of images. This process resulted in fewer images that could be used for training, but with an increased quality. This pruned dataset, LSUN-Stanford dataset, was evaluated by training the StyleGAN neural network with original settings. _Results_: Pruning the combined LSUN and Stanford datasets resulted in 2,067,710 images of cars with less noise and more adjusted zoom levels. The training of the StyleGAN neural network with the LSUN-Stanford car dataset proved to be superior to the training with just the LSUN dataset by 3.7% using the Fréchet Inception Distance (FID) as a metric. _Conclusion_: Results pointed out that proposed LSUN-Stanford car dataset is more consistent and better suited for training GAN neural networks than other currently available large car datasets. _Significance_: Our proposed LSUN-Stanford dataset is large-scale and high-quality dataset specially tailored for the GAN neural networks aimed for the automotive industry or traffic.

### Citing LSUN-Stanford car dataset

If you find LSUN-Stanford car dataset useful in your research, please cite:

    @article{KrambergerPotocnik,
        Author = {Tin Kramberger and Božidar Potočnik},
        Title = {LSUN-Stanford car dataset: Enhancing a Large-scale Car Image Datasets using Deep Learning for usage in GAN training},
        Journal = {},
        Year = {2020}
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
