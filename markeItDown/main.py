import os
import shutil
from uuid import uuid4

from fastapi import FastAPI, UploadFile, HTTPException, File
from markitdown import MarkItDown
from groq import Groq

app = FastAPI()

# Initialize the Groq client and MarkItDown instance.
client = Groq()
md = MarkItDown(llm_client=client, llm_model="llama-3.2-11b-vision-preview")


@app.post("/convert")
async def convert_markdown(file: UploadFile = File(...)):
    # Create a unique temporary folder using a UUID.
    folder_name = str(uuid4())
    folder_path = os.path.join("tmp", folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating temporary folder: {e}"
        )

    file_path = os.path.join(folder_path, file.filename)  # type: ignore

    try:
        # Save the uploaded file to disk using copyfileobj.
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Convert the file using MarkItDown.
        result = md.convert(file_path)
        return {"text_content": result.text_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion error: {e}")
    finally:
        # Clean up the temporary folder.
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            # Log the error; cleanup failure shouldn't break the API response.
            print(f"Error removing temporary folder {folder_path}: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
