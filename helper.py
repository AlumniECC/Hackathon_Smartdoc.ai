import pandas as pd
import numpy as np
import json

def produce_brut(assureur):
    with open('data/ocr/{}.json'.format(assureur), 'r',encoding="utf8") as f:
        data = json.load(f)
    pages_content=data["responses"]
    num_page=0
    df=[]
    for page in pages_content:
        num_page+=1
        if "fullTextAnnotation" not in page:
            continue
        p=page["fullTextAnnotation"]["pages"]
        for e in p:
            blocks=e["blocks"]
            page_features=[]
            for block in blocks:
                for para in block["paragraphs"]:
                    # collect text
                    text = ""
                    for word in para["words"]:
                        #print("-----")
                        #print(word)
                        for symbol in word["symbols"]:
                            if symbol["confidence"]>=0.8:
                                text += symbol["text"]
                        text+=" "
                    # extract bounding box features
                    x_list = []
                    y_list = []
                    for v in para["boundingBox"]["normalizedVertices"]:
                        x_list.append(v["x"])
                        y_list.append(v["y"])
                    f = {}
                    f["num_page"]=num_page
                    f["text"] = text
                    f["width"] = max(x_list) - min(x_list)
                    f["height"] = max(y_list) - min(y_list)
                    f["area"] = f["width"] * f["height"]
                    f["chars"] = len(text)
                    f["char_size"] = f["area"] / f["chars"] if f["chars"] > 0 else 0
                    f["pos_x"] = (f["width"] / 2.0) + min(x_list)
                    f["pos_y"] = (f["height"] / 2.0) + min(y_list)
                    f["aspect"] = f["width"] / f["height"] if f["height"] > 0 else 0
                    f["layout"] = "h" if f["aspect"] > 1 else "v"
                    f["x0"]=x_list[0]
                    f["x1"]=x_list[1]
                    f["y0"]=y_list[0]
                    f["y1"]=y_list[1]
                    page_features.append(f)
            df=df+page_features   
    df=pd.DataFrame(df)
    df["assureur"]=assureur
    return df
