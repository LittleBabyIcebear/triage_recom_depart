import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Setup API Key
load_dotenv()

if os.getenv("GOOGLE_API_KEY") is None:
    print("WARNING: Need API Key .env")

# Model input
class PatientInfo(BaseModel):
    gender: str                 
    age: int                     
    symptoms: List[str]         

# Model output 
class Recommendation(BaseModel):
    recommended_department: str # 

# Initialization
app = FastAPI(
    title="BitHealth Triage API",
    description="API for Departement Recommendation"
)

# Setup LangChain
PROMPT_TEMPLATE = """
Berperanlah seperti AI asisten triase di sistem rumah sakit.
Tugasmu adalah merekomendasikan satu departemen spesialis yang paling relevan
berdasarkan informasi pasien (jenis kelamin, usia, gejala).

Jawab HANYA dengan nama departemennya saja (misal: "Neurology", "Cardiology", "Gastroenterology", "Pediatry") dan lain-lainnya.

Informasi Pasien:
- Jenis Kelamin: {gender}
- Usia: {age} tahun
- Gejala: {symptoms}

Rekomendasi Departemen: 
"""

# LLM Google initialization
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
output_parser = StrOutputParser()

# Combined all
chain = prompt | llm | output_parser


# Endpoint Definition
@app.get("/")
def read_root():
    """Root API"""
    return {"status": "BitHealth Triage API is running."}


@app.post("/recommend", response_model=Recommendation) # 
async def recommend_department(patient_info: PatientInfo):
    
    # ubah jawaban menjadi string 
    symptoms_str = ", ".join(patient_info.symptoms)
    
    # call langchain
    recommendation_text = await chain.ainvoke({
        "gender": patient_info.gender,
        "age": patient_info.age,
        "symptoms": symptoms_str
    })
    
    # membersihkan output untuk jaga-jaga kalau llm aneh-aneh
    cleaned_recommendation = recommendation_text.strip()

    return Recommendation(recommended_department=cleaned_recommendation)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)