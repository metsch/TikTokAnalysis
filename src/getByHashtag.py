from TikTokApi import TikTokApi
from TikTokApi.browser import set_async
import pandas as pd
import time

from TikTokApi import TikTokApi
api = TikTokApi()

customFP = "INPUT CUSTOM FP HERE"
temp = api.byHashtag(hashtag="trump2020",custom_verifyFp=customFP)

df = pd.DataFrame(temp)

timestamp = int(time.time())
df.to_csv("trump_10_"+str(timestamp)+".csv")

