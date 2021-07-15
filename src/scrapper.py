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

    item_box = soup.select_one(".highlight").find_all("a", {"class": "swiper-slide"})
    highlights = []
    for child in item_box:
        highlight_url = child["href"]
        info = child.div
        data_src = info.picture.img["data-src"]
        title = info.div.strong.text
        text = info.div.p.text

        highlights.append({
            "url": highlight_url,
            "data_src": data_src,
            "title": title,
            "text": text
        })


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
            "url": review_url,
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
            "url": news_url,
            "subject": subject,
            "headline": headline,
            "text": text,
            "images": images
        })

    item_box = soup.select_one("div.row:nth-child(3)").find_all("div", attrs={"class": "small"})
    galleries = []
    for child in item_box:
        gallery_url = child.a["href"]
        label = child.a.div.string

        src = "srcset" if child.a.img.has_attr("srcset") else "data-srcset"
        images = decode_srcset_str(child.a.img[src])

        galleries.append({
            "url": gallery_url,
            "label": label,
            "images": images
        })

    item_box = soup.select_one("div.col-xs-12:nth-child(2)").find_all("tr", attrs={"class": "presents"})
    tour_dates = []
    for child in item_box:
        date = child.find("td", attrs={"class": "concert-date"}).span["content"]
        info = child.find("td", attrs={"itemprop": "name"})
        date_url = info.a["href"]
        band = info.a.text
        location = info.text

        tour_dates.append({
            "url": date_url,
            "date": date,
            "band": band,
            "location": location
        })

    specials = []
    item_box = soup.select_one("div.row:nth-child(6)").find_all("div", attrs={"class": "teaser"})
    for child in item_box:
        special_url = child.a["href"]
        info = child.a.div
        title = info.strong.text
        headline = ""
        try:
            headline = info.select_one("span.teaser-headline").text
        except:
            pass
        text = info.select_one("p.teaser-text").text

        src = "srcset" if child.img.has_attr("srcset") else "data-srcset"
        images = decode_srcset_str(child.img[src])

        specials.append({
            "url": special_url,
            "title": title,
            "text": text,
            "images": images
        })

    interviews = []
    item_box = soup.select_one("div.row:nth-child(7)").find_all("div", attrs={"class": "teaser"})
    for child in item_box:
        special_url = child.a["href"]
        info = child.a.div
        title = info.strong.text
        headline = ""
        try:
            headline = info.select_one("span.teaser-headline").text
        except:
            pass
        text = info.select_one("p.teaser-text").text

        src = "srcset" if child.img.has_attr("srcset") else "data-srcset"
        images = decode_srcset_str(child.img[src])

        specials.append({
            "url": special_url,
            "title": title,
            "text": text,
            "images": images
        })

    presents = []
    item_box = soup.select_one("div.row:nth-child(8)").find_all("div", attrs={"class": "swiper-slide"})
    for child in item_box:
        if "more" in child.div["class"]:
            continue

        presents_url = child.a["href"]
        image = child.a.img["src"]
        title = child.a.div.strong

        presents.append({
            "url": presents_url,
            "title": title,
            "image": image
        })

    return {
        "highlights": highlights,
        "reviews": reviews,
        "news": news,
        "galleries": galleries,
        "tour_dates": tour_dates,
        "specials": specials,
        "interviews": interviews,
        "presents": presents
    }

get_homepage_as_dict()