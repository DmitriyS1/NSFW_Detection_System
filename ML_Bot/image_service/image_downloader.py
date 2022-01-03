from aiohttp.client import ClientSession
from image_service import config
import aiohttp

MAX_IMAGE_SIZE = config.MAX_IMAGE_SIZE * 1000000

async def is_nsfw(urls) -> bool:
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
            result = await resp.read()
        else:
            return 0
            
    return result
    

async def classify_image(image: bytes):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field('file', image, content_type='multipart/form-data')
        async with session.post(config.CLASSIFIER_URL, data=form) as resp:
            if resp.status == 200:
                result = await resp.json(encoding='utf-8')
        
    return result
