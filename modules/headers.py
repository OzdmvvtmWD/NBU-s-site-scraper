
#default headers
DEFAULT_HEADERS = {
        "authority": "bank.gov.ua",
        "accept": "*/*",
        "accept-language": "uk-UA,uk;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6",
        "referer": "https://bank.gov.ua/ua/markets/exchangerates?date=06.02.2026&period=daily",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        #i set cookie in a headers
        "cookie": """
                    locale=ua; _ga=GA1.1.1816299331.1773655444; 
                    cf_clearance=hhwFSLaymfOSjkDNtTq9EU3j2fiy7nVnnLb.vqwKqXk-1773656469-1.2.1.1-gnW_4zA8xPLz8rTXg7fY1Vy07nXwhUJYf8LPyuMRD6TC04PEO_Yc5vaKUpo1qL7fy0Kh3gNzmwRDauEwaOY45M7
                    .gXdkVWLIXYYg6024YwpvwhJF7caRHVzizAdFguWzjSA1o.OTuOclkBJrV9dD9I3M6T42LiL0EcRjTf8eTq6efq49TIJ0DIMz4_ykJoV8b66zE4px.fyg3IAu1BZuDKaP975S58fF0Aw93haPPBQ; 
                    __cf_bm=n7fF1KIbpzwVkysfIeZGNUI2ytQv45QFX7jfu_4C9n0-1773656469.373107-1.0.1.
                    1-WtbqYnUG8vmloSjAW59sWp2k2Afx88eooXHDt1QcZ1oPrYrJM4cDW1CICCxRjm1vW5l855E0iUMjgGuCR9xsoCnHG3ni0oXk9oPloPX4Y_1L0p7JKKBpmD1rGourcX.499ai_9rq0qQ.UoMn2gUh_A; 
                    _ga_XJX0SQ6KHR=GS2.1.s1773655444$o1$g1$t1773656889$j60$l0$h0
                """
    }
