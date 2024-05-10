from re import A
from fastapi import FastAPI, WebSocket, websockets, Response
from starlette.websockets import WebSocketDisconnect, WebSocketClose
import matplotlib.pyplot as plt
from pydantic import BaseModel
import numpy as np
import base64
import io

app = FastAPI()

class WebsocketRequest(BaseModel):
    R: int
    G: int
    B: int

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # The FastAPI tutorial will tell you to use while True: here.
    # That's not a good idea, as it can block the even loop. Use
    # the async for over the text iteration instead.
    await websocket.accept()
    try:
        async for message in websocket.iter_text():
            formatted = WebsocketRequest.parse_raw(message)

            print(f"Data received: {formatted}")

            # Ok, now we have to format and send the image.
            try:
                with io.BytesIO() as output:
                    arr = np.empty([64, 64, 3])
                    arr[:,:] = np.array([formatted.R, formatted.G, formatted.B]) / 255.0
                    plt.imsave(output, arr)

                    output.seek(0)
                    img = f"{{\"image\": \"data:image/png;base64,{base64.b64encode(output.read()).decode('utf-8')}\"}}"
                    print("Sending image")
                    await websocket.send_text(img)
            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except WebSocketDisconnect as e:
        try:
            await websocket.close()
        except RuntimeError:
            # It died.
            return

@app.get("/http/tile.png")
async def http_endpoint(R: float, G: float, B: float):
    try:
        with io.BytesIO() as output:
            arr = np.empty([64, 64, 3])
            arr[:,:] = np.array([R, G, B]) / 255.0
            plt.imsave(output, arr)

            return Response(content=output.getvalue(), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
