import threading

import requests
import time
from bs4 import BeautifulSoup
import pymongo
import lxml

from config import HEADERS, URL, CHANNEL_ID, TOKEN, URI
from diagram.diagram import Diagram
from bot.LogHandler import LogHandler


class Parser:
    cached_numbers = {}
    log_handler = None

    @staticmethod
    def get_html():
        response = requests.get(url=URL, headers=HEADERS)
        response.raise_for_status()
        return response.text

    @staticmethod
    def parse_numbers(html):
        soup = BeautifulSoup(html, 'lxml')
        results = soup.find_all('tr', class_='tm-row-selectable')
        numbers = []
        for row in results:
            number = row.find('div', class_='table-cell-value tm-value').text
            price = row.find('div', class_='table-cell-value tm-value icon-before icon-ton').text
            numbers.append({'number': number, 'price': price})
        return numbers

    @staticmethod
    def save_numbers(numbers):
        client = pymongo.MongoClient(URI)
        db = client['fragment']
        db.numbers.delete_many({})
        db.numbers.insert_many(numbers)

    @staticmethod
    def extract_numbers():
        while True:
            try:
                html = Parser.get_html()
                numbers = Parser.parse_numbers(html)
                if numbers:
                    Parser.save_numbers(numbers)
                    Parser.update_numbers()
                    Diagram.generate(Parser.cached_numbers)
                    Parser.log_handler.send_parsing_update_message()
                print(f'Parsing and updating at {time.strftime("%H:%M, %d.%m.%Y")}')
                time.sleep(300)
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while extracting numbers: {e}")
                time.sleep(10)

    @staticmethod
    def retrieve_numbers(limit=10):
        client = pymongo.MongoClient(URI)
        db = client['fragment']

        pipeline = [
            {'$group': {'_id': '$price', 'count': {'$sum': 1}}},
            {'$sort': {'_id': 1}},
            {'$limit': limit}
        ]

        result = db.numbers.aggregate(pipeline)
        counts_sorted = {item['_id']: item['count'] for item in result}

        return counts_sorted

    @staticmethod
    def update_numbers():
        Parser.cached_numbers = Parser.retrieve_numbers()

    @staticmethod
    def parse_and_update():
        while True:
            Parser.extract_numbers()

    @staticmethod
    def start():
        thread = threading.Thread(target=Parser.parse_and_update)
        thread.daemon = True
        thread.start()
        Parser.log_handler = LogHandler(TOKEN, CHANNEL_ID)
