import requests
import json
import random

def randomGifUrl():
    # set the apikey and limit
    apikey = "LIVDSRZULELA"  # test value
    lmt = 8
    
    # our test search
    search_term = "zelda"
    
    # get random results using default locale of EN_US
    r = requests.get(
        "https://g.tenor.com/v1/random?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    
    if r.status_code == 200:
        gifs = json.loads(r.content)
        #Get random gif
        gif = random.choice(gifs['results'])
        url = gif['url']
    else:
        gifs = None
    return url
