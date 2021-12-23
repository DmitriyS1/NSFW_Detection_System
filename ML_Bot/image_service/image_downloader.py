import asyncio
from types import coroutine
import config
from random import randint
import aiohttp
import aiofiles

MAX_IMAGE_SIZE = config.MAX_IMAGE_SIZE * 1000000
URL = "https://planetanimal.ru/wp-content/uploads/2021/01/ussur-jpg-1024x694.jpeg"

async def get_site_images(url):
    # make request to site and get 10 images
    #for url in urls:
    image = await download_image(url)
    if len(image) > 0:
        result = await classify_image(image)

#do it correct!
async def download_image(url) -> bytes:
    async with aiohttp.ClientSession() as session: # to not open a lot of sessions download bunch of pics in one session
        async with session.get(url) as resp:
            if resp.status == 200:
                if int(resp.headers['Content-Length']) > MAX_IMAGE_SIZE:
                    return False
                # f = await aiofiles.open(file_name, mode='wb')
                result = await resp.read() # send to queue? send over http to classifier?
            else:
                return 0
            
    return result

async def classify_image(image: bytes):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field('file', image, content_type='multipart/form-data')
        async with session.post(config.CLASSIFIER_URL_local, data=form) as resp:
            if resp.status == 200:
                result = await resp.read()
        
    print('result: ', result)
    return result


loop = asyncio.get_event_loop()
loop.run_until_complete(get_site_images(URL))
loop.close()
