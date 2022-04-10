from random import randint
import aiofiles
from fastapi import FastAPI, File
from fastapi.datastructures import UploadFile
from nsfw_detector import predict
from mangum import Mangum
import os

model = predict.load_model('nsfw_detector/nsfw_model.h5')
app = FastAPI()

@app.post("/")
async def detect_nsfw(file: UploadFile = File(...)):
    # with file.read() as image:
    #     if not image:
    #         return {"ERROR": "IMAGE SIZE TOO LARGE OR INCORRECT URL"}
    file_name = await save_img(file.file)
    results = predict.classify(model, file_name)

    delete_img(file_name)

    hentai = results['data']['hentai']
    sexy = results['data']['sexy']
    porn = results['data']['porn']
    drawings = results['data']['drawings']
    neutral = results['data']['neutral']
    if neutral >= 25:
        results['data']['is_nsfw'] = False
        return results
    elif (sexy + porn + hentai) >= 70:
        results['data']['is_nsfw'] = True
        return results
    elif drawings >= 40:
        results['data']['is_nsfw'] = False
        return results
    else:
        results['data']['is_nsfw'] = False
        return results


async def save_img(file: UploadFile) -> str:
    file_name = f"{randint(6900, 6999)}.jpg"
    f = await aiofiles.open(file_name, mode='wb')
    await f.write(file.read())
    await f.close()

    return file_name

def delete_img(file_name):
    os.remove(file_name)

handler = Mangum(app)
