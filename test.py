from helper import produce_brut
import pandas as pd


df = produce_brut('allianz-1-to-94')
df.to_csv("data.csv", index=False)