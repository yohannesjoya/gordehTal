
import mysql.connector
from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pdfsumm import PDFhandler

from extractive import ExtractiveModel, _get_summary
from cosine import CosineModel, build_summary
from abstractive import Abstractive

from transformers import pipeline

hub_model_id = "yohannesa2sv/amharic_text_summarization"
abs_summarizer = pipeline("summarization", model=hub_model_id)


app = FastAPI()

# Setup cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Post route
@app.post("/pdfsummary")
def summarizePdf(request_body:dict):

    pdfText = PDFhandler().pdfSummerizeHandler(request_body["url"])
    model =request_body["model"]


    if (pdfText==""):
        return {"error":"could not summarize"}
    
    if model==0:
        tparser = ExtractiveModel(pdfText)
        summary =_get_summary(tparser)
    elif model==1:
        tparser = CosineModel(text=pdfText)
        summary = build_summary(tparser.sentences)
    else:
        summary = Abstractive(abs_summarizer).summarizer(pdfText)
    
    return JSONResponse(content=summary, status_code=201)


@app.post("/textsummarize")
def summarizeText(request_body:dict):

    text,model = request_body["text"],request_body["model"]
    summary="error"

    if model==0:
        tparser = ExtractiveModel(text)
        summary =_get_summary(tparser)
    elif model==1:
        tparser = CosineModel(text=text)
        summary = build_summary(tparser.sentences)
    else:
        summary = Abstractive(abs_summarizer).summarizer(text)
    if summary=="error":
        return JSONResponse(content="There is Error.", status_code=400)

    return JSONResponse(content=summary, status_code=201)




# Get route
@app.get("/")
def home():
    return {"hello":"world"}

