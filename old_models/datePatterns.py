import re
import datetime

month_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)"

abbr_pattern = r"(Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)"

# date pattern is (regex, strptime pattern)
date_patterns = [ 
    (r"%s \d{1,2}, \d{4}" % month_pattern, "%B %d, %Y"),
    (r"%s. \d{1,2}, \d{4}" % abbr_pattern, "%b. %d, %Y"), # Jan. 21, 2017
    (r"%s \d{1,2}, \d{4}" % abbr_pattern, "%b %d, %Y"), # Jan 21, 2017
    (r"\d{1,2}/\d{1,2}/\d{4}", "%m/%d/%Y"), # 10/21/2008
    (r"\d{1,2}/\d{1,2}/\d{2}", "%m/%d/%y"), # 10/21/08 or 1/1/03
    (r"\d{4}-\d{1,2}-\d{1,2}", "%Y-%m-%d")  # 2008-01-15
]



yearless_patterns = [
    (r"%s \d{1,2}" % month_pattern, "%B %d"), # Janurary 21, 2017
    (r"%s \d{1,2}" % abbr_pattern, "%b %d"), # Jan 21
    (r"%s. \d{1,2}" % abbr_pattern, "%b. %d"), # Jan 21
]

day_pattern = r"Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday"

day_map = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

# Input: The text of the article
# Returns: A datetime object or None if there was no match
def match_date(text):
    for pattern in date_patterns:
        match = re.search(pattern[0], text)
        if match is not None:
            try :
                raw_date = match.group(0)
                event_date = datetime.datetime.strptime(raw_date, pattern[1])
                return event_date
            except ValueError:
                continue
    return None

# Input: The text of the article
# Input: The year as an int
# Returns: A datetime object or None if there was no match
def match_date_yearless(text, year):
    for pattern in yearless_patterns:
        match = re.search(pattern[0], text)
        if match is not None:
            raw_date = match.group(0)
            try :
                event_date = datetime.datetime.strptime(raw_date, pattern[1])
                event_date = event_date.replace(year=year)
                return event_date
            except ValueError:
                continue
    return None

# Input: The text of the article
# Input: The published date of the article
# Returns: A datetime object or None if there was no match
def match_day(text, reference_date):
    match = re.search(day_pattern, text)
    if match is not None:
        day = match.group(0)
        day_idx = day_map[day]
        diff = day_idx - reference_date.weekday()
        if diff > 0:
            diff = diff - 7
        event_date = reference_date + datetime.timedelta(days=diff)
        return event_date
    return None

# Input: The text of the article
# Input: The published date of the article
# Returns: A datetime object or None if there was no match
# Can do more complicated analysis. The first date seen is not necessarily the date that someone died. Can modify the above dates to return a list of them.
def find_date(text, published_date):
    reference_date = datetime.datetime.strptime(published_date, "%Y-%m-%d")
    res = match_day(text, reference_date)
    if res is not None:
        return res
    res = match_date(text)
    if res is not None:
        return res
    res = match_date_yearless(text, reference_date.year)
    if res is not None:
        return res
    return None

def find_date_ft(text, published_date):
    reference_date = datetime.datetime.strptime(published_date, "%Y-%m-%d")
    res = match_day(text, reference_date)
    if res is not None:
        return res, 1
    res = match_date(text)
    if res is not None:
        return res, 0
    res = match_date_yearless(text, reference_date.year)
    if res is not None:
        return res, 0
    return None, 0



# WTF the gold said it happend on 2/10/14 when it was published on 2/6/14
#https://www.indystar.com/story/news/crime/2014/02/06/person-shot-during-carjacking/5263729/




    
