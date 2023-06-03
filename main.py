from main2 import * 

app = FastAPI(title="Image Captioning API", description="An API for generating caption for image.")

class ImageCaption(BaseModel):
    caption: str

@app.post("/predict/", response_model=ImageCaption)
def predict(file: UploadFile = File(...)):
    # Load the image file into memory
    contents = file.file.read()
    image = Image.open(io.BytesIO(contents))
    result = predict_step([image])
    result = [clean_text(st) for st in result]
    return JSONResponse(content={"caption": result})

# Redirect the user to the documentation
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")


