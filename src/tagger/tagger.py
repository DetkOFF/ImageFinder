# # # # img captioning functionality using BLIP # # # #
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model     = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def img_2_text(image_path: str) -> str:
    img = Image.open(image_path).convert("RGB")
    inputs = processor(images=img, return_tensors="pt")   
    out    = model.generate(**inputs, max_new_tokens=15)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# # # # OCR functionality using EasyOCR # # # #
import easyocr
import numpy as np

reader = easyocr.Reader(['ru', 'en'], gpu=False) 

def ocr_easy(path: str) -> str:
    img = np.array(Image.open(path).convert("RGB"))
    results = reader.readtext(img, detail=0) 
    return "\n".join(results)

# # # # Main function to generate caption from image # # # #
import os

def generate_caption(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The image at {image_path} does not exist.")
    
    caption = img_2_text(image_path)
    caption_ocr = ocr_easy(image_path)
    if caption_ocr is not None and caption_ocr != "" and not caption_ocr.isspace(): 
        caption += "\n" + caption_ocr

    return caption

# # # # Function to stream captions from a directory # # # #
import json

def stream_captions(input_dir: str, out_path: str):
    with open(out_path, "a", encoding="utf-8") as fout:
        for fn in os.listdir(input_dir):
            if not fn.lower().endswith((".jpg", ".png", ".jpeg")):
                continue
            path = os.path.join(input_dir, fn)
            caption = generate_caption(path)
            record = {"filename": fn, "caption": caption}
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
            fout.flush()

stream_captions("/../Imgs", "/../captions.jsonl")