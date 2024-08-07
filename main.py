from fastapi import FastAPI, Response, status, Response
from fastapi.responses import HTMLResponse
import yt_dlp
import base64
from shazamio import Shazam

app = FastAPI()

yt_opts = {
    "format": "m4a/bestaudio/best",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
}


@app.get("/")
async def root(response_class=HTMLResponse):
    content = """
        <html>
            <head>
                <title>Simple Site</title>
            </head>
            <body>
                <script src="https://unpkg.com/htmx.org@2.0.1"></script>
                <h1>Youtube audio recognizer</h1>
                <input type="text" name="url">
                <button 
                    hx-get="/audio" 
                    hx-trigger="click"
                    hx-include="[name='url']"
                >Search</button>
            </body>
        </html>
        """

    return HTMLResponse(content, status_code=status.HTTP_200_OK)


# async def get_audio(url: str, response: Response):
@app.get("/audio")
async def get_audio(url: str):

    opts = yt_opts.copy()
    base64_filename: str = base64.b32encode(url.encode()).decode()

    output_file = f"tmp/{base64_filename}"
    opts["outtmpl"] = output_file

    print(f"Downloading {url}...")
    with yt_dlp.YoutubeDL(opts) as yt:
        err = yt.download(url)
        assert err == 0

    print(f"Success downloading {output_file}")

    print("Uploading to shazam...")

    s = Shazam()
    result = await s.recognize(f"{output_file}.m4a")
    return result

    return "Could not find audio 🤷"
