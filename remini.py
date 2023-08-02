import base64
import hashlib
from time import sleep

import httpx

from config import REMIKEY

import aiofiles
import asyncio 

 

class ImageCreator: 
    def __init__ (self):
        self.api_key =  REMIKEY
        self.content_type = "image/jpeg"
        self.output_content_type = "image/jpeg"
        self._timeout = 60
        self._base_url = "https://developer.remini.ai/api"

    @staticmethod
    def _get_image_md5_content(telegram_id) -> tuple[str, bytes]:
        with open(f'{telegram_id}.jpg', "rb") as fp:
            content = fp.read()
            image_md5 = base64.b64encode(hashlib.md5(content).digest()).decode("utf-8")
        return image_md5, content

    async def _generate(self, telegram_id : int, face_mode : str, back_mode : str, color_mode : str):
        try:


            if color_mode == 'none':
                tools = [
                            {"type": "face_enhance", "mode": face_mode},
                            {"type": "background_enhance", "mode": back_mode},
                        ]

            else:
                tools = [
                            {"type": "face_enhance", "mode": face_mode},
                            {"type": "background_enhance", "mode": back_mode},
                            {"type":"color_enhance","mode": color_mode},
                        ]


            image_md5, content = self._get_image_md5_content(telegram_id)
            # Setup an HTTP client with the correct options
            async with httpx.AsyncClient(
                base_url=self._base_url, headers={"Authorization": f"Bearer {self.api_key}"}
            ) as client:
                # Submit the task
                response = await client.post(
                    "/tasks",
                    json={
                        "tools": tools,
                        "image_md5": image_md5,
                        "image_content_type": self.content_type,
                        "output_content_type": self.output_content_type,
                    },
                )
                assert response.status_code == 200
                body = response.json()
                task_id = body["task_id"]

                # Upload the image
                response =  httpx.put(
                    body["upload_url"],
                    headers=body["upload_headers"],
                    content=content,
                    timeout=self._timeout,
                )
                assert response.status_code == 200

                # Process the image
                response = await client.post(f"/tasks/{task_id}/process")
                assert response.status_code == 202

                # Get the image
                for i in range(50):
                    response = await client.get(f"/tasks/{task_id}")
                    assert response.status_code == 200

                    if response.json()["status"] == "completed":
                        break
                    else:
                        await asyncio.sleep(2)

                # Print the output URL to download the enhanced image
                print(response.json()["result"]["output_url"])
                image_url = response.json()["result"]["output_url"]
                async with httpx.AsyncClient() as client:
                    image = await client.get(image_url)
                    async with aiofiles.open(f'{telegram_id}.jpg', 'wb') as file:
                        await file.write(image.content)
                    return f'{telegram_id}.jpg'
        except AssertionError as ex:
            print(ex)
            return False 







if __name__ == '__main__':
    res = ImageCreator()
    asyncio.run(res.main('image.jpg'))