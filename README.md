# AI Project Framework for Data Processing and Deployment

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Pytorch](https://img.shields.io/badge/pytorch-compose-orange.svg)](https://pytorch.org/vision/0.19/generated/torchvision.transforms.Compose.html)
[![MkDocs](https://img.shields.io/badge/MkDocs-green.svg)](https://squidfunk.github.io/mkdocs-material/getting-started/)
[![Yolov5](https://img.shields.io/badge/Yolo-v5-blue.svg)](https://github.com/ultralytics/yolov5)

<img align="right"
src="https://www.foerstergroup.de/typo3conf/ext/wr/Resources/Public/img/foe_logo.svg"
alt="Foester Logo" width=200 height=100>

This project serves as a demonstration of the knowledge and experience I have acquired. The goal is to build a comprehensive, deployable AI framework that integrates data processing, model training, deployment readiness, and documentation.

---

## Table of Contents

- [AI Project Framework for Data Processing and Deployment](#ai-project-framework-for-data-processing-and-deployment)
  - [Table of Contents](#table-of-contents)
  - [📌 Key Features](#-key-features)
    - [Data Processing Pipelines](#data-processing-pipelines)
    - [AI Deployment Framework](#ai-deployment-framework)
    - [Documentation](#documentation)
    - [Logging](#logging)
    - [Code Quality Control](#code-quality-control)
    - [Open Source Model Integration](#open-source-model-integration)
  - [📂 Project Organization](#-project-organization)
  - [⚙️ Quick start](#️-quick-start)
    - [Step 1 - Create virtual enviroment](#step-1---create-virtual-enviroment)
    - [Step 2 - install dependencies](#step-2---install-dependencies)
    - [Step 3 - run the application under folder `notebooks`](#step-3---run-the-application-under-folder-notebooks)
    - [Step 4 - run streamlit UI](#step-4---run-streamlit-ui)
  - [✒️ Linters](#️-linters)
  - [🗒️ Mike Docs](#️-mike-docs)
    - [📜 Others](#-others)

---

## 📌 Key Features

### Data Processing Pipelines

- Reusable pipelines for **time series** and **image data**.  
- Utilize PyTorch's `Compose` for efficient preprocessing.  
- Configurable via YAML files:  
  - `image_pipeline.yaml` - Image data pipeline.  
  - `pipeline.yaml` - General pipeline settings.  

### AI Deployment Framework

- A comprehensive framework tailored for AI model deployment.  
- Virtual environment ensures project dependency isolation.

### Documentation

- Technical project details documented using **MkDocs**.  
- Easy-to-read and well-structured software descriptions.

### Logging

- Centralized logging: outputs to both **files** and **console**.  

### Code Quality Control

- Linters ensure high-quality code with automatic checks:
  - **Pre-commit hooks** for linting before commits.  
  - Centralized configuration managed in `pyproject.toml`.

### Open Source Model Integration

- Integrated **YOLOv5** for object detection inferencing tasks.

---

## 📂 Project Organization
  
    ├── 📂 .venv                        <- Virtual environment for project dependencies
    │
    ├── 📂 .vscode                      <- Shared VSCode settings
    │   ├── launch.json                 <- Configuration for debugging settings
    │   ├── settings.json               <- Auto-activate the virtual environment and define project
    │                                   ├─ folder
    │
    ├── 📂 data                         <- Folder to store raw and processed data
    │
    ├── 📂 docs                         <- Project documentation
    │   ├── 📂 reports                  <- Reports and analysis results
    │   ├── 📃 index.md                 <- MkDocs start page
    │   ├── 📃 linters.md               <- Information about linting tools
    │
    ├── 📂 inference                    <- Inference output and related files
    │   ├── 📂 output                   <- Model output results
    │
    ├── 📂 logs                         <- Log files for debugging and monitoring
    │
    ├── 📂 models                       <- Folder to save machine learning models
    │
    ├── 📂 notebooks                    <- Jupyter notebooks and Python applications
    │
    ├── 📂 settings                     <- Pipeline configuration files
    │   ├── image_pipeline.yaml         <- Configuration for image data pipeline
    │   └── pipeline.yaml               <- General pipeline configuration
    │
    ├── 📂 src                          <- Main source code folder
    │   ├── 📂 data                     <- Data processing scripts
    │   ├── 📂 utils                    <- Utility scripts for logging and plotting
    │
    ├── 📂 ui                           <- User interface and GUI-related scripts
    │
    ├── 📃 .env                         <- Environment variables configuration
    ├── 📃 .gitignore                   <- Files and folders ignored by Git
    ├── 📃 .pre-commit-config.yaml      <- Pre-commit configuration for linting
    ├── 📃 mkdocs.yml                   <- MkDocs configuration file
    ├── 📃 pyproject.toml               <- Project configuration for dependencies and tools
    ├── 📃 README.md                    <- Top-level README for project description
    └── 📃 requirements.txt             <- List of required Python dependencies

---

## ⚙️ Quick start

### Step 1 - Create virtual enviroment

    python -v venv .venv

### Step 2 - install dependencies

    pip install -r requirements.txt

### Step 3 - run the application under folder `notebooks`

### Step 4 - run streamlit UI

    # tpye the following command in command line under folder 'build_scripts'
    python streamlit run %~dp0\\..\\ui\Overview.py  --server.port 8501
    pause

---

## ✒️ Linters

We use `pre-commit` for linting. Make sure that you have `pre-commit` installed, otherwise run `pre-commit install`.  
Then, to lint the currently staged code, run:

    pre-commit run --all-files

To skip the linter, use:

    git commit --no-verify -m "commit message"

---

## 🗒️ Mike Docs

Use the following command to start the live-reloading docs server, and this page will be available at <http://127.0.0.1:8000/>

    mkdocs serve

---

### 📜 Others

CI/CD Pipeline Integration?

Dev Container?

COCO Dataset (val2017) / Imagenet
