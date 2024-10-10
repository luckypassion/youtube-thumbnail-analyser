import os
import base64
import re
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import mysql.connector
from groq import Groq
from datetime import datetime
import hashlib
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/","http://localhost:5173"],  # Adjust this to your specific needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY1"))



def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_DATABASE"),
    )

def get_image_hash(image_data):
    return hashlib.sha256(image_data).hexdigest()

# Function to encode the image
def encode_image(file):
    return base64.b64encode(file.read()).decode('utf-8')


@app.post("/upload_thumbnail/")
async def upload_thumbnail(file: UploadFile = File(...)):
    base64_image = encode_image(file.file)
    image_hash = get_image_hash(base64_image.encode())
    
    # Check the database for an existing response
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT score, comment FROM thumbnail_feedback WHERE image_hash = %s", (image_hash,))
    existing_response = cursor.fetchone()

    if existing_response:
        return {"score": existing_response['score'], "comment": existing_response['comment']}

    # If no existing response, prepare the request to Groq
    comment = ""
    score = None
    attempts = 3
    attempt = 0

    while attempt < attempts and score is None:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze and Describe the thumbnail and provide a rating from 1 to 10 should be in that format 8/10, along with suggestions for improvement."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )

        response_message = chat_completion.choices[0].message
        comment = response_message.content
        score = extract_score_from_comment(comment)

        attempt += 1

    # If score is still None after attempts, you may choose to handle it
    if score is None:
        return {"error": "Unable to retrieve a score after multiple attempts.", "comment": comment}

    # Store feedback and original image in the database
    cursor.execute(
        "INSERT INTO thumbnail_feedback (image_hash, score, comment, created_at) VALUES (%s, %s, %s, %s)",
        (image_hash, score, comment, datetime.now())
    )
    connection.commit()
    cursor.close()
    connection.close()

    return {"score": score, "comment": comment}




def extract_score_from_comment(comment):
    # Check for "rated" phrases
    if "rated" in comment.lower():
        parts = comment.split("rated")
        score_part = parts[1].split("/")[0].strip()
        try:
            return float(score_part)  # Change to float to support decimal scores
        except ValueError:
            return None

    # Look for explicit scores in "X/10" format (including float)
    match = re.search(r'(\d+(\.\d+)?)\s*/\s*10', comment)
    if match:
        return float(match.group(1))

    # Look for scores in "X-Y" format
    match = re.search(r'(\d+(\.\d+)?)\s*-\s*\d+', comment)
    if match:
        return float(match.group(1))  # Return the first number as float

    # Look for "I would rate it a X" pattern (including float)
    match = re.search(r'I would rate it a (\d+(\.\d+)?)', comment)
    if match:
        return float(match.group(1))

    # Look for explicit scores using "out of 10"
    match = re.search(r'(\d+(\.\d+)?)\s*out of 10', comment)
    if match:
        return float(match.group(1))

    # Look for "may be rated" phrases
    if "may be rated" in comment.lower():
        parts = comment.split("may be rated")
        score_part = parts[1].split()[0].strip()
        try:
            return float(score_part)  # Change to float to support decimal scores
        except ValueError:
            return None

    # Default to None if no score is found
    return None

# def extract_score_from_comment(comment):
#     # Check for "rated" phrases
#     if "rated" in comment.lower():
#         parts = comment.split("rated")
#         score_part = parts[1].split("/")[0].strip()
#         return int(score_part) if score_part.isdigit() else None

#     # Look for explicit scores in "X/10" format
#     match = re.search(r'(\d+)\s*/\s*10', comment)
#     if match:
#         return int(match.group(1))

#     # Look for scores in "X-Y" format
#     match = re.search(r'(\d+)\s*-\s*\d+', comment)
#     if match:
#         return int(match.group(1))  # Return the first number

#     # Look for "I would rate it a X" pattern
#     match = re.search(r'I would rate it a (\d+)', comment)
#     if match:
#         return int(match.group(1))

#     # Look for explicit scores using "out of 10"
#     match = re.search(r'(\d+)\s*out of 10', comment)
#     if match:
#         return int(match.group(1))

#     # Look for "may be rated" phrases
#     if "may be rated" in comment.lower():
#         parts = comment.split("may be rated")
#         score_part = parts[1].split()[0].strip()
#         return int(score_part) if score_part.isdigit() else None

#     # Default to None if no score is found
#     return None