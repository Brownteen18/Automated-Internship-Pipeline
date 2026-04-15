from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI(title="LaTeX Compiler API")

class LatexRequest(BaseModel):
    latex_code: str

@app.post("/compile")
async def compile_latex(request: LatexRequest):
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            tex_file = os.path.join(temp_dir, "document.tex")
            pdf_file = os.path.join(temp_dir, "document.pdf")
            
            # Write the latex code to a file
            with open(tex_file, "w", encoding="utf-8") as f:
                f.write(request.latex_code)
            
            # Run pdflatex (run twice for references/formatting if needed, but once is usually enough for simple resumes)
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_file],
                capture_output=True,
                text=True
            )
            
            if not os.path.exists(pdf_file):
                print(f"LaTeX Error Log: {result.stdout}\n{result.stderr}")
                raise HTTPException(status_code=400, detail=f"LaTeX compilation failed: See logs")
            
            # Read the PDF content
            with open(pdf_file, "rb") as f:
                pdf_content = f.read()
                
            return Response(content=pdf_content, media_type="application/pdf")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
