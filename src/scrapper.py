import requests 
from bs4 import BeautifulSoup

url = "http://www.metal.de/"

def decode_srcset_str(srcset):
    images = []
    for s in srcset.split(","):
        t = s.strip().split(" ")
        images.append({
            "url": t[0],
            "size": t[1]
        })
    return images

def get_homepage_as_dict():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    item_box = soup.find_all("div", attrs={"class": "swiper-slide item"})

    reviews = []
    for child in item_box:
        if "more-reviews" in child.div["class"]:
            continue
        genre = child.span.text
        review_url = child.a["href"]
        rating = child.select_one("a div.info div.rating div.rating-values").span.text
        band = child.select_one("a div.info strong.band").text
        album = child.select_one("a div.info span.title").text
        
        src = "srcset" if child.a.img.has_attr("srcset") else "data-srcset"
        images = decode_srcset_str(child.a.img[src])
        
        reviews.append({
            "genre": genre,
            "review_url": review_url,
            "rating": rating,
            "band": band,
            "album": album,
            "images": images
        })

    news = []
    item_box = soup.select_one("div.row:nth-child(2)").find_all("div", attrs={"class": "teaser"})
    for child in item_box:
        news_url = child.a["href"]
        info = child.a.div
        subject = info.strong.text
        headline = info.span.text
        text = info.p.text

        src = "srcset" if child.a.img.has_attr("srcset") else "data-srcset"
        images = decode_srcset_str(child.a.img[src])

        news.append({
            "news_url": news_url,
            "subject": subject,
            "headline": headline,
            "text": text,
            "images": images
        })

    return {
        "reviews": reviews,
        "news": news
    }