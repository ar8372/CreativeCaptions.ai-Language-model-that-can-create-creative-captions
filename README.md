### [Language-model-that-can-create-creative-captions]
# CreativeCaptions.ai
Language Model that creates catchy, exciting, innovative, captivating, creative and engaging captions instead of just a description of the picture.

## Samples
### 1.
<p>
    <img src="images/Image5.png" width="800" height="400" />
</p>

> Output 
<p>
    <img src="images/response5.png" width="500" height="120" />
</p>

### 2.
<p>
    <img src="images/Image6.png" width="800" height="400" />
</p>

> Output 
<p>
    <img src="images/response6.png" width="500" height="120" />
</p>
# How to use it

## Environment setup
### Folder Structure
Download the repository and make sure we have below file structure.
```
CreativeCaptions.ai-Language-model-that-can-create-creative-captions/
|
├── images/
|     |__ Images5.png
|     |__ Images6.png
|
├── models_folder/
|     |__ gpt2_medium_joke_insta.pt
|     |__ ..
|
├── main.py
|
├── modules.py
|
└── requirements.txt
```
Change your working directory to `CreativeCaptions.ai-Language-model-that-can-create-creative-captions`. 
Download the model `gpt2_medium_joke_insta.pt` from https://www.kaggle.com/code/raj401/inference-mnist and store it in `models_folder`

### Dependencies
Install below libraries.<br>
```
pip install sentencepiece
pip install transformers
pip install torch
pip install fastapi
pip install starlette
pip install aiofiles
pip install python-multipart
pip install Pillow
pip install uvicorn
```