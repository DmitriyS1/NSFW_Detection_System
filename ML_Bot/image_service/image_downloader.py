from config import MAX_IMAGE_SIZE
from random import randint
import aiohttp
import aiofiles

MAX_IMAGE_SIZE = MAX_IMAGE_SIZE * 1000000

#do it correct!
async def download_image(urls):
    file_name = f"{randint(6969, 6999)}.jpg"
    async with aiohttp.ClientSession() as session: # to not open a lot of sessions download bunch of pics in one session
        for url in urls:
            async with session.get(url) as resp:
                if resp.status == 200:
                    if int(resp.headers['Content-Length']) > MAX_IMAGE_SIZE:
                        return False
                    f = await aiofiles.open(file_name, mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                else:
                    return False
        
    return file_name
