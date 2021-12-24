import asyncio
from aiohttp.client import ClientSession
import config
import aiohttp

MAX_IMAGE_SIZE = config.MAX_IMAGE_SIZE * 1000000

async def is_nsfw(urls) -> bool:
    # make request to site and get 10 images
    async with aiohttp.ClientSession() as session:
        for url in urls:
            image = await download_image(url, session)
            if len(image) > 0:
                result = await classify_image(image)
                if result['data']['is_nsfw']:
                    return result['data']['is_nsfw']


async def download_image(url, session: ClientSession) -> bytes:
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
        async with session.post(config.CLASSIFIER_URL, data=form) as resp:
            if resp.status == 200:
                result = await resp.json(encoding='utf-8') #read()
        
    return result


# loop = asyncio.get_event_loop()
# loop.run_until_complete(is_nsfw([URL1, URL2]))
# loop.close()
