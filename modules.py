from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from pydantic import BaseModel
import io
import json
import requests
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

# Preliminaries
import os
import sys 
import numpy as np 
import pandas as pd

#transformers
from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer

# Pytorch
import torch
import torch.nn as nn

#warnings
import warnings
warnings.filterwarnings('ignore')

# My Module
#import config