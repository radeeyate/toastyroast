from fastapi import FastAPI, UploadFile, HTTPException, Request, File, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import secrets
import google.generativeai as genai
from pathlib import Path
from config import *
from statistics import mean
from bson import ObjectId
import time
from io import BytesIO
from PIL import Image
import ast


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Made-With"] = f"<3 from radi8"
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(500)
async def error_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html", {"request": request}, status_code=500
    )


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    if "ref" in request.query_params and request.query_params["ref"] == "taaft":
        return RedirectResponse(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ", status_code=302
        )
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/updates")
async def updates(request: Request):
    return templates.TemplateResponse("updates.html", {"request": request})


@app.get("/faq")
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})


@app.post("/generate")
async def upload_image(request: Request, image: UploadFile = File(...)):
    if (
        not image.filename.endswith(".jpg")
        and not image.filename.endswith(".jpeg")
        and not image.filename.endswith(".png")
    ):
        raise HTTPException(400, "Invalid image format. Only JPG/JPEG/PNG is accepted.")
    compressedImage = BytesIO()
    Image.open(BytesIO(image.file.read())).convert("RGB").save(
        compressedImage, format="JPEG", quality=85
    )
    compressedImage.seek(0)
    image_parts = [
        {"mime_type": "image/jpeg", "data": compressedImage.read()},
    ]
    prompt_parts = [
        "Rate this image",
        image_parts[0],
    ]
    response = model.generate_content(prompt_parts)
    responseJSON = ast.literal_eval(response.text)

    del image  # to ensure file data does not remain in memory / protect privacy
    del compressedImage

    if response.prompt_feedback.block_reason:
        return templates.TemplateResponse("inappropriate.html", {"request": request})
    if "error" in responseJSON and responseJSON["error"] == "not face":
        return templates.TemplateResponse("noface.html", {"request": request})

    clothesRating, clothesReason = responseJSON["clothes"].values()
    vibesRating, vibesReason = responseJSON["vibes"].values()
    bgRating, bgReason = responseJSON["background"].values()
    rizzRating, rizzReason = responseJSON["rizz"].values()
    styleRating, styleReason = responseJSON["style"].values()
    humorRating, humorReason = responseJSON["humor"].values()
    bonusPoints, bonusPointsReason = responseJSON["bonus"].values()
    overallReason = responseJSON["overall"]
    tips = responseJSON["tips"]

    overallPoints = (
        round(
            mean(
                [
                    clothesRating,
                    vibesRating,
                    bgRating,
                    rizzRating,
                    styleRating,
                    humorRating,
                ]
            )
        )
        + int(bonusPoints)
    )

    roast = coll.insert_one(
        {
            "overallRating": overallPoints,
            "overall": overallReason,
            "rizzRating": rizzRating,
            "rizzReason": rizzReason,
            "clothesRating": clothesRating,
            "clothesReason": clothesReason,
            "vibeRating": vibesRating,
            "vibeReason": vibesReason,
            "bgRating": bgRating,
            "bgReason": bgReason,
            "styleRating": styleRating,
            "styleReason": styleReason,
            "humorRating": humorRating,
            "humorReason": humorReason,
            "bonusPoints": bonusPoints,
            "bonusPointsReason": bonusPointsReason,
            "improvementTips": tips,
        }
    )
    return RedirectResponse(f"/roast/{roast.inserted_id}", status_code=302)


@app.get("/roast/{roastID}")
async def roast(request: Request, roastID: str):
    dbRoast = coll.find_one({"_id": ObjectId(roastID)})
    if dbRoast:
        if "full-text" in dbRoast:
            newline = "\n"
            full_text = "<p>" + dbRoast["full-text"].replace("\n", "</p><p>") + "</p>"
            return templates.TemplateResponse(
                "rawres.html",
                {
                    "request": request,
                    "full_text": full_text,
                },
            )
        else:
            return templates.TemplateResponse(
                "rating.html", {"request": request, "roast": dbRoast}
            )
    else:
        return templates.TemplateResponse("notfound.html", {"request": request})
