import os
import asyncio
import utils
import json
from services.coqui_tts import TTS
from services.s3 import S3
from services.nat import Broker
from config import (get_nats_url, get_model_path, get_config_path, get_s3_region,
    get_s3_bucket, get_s3_key, get_s3_secret)

class Main:
    
    def __init__(self):
        self._s3 = S3(get_s3_region(), get_s3_key(), get_s3_secret())
        self._tts = TTS(get_model_path(), get_config_path())
        self._nats = Broker()
        
    async def job_tts_created_handler(self, msg):
        utils.print_info(f"Received a message on '{msg.subject}': {msg.data.decode()}")
        data = json.loads(msg.data.decode())
        output = self._tts.synthesize(data['text'], f"speakers/{data['speaker']}.wav")
        filename = os.path.basename(output)
        key = f"audio/{data['id']}/{filename}"
        self._s3.upload_file(output, get_s3_bucket(), key)
        os.remove(output)
        await self.job_tts_completed_publisher(data['id'], key)
    
    async def job_tts_completed_publisher(self, id, filepath):
        data = json.dumps({"id": id, "audio": filepath}).encode()
        await self._nats.publish("job.tts.completed", data)
        
    async def run(self):
        await self._nats.connect(get_nats_url())
        await self._nats.subscribe("job.tts.created", self.job_tts_created_handler)
        while True:
            await asyncio.sleep(1)
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_app = Main()
    try:
        loop.run_until_complete(main_app.run())
    except KeyboardInterrupt:
        print("Shutting down...")