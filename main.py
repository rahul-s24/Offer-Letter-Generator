from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel
import pandas as pd
import os
from agent.html_template_builder import build_html

from agent.prompt_builder import build_prompt
from agent.pdf_generator import generate_pdf
from agent.offer_letter_generator import generate_letter
from agent.structured_policy_retriever import summarize_structured_policies

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/pdfs", StaticFiles(directory="output/generated_letters"), name="pdfs")


class EmployeeRequest(BaseModel):
    employee_name: str

@app.post("/generate-letter")
async def generate_letter_api(req: EmployeeRequest):
    try:
        df = pd.read_csv("data/Employee_List.csv")
        employee = df[df["Employee Name"].str.strip() == req.employee_name].iloc[0].to_dict()

        summaries = summarize_structured_policies(None, employee)
        prompt = build_prompt(employee, summaries)
        letter = generate_letter(prompt)
        #pdf_path = generate_pdf(req.employee_name, letter)
        
        html_string = build_html(employee, summaries)
        pdf_path = generate_pdf(req.employee_name, html_string)
        filename = os.path.basename(pdf_path)

        return {
            "status": "success",
            "offer_letter": letter,
            "pdf_file": filename
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    file_path = os.path.join("output/generated_letters", filename)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            content = f.read()
        return Response(
            content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
                "Access-Control-Allow-Origin": "*"
            }
        )
    return {"status": "error", "message": "File not found"}
