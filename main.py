from fastapi import FastAPI, UploadFile, HTTPException, Request, File, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import secrets
import google.generativeai as genai
from pathlib import Path
from config import *
from statistics import mean
from bson import ObjectId


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def upload_image(request: Request, image: UploadFile = File(...)):
    if not image.filename.endswith(".jpg") and not image.filename.endswith(".jpeg"):
        raise HTTPException(400, "Invalid image format. Only JPG/JPEG is accepted.")
    image_parts = [
        {"mime_type": "image/jpeg", "data": image.file.read()},
    ]
    prompt_parts = [
        prompt,
        image_parts[0],
    ]
    response = model.generate_content(prompt_parts)
    print(response.prompt_feedback)
    if "block_reason" in response.prompt_feedback:
        return templates.TemplateResponse("error.html", {"request": request})
    print(response.text)
    for line in response.text.splitlines():
        if not line == "":
            line = line.strip()
            if line.startswith("Clothes: "):
                line = line.split(": ")
                clothesRating = line[1].split("/10. ")[0]
                clothesReason = line[1].split("/10. ")[1]
            elif line.startswith("Vibes: "):
                line = line.split(": ")
                vibeRating = line[1].split("/10. ")[0]
                vibeReason = line[1].split("/10. ")[1]
            elif line.startswith("Background: "):
                line = line.split(": ")
                bgRating = line[1].split("/10. ")[0]
                bgReason = line[1].split("/10. ")[1]
            elif line.startswith("Rizz: "):
                line = line.split(": ")
                rizzRating = line[1].split("/10. ")[0]
                rizzReason = line[1].split("/10. ")[1]
            elif line.startswith("Style: "):
                line = line.split(": ")
                styleRating = line[1].split("/10. ")[0]
                styleReason = line[1].split("/10. ")[1]
            elif line.startswith("Humor check: "):
                line = line.split(": ")
                humorRating = line[1].split("/10. ")[0]
                humorReason = line[1].split("/10. ")[1]
            elif line.startswith("Caption: "):
                line = line.split(": ")
                caption = line[1]
            elif line.startswith("Bonus points: "):
                line = line.split(": ")
                bonusPoints = line[1].split("/3. ")[0]
                bonusPointsReason = line[1].split("/3. ")[1]
            elif line.startswith("Overall: "):
                line = line.split(": ")
                overallReason = line[1]
            elif line.startswith("Improvement Tips: "):
                line = line.split(": ")
                if len(line) == 1:
                    improvementTips = "None"
                improvementTips = line[1]

    roast = coll.insert_one(
        {
            "overallRating": round(
                mean(
                    [
                        int(rizzRating),
                        int(clothesRating),
                        int(vibeRating),
                        int(bgRating),
                        int(styleRating),
                        int(humorRating),
                    ]
                )
            )
            + int(bonusPoints),
            "overall": overallReason,
            "rizzRating": rizzRating,
            "rizzReason": rizzReason,
            "clothesRating": clothesRating,
            "clothesReason": clothesReason,
            "vibeRating": vibeRating,
            "vibeReason": vibeReason,
            "bgRating": bgRating,
            "bgReason": bgReason,
            "styleRating": styleRating,
            "styleReason": styleReason,
            "humorRating": humorRating,
            "humorReason": humorReason,
            "bonusPoints": bonusPoints,
            "bonusPointsReason": bonusPointsReason,
            "improvementTips": improvementTips,
        }
    )
    return RedirectResponse(f"/roast/{roast.inserted_id}", status_code=302)


@app.get("/roast/{roastID}")
async def roast(request: Request, roastID: str):
    dbRoast = coll.find_one({"_id": ObjectId(roastID)})
    if dbRoast:
        return templates.TemplateResponse(
            "rating.html", {"request": request, "roast": dbRoast}
        )
    else:
        return templates.TemplateResponse("notfound.html", {"request": request})

@app.get("/faq")
async def faq(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request })