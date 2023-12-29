import base64
import cv2
import requests
from datetime import datetime
import os
from openai import OpenAI
import time

# OpenAI API Key
api_key = "sk-"
client =  OpenAI(api_key=api_key)

# Ça c'est juste pour bien debuger, pour nous permettre de faire un nouveau sous répertoire à chaque expérience
# On va mettre tous nos fichiers dedans pour les retrouver facilement
datetime_folder = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
experiment_folder = os.path.join("experiments", datetime_folder)
os.mkdir(experiment_folder)

# Function to capture an image from the webcam
def capture_image():
  cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
  cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
  time.sleep(1) # needed with webcam at work, but not at home.
  ret, frame = cam.read()
  if not ret:
    print("Failed to grab frame")
    return None
  cam.release()
  cv2.destroyAllWindows()

  # Path to your image
  image_path = os.path.join(experiment_folder, "WebcamFrame.jpg")

  # Save the image to disk
  cv2.imwrite(image_path, frame)
  return frame

def capture_square_1024_image():
  image = capture_image()
  # Calculate the center crop dimensions
  start_x = (1920 - 1024) // 2
  end_x = start_x + 1024
  start_y = (1080 - 1024) // 2
  end_y = start_y + 1024

  # Crop the image using numpy slicing
  center_cropped_image = image[start_y:end_y, start_x:end_x]
  return center_cropped_image

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

print("On va capturer une image")
image = capture_square_1024_image()
print("on vient de capturer l'image")

# Path to your image
image_path = os.path.join(experiment_folder, "WebcamCroped1024.jpg")

# Save the image to disk
cv2.imwrite(image_path, image)

# Getting the base64 string
base64_image = encode_image(image_path)

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": """Explique moi en français ce que tu vois dans l'image.
                  Tu es un ourson en peluche qui s'appelle Elis.
                  Tu crois que tu as vu l'image au travers de tes yeux de peluche.
                  Souviens toi, je n'ai que 5 ans. 
                  Garde tes réponses plutôt courtes svp."""
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  max_tokens=500
)

print(response.choices[0].message.content)
