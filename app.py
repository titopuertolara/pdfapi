from fastapi import FastAPI, Response
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import os
from io import BytesIO
from datetime import date
from sign_pdf import sign_pdf
from language_template_selector import select_template


class Employee(BaseModel):
    name: str
    email: str
    role: str
    enroll_date: date
    country: str
    language: str


class BodyWrapper(BaseModel):
    body: Employee


app = FastAPI()


@app.post("/generate")
async def pdf_gen(data: BodyWrapper):

    employee = data.body
    print(f"Generating PDF for {employee.name}")
    today_str = date.today().strftime("%B %d, %Y")
    start_date_str = employee.enroll_date.strftime("%B %d, %Y")
    pdf = FPDF(orientation="P", unit="mm", format="Letter")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    logo_path = "logo/logo-provectus-ua.png"
    signature_image_path = "signature_img/signature.png"
    if os.path.exists(logo_path):

        pdf.image(logo_path, x=10, y=10, w=45)
    if os.path.exists(signature_image_path):
        pdf.image(signature_image_path, x=150, y=230, w=40)
    
    pdf.set_y(30)
                
        
    if employee.language.lower().strip() in ['ukrainian','russian','serbian','polish','armenian','french','german','kazakh']:
        
        font_type = "DejaVuSans"
        encoding = "latin1"
        pdf.add_font(font_type, "", "fonts/DejaVuSans.ttf", uni=True)
        pdf.set_font(font_type, "", 12)
        
    else:
        font_type = "Arial"
        encoding = "latin1"
        pdf.set_font(font_type, size=12)    

    
    letter = select_template(
        employee.name, employee.country, employee.role,
        today_str, start_date_str, employee.language
    )
    
    
    pdf.multi_cell(0, 10, txt=letter, align="L")
    
    
    

    pdf_bytes = pdf.output(dest="S").encode(encoding)    
 
    
    signed_pdf_bytes = sign_pdf(pdf_bytes)
    print("PDF content generated successfully.")

    return Response(
        content=signed_pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=verification_letter.pdf"},
    )
