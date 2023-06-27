import asyncio
import websockets
import time
import sounddevice as sd
import numpy as np
import asyncclick as click

LOCAL_WEB_SOCKET_URL = "ws://127.0.0.1:8765"
DEFAULT_SAMPLE_RATE = "44100"
DEFAULT_CHANNELS = "1"
DEFAULT_DTYPE = np.int16
DEFAULT_TASK = "translate"

async def audio_stream(
    samplerate = DEFAULT_SAMPLE_RATE,
    channels   = DEFAULT_CHANNELS,
    dtype      = DEFAULT_DTYPE,
    task       = DEFAULT_TASK,
    url        = LOCAL_WEB_SOCKET_URL,
):
    samplerate = int(samplerate)
    channels   = int(channels)
    
    # Set the WebSocket request headers
    headers = {
        "samplerate": samplerate,
        "channels": channels,
        "dtype": dtype,
        "task": task
    }
    
    # Open the WebSocket connection
    async with websockets.connect(url,extra_headers=headers) as websocket:
        print("WebSocket connection established.")
    
        # Configure sounddevice input stream
        stream = sd.InputStream(
            channels=channels,
            samplerate=samplerate,
            dtype=dtype,
        )
        
        # Start recording audio
        stream.start()
        print("Start streaming audio ...")
        
        start_of_speech_flag = False
        start_time = time.time()
        
        while True:
            # Read audio data from input stream
            audio_data, _ = stream.read(1024)
            
            # Detect start of speech
            if np.mean(audio_data) > 10:
                start_of_speech_flag = True 
                start_time = time.time()
    
            # Detect end of speech
            if start_of_speech_flag and time.time() - start_time >= 0.55:
                stream.stop()
                print("Stop streaming audio ...")
                # send end of speech
                eos_time = time.time()
                await websocket.send("end of speech")
                break
            else: 
                # Send audio data to the WebSocket server
                await websocket.send(audio_data.tobytes())
         
        # Receive any response from the WebSocket server (if needed)
        response = await websocket.recv()
        response_time = time.time()
        print(response)
        print("Response time: " + str(response_time - eos_time))
        await websocket.close()
        
@click.command()
@click.option(
    "--task",
    default="transcribe",
    type=str,
    help="Task to perform: translate or transcribe",
)
@click.option(
    "--url",
    default=LOCAL_WEB_SOCKET_URL,
    type=str,
    help="URL of the WebSocket server",
) 
@click.option(
    "--samplerate",
    default="44100",
    type=str,
    help="Sample rate of the audio stream",
)
@click.option(
    "--channels",
    default="1",
    type=str,
    help="Channels of the audio stream",
)       
async def main(task: str, url: str, samplerate: str, channels: str):
    # Run the audio_stream function in an event loop
    await audio_stream(task=task, url=url, samplerate=samplerate, channels=channels)

if __name__ == "__main__":
    asyncio.run(main())
