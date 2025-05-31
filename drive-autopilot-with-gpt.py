import base64
from openai import OpenAI
from lib.camera.camera import makePhoto
from lib.drive.motor import forward, left, right, stop
from picamera import PiCamera
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

camera = PiCamera()

drivePath = "./drive/"

if(os.path.exists(drivePath) == False):
  os.mkdir(drivePath)

currentDriveSeqPath = drivePath + "drive_" + str(len(next(os.walk(drivePath))[1])+1) + "/"
os.mkdir(currentDriveSeqPath)

def detect_path(image_source):
    # open image
    with open(image_source, 'rb') as f:
        image = f.read()

        client = OpenAI()
        base64_image = base64.b64encode(image).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Detect next move for the autonomous car. Based on lane detected on image return only a single word: forward, left or right."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "low"
                        },
                    },
                ],
            }],
        )

        return response.choices[0].message.content.lower()


while 1:
    path = makePhoto(currentDriveSeqPath, camera)
    cmd = detect_path(path)

    debugPath = 'debug'
    if (os.path.exists(debugPath) == False):
        os.mkdir(debugPath)

    print(f'command: {cmd}')
    if(cmd == 'forward'):
        forward(0.3)
        stop()
    if(cmd == 'left'):
        left(0.3)
        stop()
    if(cmd == 'right'):
        right(0.3)
        stop()
