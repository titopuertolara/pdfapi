from fastapi import FastAPI , Response
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.responses import FileResponse
import os
from io import BytesIO
from datetime import date
from sign_pdf import sign_pdf

class Employee(BaseModel):
    name: str
    email: str
    role: str
    enroll_date : date
    country: str
    
class BodyWrapper(BaseModel):
    body: Employee
    
app = FastAPI()


@app.post("/generate")
async def pdf_gen(data: BodyWrapper):
    
    employee = data.body
    print(f"Generating PDF for {employee.name}")
    today_str = date.today().strftime("%B %d, %Y")  
    start_date_str = employee.enroll_date.strftime("%B %d, %Y")

   
    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

   
    logo_path = "logo/logo-provectus-ua.png"
    if os.path.exists(logo_path):
        
        pdf.image(logo_path, x=10, y=10, w=45)
    pdf.set_font("Arial", size=12)
    
    pdf.set_y(30) 

    
    pdf.cell(0, 10, txt=today_str, ln=True)
    pdf.ln(10)

    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(0, 10, txt=f"RE: Verification for  {employee.name}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    
    letter = (
        f"To Whom It May Concern,\n\n"
        f"This letter is written in the verification of the fact that {employee.name} "
        f"is performing services as an Independent Contractor remotely from {employee.country} for "
        f"Provectus IT, Inc. as a {employee.role} from {start_date_str}, up till now.\n\n"
        "I serve as Director of People Operations, Technology, and Analytics of the "
        "company and can attest to his performance and contributions.\n\n"
        "If you have any further questions, please feel free to contact me.\n\n"
        "Yours truly,\n\n"
        "Director of People Operations, Technology and Analytics\n"
        "Provectus IT, Inc."
    )

    pdf.multi_cell(0, 10, txt=letter, align='L')

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    signed_pdf_bytes= sign_pdf(pdf_bytes)
    pdf_stream = BytesIO(signed_pdf_bytes)

    
    return Response(
        #content=pdf_stream.getvalue(),
        content=signed_pdf_bytes
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=verification_letter.pdf"
        }
    )
  