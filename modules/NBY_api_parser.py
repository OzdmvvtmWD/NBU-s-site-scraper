import os
import json
import logging
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
# from pprint import pprint
from urllib.error import URLError, HTTPError

from CONFIG import JSON_DIR, LOGS_DIR, DEFAULT_HEADERS

#its APi for scrape exchange_rate
API_URL='https://bank.gov.ua/ua/tables/exchangerate-chart'

logging.basicConfig(level=logging.INFO, filename=os.path.join(LOGS_DIR, 'nbu_parser_logs.log'),filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s")


def analyze_exchange_rate_dict(json_data: dict) -> tuple[dict, dict, float]:
    EUR_dict = {}
    try:
        data = json_data.get('data', '')

        if not data:
            logging.error("Invalid JSON structure: 'data' key is missing or empty")
            raise AttributeError
        
        logging.info("DATA json is not empty!")
        logging.info("Creating EUR_dict for easier work.")

        for dt in data:
            EUR_dict[dt.get('date')] = dt.get('EUR')

        logging.info("EUR_dict is succesfull created.")
        logging.info("Computing minimal exchange rate date.")

        min_val = min(EUR_dict.values())
        min_exchange_rate_date = [k for k, v in EUR_dict.items() if v == min_val]

        #save like that is because there are can be one min/max exchange_rate and couple of date
        data_min_exchange_rate = {
            min_val : min_exchange_rate_date
        }
        logging.info("Minimal exchange rate date is succesfull computed.")
        logging.info("Computing maximal exchange rate date.")

        max_val = max(EUR_dict.values())
        max_exchange_rate_date = [k for k, v in EUR_dict.items() if v == max_val]

        data_max_exchange_rate = {
            max_val : max_exchange_rate_date
        }
        logging.info("Maximal exchange rate date is succesfull computed.")
        logging.info("Computing avg exchange rate.")

        try:

            avg_f = lambda d: sum(d.values()) / len(d)
            avg = avg_f(EUR_dict)
        
        except ZeroDivisionError as e:
            print("Division by zero while calculating the average exchange rate:", e)
            logging.error(f"Division by zero while calculating the average exchange rate: {e}")

        logging.info("AVG exchange rate is succesfull computed.")
        return data_min_exchange_rate, data_max_exchange_rate, avg
    
    except AttributeError as e:
        print("Invalid JSON structure. Failed to access expected attributes:", e)
        logging.error("Invalid JSON structure. Failed to access expected attributes:", e)

    except Exception as e:
        logging.error("Unexpected error during exchange rate analysis:", e)
        print("Unexpected error during exchange rate analysis:", e)

    return None, None, None



def save_result_as_json(json_data: dict, file_name: str = None) -> None:
    json_file_name = f'exchange_rate.json' if not file_name else file_name
    try:
        with open(os.path.join(JSON_DIR, json_file_name), 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, indent=4))
            logging.info(f"Json is saved to {JSON_DIR}")

    
    except Exception as e:
        logging.error("Failed to save JSON file:", e)
        print("Failed to save JSON file:", e)

def is_valid_dates(startDate: str, endDate: str):
    try:
        logging.info("Parsing dates")

        startDate_obj = datetime.strptime(startDate, '%d.%m.%Y')
        endDate_obj = datetime.strptime(endDate, '%d.%m.%Y')
        logging.info("Dates are correct parsed")

        delt = endDate_obj - startDate_obj

        if delt <= timedelta(0):
            logging.error(f'End date is lower than Start date \n startDate:{startDate} - endDate:{endDate}')
            print(f'End date is lower than Start date \n startDate:{startDate} - endDate:{endDate}')
            raise ValueError
        
        logging.info("Dates is valid!")
        return True

    except ValueError as e:
        logging.error(f"Invalid date format or logic!", e)
        print(f"Invalid date format or logic!", e)

    except Exception as e:
        logging.error("Unexpected error:", e)
        print("Unexpected error:", e)

    return False


def get_exchange_rate_by_date(startDate: str, 
                              endDate: str, 
                              #i use default headers from NBU site
                              headers: dict=DEFAULT_HEADERS,
                              is_save_json: bool =True
                              ) -> dict: 
    
    if not is_valid_dates(startDate, endDate):
        return 
    

    #payload for request 
    values = {"cn[]" : 'EUR', 'startDate': startDate, 'endDate': endDate}
    url_values = urllib.parse.urlencode(values)
    full_url = API_URL + '?' + url_values
    logging.debug(f"Full url is:\n{full_url}")


    try:
        logging.info("Making request")
        req = urllib.request.Request(full_url, headers=headers)

        with urllib.request.urlopen(req) as response:
            if response.code != 200:
                logging.error("Expected code 200, but code is", response.code)
                print("Expected code 200, but code is", response.code)
                raise HTTPError
            
            logging.info("Request success, response code is 200!")
            data = response.read()
            encoding = response.info().get_content_charset('utf-8')
            json_data = json.loads(data.decode(encoding))

            if is_save_json:
                file_name = f'exchange_rate_{startDate}-{endDate}.json'
                logging.info("Saving json")
                save_result_as_json(json_data, file_name)

        return json_data

    #error catcher
    except HTTPError as e:
        print("The server could not fulfill the request.")
        print("Error code:", e.code)
        logging.error(f""""The server could not fulfill the request. \nError code: {e.code} """)

    except URLError as e:
        print("Failed to reach the server.")
        print("Reason:", e)
        logging.error(f""""Failed to reach the server. \nReason: {e} """)

    except AttributeError as e:
        print("Failed to convert response data to JSON.")
        print("Reason:", e)
        print("Response data preview:\n", data[:500])
        logging.error(f""""Failed to convert response data to JSON. \nReason: {e} \nResponse data preview:\n", data[:500]""")

    except Exception as e:
        print("Unexpected exception occurred while making the request.")
        print("Reason:", e)
        logging.error(f""""Unexpected exception occurred while making the request. \nReason:, {e}""")

    return None

# its just for testing
def main():
    data = get_exchange_rate_by_date(startDate="23.04.2016",endDate="23.04.2026")

    if not data:
        return None
    
    min_exchange_rate_date, max_exchange_rate_date, avg = analyze_exchange_rate_dict(data)
    print(min_exchange_rate_date, max_exchange_rate_date, avg)

if __name__ == "__main__":
    main()

