
import PyPDF2
from openai import OpenAI
import requests
from io import BytesIO
from abstractive import Abstractive

client = OpenAI(api_key="")

class PDFhandler():

    def pdfSummerizeHandler(self,pdfUrl):

        response = requests.get(pdfUrl)

        if response.status_code == 200:
            pdf_file = BytesIO(response.content)
            pdf_reader = PyPDF2.PdfReader(pdf_file);

            pdf_text = ""
            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()

            return pdf_text
        
        return ""




                # response = client.chat.completions.create(
                #     model = "gpt-3.5-turbo",
                #     messages = [
                #                 {"role" : "system","content":"You are a helpful research assistant.",},
                #                 {"role" : "user","content":f"Summarize this: {page_text}",}
                #             ]
                # )
                # page_summary = response.choices[0].message.content.strip()
                # pdf_summmary_text += page_summary + "\n"

            