from fastapi import FastAPI , Response
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import os
from io import BytesIO
from datetime import date

class Employee(BaseModel):
    name: str
    email: str
    role: str
    enroll_date : date
    
class BodyWrapper(BaseModel):
    body: Employee
    
app = FastAPI()


@app.post("/generate")
async def pdf_gen(data: BodyWrapper):
    
    employee = data.body
    print(f"Generating PDF for {employee.name}")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content from JSON
    pdf.cell(200, 10, txt=f"Name: {employee.name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: { employee.email}", ln=True)
    pdf.cell(200, 10, txt=f"Position: { employee.role}", ln=True)
    pdf.cell(200, 10, txt=f"Enroll date: { employee.enroll_date}", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_stream = BytesIO(pdf_bytes)

    # Return PDF as file response
    return Response(
        content=pdf_stream.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=user_info.pdf"
        }
    )
  