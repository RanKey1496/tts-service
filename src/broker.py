import asyncio
import nats
import json

async def main():
    try:
        nc = await nats.connect("nats://127.0.0.1:4222")

        #data = {"text": "Quiero construir un audio muchisimo más largo, entonces voy a enviar un texto bien largo para explicar esta vaina. Cuando haga el audio luego debo subir el audio a S3 que posteriormente será descargado por el servcio de video y procesará el resto de cosas necesarias para formar un video completo.", "speaker": "speakers/herrera.wav"}
        
        data = {"id": 1, "text": "Ducati es reconocida mundialmente como un símbolo de lujo y alto rendimiento en el mundo de las motocicletas. Su diseño italiano impecable, combinado con tecnologías innovadoras como la distribución desmodrómica, ha establecido estándares en el segmento de las motos deportivas y de lujo. Modelos como la Panigale y la Streetfighter no solo destacan por su potencia y precisión en el manejo", "speaker": "daniel"}
        await nc.publish("job.tts.created", json.dumps(data).encode())
        await nc.drain()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())