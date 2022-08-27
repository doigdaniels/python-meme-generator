from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
import matplotlib.pyplot as plt
import nltk
import requests
import random
import numpy as np
import string
import json

debug = False
with open("config.json", "r") as f:
    config = json.load(f)


def gen_title():
    nouns = []
    adjs = []

    with open("files/narrative.txt", "r") as f:
        for l in f:
            tokens = nltk.word_tokenize(l)
            tagged = nltk.pos_tag(tokens)
            for word in tagged:
                if 'NN' in word[1] or 'NNP' in word[1]:
                    if not any(ch in string.punctuation for ch in word[0]):
                        nouns.append(word[0])
                if 'JJ' in word[1]:
                    adjs.append(word[0])

    noun = random.choice(nouns)
    adj = random.choice(adjs)

    ch = random.randrange(0, 2)
    if ch == 0:
        return f"Your {noun} is:", f"{adj} {noun}", f"{adj} {noun}"
    if ch == 1:
        return f"You {random.choice(['stepped in', 'licked', 'hear'])} it:", f"{adj} {noun}", f"{adj} {noun}"


def generate(uncannyness=random.randrange(0, 7)):
    base = Image.new('RGB', (500, 500), color=(0, 0, 0))

    # add text
    text1, text2, search_term = gen_title()

    font = ImageFont.truetype("files/FreeSans.ttf", 60)
    txt_img = Image.new('RGB', font.getbbox(text1)[2:], color=(0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((0, 0), text1, (255, 255, 255), font=font)
    txt_img = txt_img.resize((480, 60))
    base.paste(txt_img, (10, 10))

    font = ImageFont.truetype("files/FreeSansBold.ttf", 70)
    txt_img = Image.new('RGB', font.getbbox(text2)[2:], color=(0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((0, 0), text2, (255, 0, 0), font=font)
    txt_img = txt_img.resize((400, 80))
    base.paste(txt_img, (50, 80))

    # add walter white
    walt_img = Image.open(f"images/{uncannyness}.png").resize((250, 300))
    base.paste(walt_img, (0, 200))

    # add image from bing
    subscription_key = config["bing_key"]
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "license": "public", "imageType": "photo"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"]
                      for img in search_results["value"][:16]]

    image_data = requests.get(random.choice(thumbnail_urls[:5]))
    image_data.raise_for_status()
    search_img = Image.open(BytesIO(image_data.content)).resize((250, 300))
    base.paste(search_img, (250, 200))

    if debug:
        print(search_term)
        f, axes = plt.subplots(4, 4)
        for i in range(4):
            for j in range(4):
                image_data = requests.get(thumbnail_urls[i+4*j])
                image_data.raise_for_status()
                image = Image.open(BytesIO(image_data.content))
                axes[i][j].imshow(image)
                axes[i][j].axis("off")
        plt.show()

    return np.asarray(base), uncannyness


if __name__ == "__main__":
    image = Image.fromarray(generate()[0])
    image.save("out.png")
