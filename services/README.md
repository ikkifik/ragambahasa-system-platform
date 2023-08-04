# Services—Bhinneka Project (ACE INA I2)

This is a services side from Bhinneka Project by project code I2-Garuda ACE.

What you will get?

- Tools for migrating data source to Google Drive.
- Script for extracting content of files with 3 known OCR tools.

----

## Quick Start

**Get the repo**

- [Create new repo](#) from this template
- Clone the repo on GitHub
- … or download .zip from GitHub

**Installation**

- Go to the project directory
- Create new python virtual environment (conda), and activate it

        conda create --name <env_name> python=3.8
        conda activate <env_name>

- Install the required package/library  

        pip install -r requirements.txt

**Run the app**

- Define server configuration in `config.py`

        cp config.py.ext config.py
        nano config.py

- Drive Backup

        python drive_backup.py

- OCR Extractor

        python text_extractor.py --pocr
        python text_extractor.py --mmocr
        python text_extractor.py --txtract

----

## Installing OCR Libraries

**PaddleOCR** [source](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_en/quickstart_en.md)

        python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple

        pip install paddleocr==2.6.1.3

**Textract (TesseractOCR)** [source](https://textract.readthedocs.io/en/latest/installation.html)

        sudo apt install libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
        flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev

        pip install textract

**MMOCR** [source](https://mmocr.readthedocs.io/en/latest/get_started/install.html)

        conda install pytorch torchvision cpuonly -c pytorch
        pip install -U openmim
        mim install mmengine
        mim install mmcv
        mim install mmdet
        mim install mmocr

----
