from fastapi import APIRouter, UploadFile, File, Form
from ...cas_parser.main import parse_cas
import os
import shutil
import tempfile

router = APIRouter(prefix="/cas", tags=["CAS"])

@router.post("/parse")
async def upload_cas(
    file: UploadFile = File(...),
    pan: str = Form(None),
    dob: str = Form(None)
):
    # Save uploaded file to temp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Parse
        result = parse_cas(tmp_path, pan=pan, dob=dob)
        return result
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
