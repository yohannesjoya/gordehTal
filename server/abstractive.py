
from transformers import pipeline



class Abstractive:

    def __init__(self, model) -> None:
        self.abs_summarizer = model

    def summarizer(self,text,):

        summary = self.abs_summarizer(text)[0]["summary_text"]

        return summary
    

