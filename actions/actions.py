# from typing import Any, Text, Dict, List
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# import aiohttp
# import urllib.parse

# class ActionSearchHotel(Action):

#     def name(self) -> Text:
#         return "action_search_hotel"

#     async def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         city = tracker.get_slot("city")
#         start_date = tracker.get_slot("start_date") or "7/7/2024"
#         end_date = tracker.get_slot("end_date") or "7/8/2024"
#         adults = tracker.get_slot("adults") or 2
#         children = tracker.get_slot("children") or 0
#         rooms = tracker.get_slot("rooms") or 1
#         user_sex = tracker.get_slot("user_sex")
#         username = tracker.get_slot("username")
        
#         if user_sex in ["Mình", "Tôi", "Tớ", "Tao"]:
#             user_sex = "Bạn"

#         if not city:
#             dispatcher.utter_message(text=f"Ở Việt Nam không có tên thành phố này ạ. {user_sex} {username} vui lòng nhập tên thành phố đúng giúp bot với nhé!!!")
#             return []

#         encoded_city = urllib.parse.quote(city)
#         base_url = "http://localhost:5000/api/hotel/getHotelBySearch"
        
#         params = {
#             "city": encoded_city,
#             "startDate": start_date,
#             "endDate": end_date,
#             "adults": adults,
#             "children": children,
#             "roomNumber": rooms
#         }

#         api_url = f"{base_url}?{urllib.parse.urlencode(params)}"

#         try:
#             response = await self.fetch_data(api_url)

#             if not response:
#                 dispatcher.utter_message(text=f"Xin lỗi {user_sex} {username}, hệ thống không phản hồi trong thời điểm này ạ.")
#                 return []

#             hotels = await response.json()

#             if not hotels:
#                 dispatcher.utter_message(text=f"Xin lỗi {user_sex} {username}, hệ thống không có khách sạn nào ở {city} trong thời điểm này ạ.")
#                 return []

#             hotel_links = ""
#             for hotel in hotels:
#                 hotel_links += f"- [{hotel['hotelName']}](<http://localhost:3000/hotel/{hotel['_id']}>)\n"

#             message = f"Danh sách khách sạn mà chúng tôi tìm được ở {city} là:\n{hotel_links}\n Chúc {user_sex} {username} tìm được khách sạn phù hợp và trải nghiệm thật tuyệt vời cùng gia đình ạ."

#         except aiohttp.ClientError as e:
#             message = "Xin lỗi, chúng tôi không thể tìm thấy khách sạn nào theo yêu cầu của bạn vào lúc này."

#         dispatcher.utter_message(message)
#         return []

#     async def fetch_data(self, url: str) -> aiohttp.ClientResponse:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 return response


# class ActionSearchByCondition(Action):

#     def name(self) -> Text:
#         return "action_search_by_condition"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         city = tracker.get_slot("city")
#         start_date = tracker.get_slot("start_date")
#         end_date = tracker.get_slot("end_date")
#         adults = tracker.get_slot("adults")
#         children = tracker.get_slot("children")
#         rooms = tracker.get_slot("rooms")
#         distance = tracker.get_slot("distance")
#         price1 = tracker.get_slot("price1")
#         price2 = tracker.get_slot("price2")
#         user_sex = tracker.get_slot("user_sex")
#         username = tracker.get_slot("username")
        
#         if user_sex in ["Mình", "Tôi", "Tớ", "Tao"]:
#             user_sex = "Bạn"
#             return user_sex

#         if not city:
#             dispatcher.utter_message(text=f"Ở Việt Nam không có tên thành phố này ạ. {user_sex} {username} vui lòng nhập tên thành phố đúng giúp bot với nhé!!!")
#             return []

#         encoded_city = urllib.parse.quote(city)
#         base_url = f"http://localhost:5000/api/hotel/getHotelByFilter?city={encoded_city}"
        
#         start_date_query = f"&startDate={start_date}" if start_date else ""
#         end_date_query = f"&endDate={end_date}" if end_date else ""
#         adults_query = f"&adult={adults}" if adults else ""
#         children_query = f"&children={children}" if children else ""
#         room_query = f"&roomNumber={rooms}" if rooms else ""
#         distance_query = f"&distance={distance}" if distance else ""
#         price_range_query = f"&priceRange={price1},{price2}" if price1 and price2 else ""

#         api_url = f"{base_url}{start_date_query}{end_date_query}{adults_query}{children_query}{room_query}{distance_query}{price_range_query}"

#         try:
#             response = requests.get(api_url)
#             response.raise_for_status()  # Kiểm tra nếu có lỗi
#             hotels = response.json()

#             if not hotels:
#                 dispatcher.utter_message(text=f"Xin lỗi {user_sex} {username}, hệ thống không có khách sạn nào ở {city} với các điều kiện bạn yêu cầu.")
#                 return []

#             hotel_links = ""
#             for hotel in hotels:
#                 hotel_links += f"- [{hotel['hotelName']}](<http://localhost:3000/hotel/{hotel['_id']}>)\n"

#             message = f"Danh sách khách sạn mà chúng tôi tìm được ở {city} với các điều kiện bạn yêu cầu là:\n{hotel_links}\n Chúc {user_sex} {username} tìm được khách sạn phù hợp và trải nghiệm thật tuyệt vời cùng gia đình ạ."

#         except requests.exceptions.RequestException as e:
#             message = f"Xin lỗi, chúng tôi không thể tìm thấy khách sạn nào theo yêu cầu của {user_sex} {username} vào lúc này."

#         dispatcher.utter_message(message)
#         return []

# rasa run --cors "*"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import urllib.parse
from datetime import datetime, timedelta

class ActionSearchHotel(Action):

    def name(self) -> Text:
        return "action_search_hotel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        # Format dates as MM/DD/YYYY
        today_str = today.strftime("%m/%d/%Y")
        tomorrow_str = tomorrow.strftime("%m/%d/%Y")
        
        start_date = tracker.get_slot("start_date") or today_str
        end_date = tracker.get_slot("end_date") or tomorrow_str
        adults = tracker.get_slot("adults") or 2
        children = tracker.get_slot("children") or 0
        rooms = tracker.get_slot("rooms") or 1
        user_sex = tracker.get_slot("user_sex")
        username = tracker.get_slot("username")
        
        if user_sex in ["Mình", "Tôi", "Tớ", "Tao"]:
            user_sex = "Bạn"

        if not city:
            dispatcher.utter_message(text=f"Ở Việt Nam không có tên thành phố này ạ. {user_sex} {username} vui lòng nhập tên thành phố đúng giúp bot với nhé!!!")
            return []

        base_url = "http://localhost:5000/api/hotel/getHotelBySearch"
        
        params = {
            "city": city,
            "startDate": start_date,
            "endDate": end_date,
            "adult": int(adults),
            "children": int(children),
            "roomNumber": int(rooms)
        }

        api_url = f"{base_url}?{urllib.parse.urlencode(params)}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Kiểm tra nếu có lỗi
            hotels = response.json()

            if not hotels:
                dispatcher.utter_message(text=f"Xin lỗi {user_sex} {username}, hệ thống không có khách sạn nào ở {city} trong thời điểm này ạ.")
                return []

            hotel_links = ""
            for hotel in hotels:
                hotel_links += f"- [{hotel['hotelName']}](<http://localhost:3000/hotel/{hotel['_id']}>)\n"

            message = f"Danh sách khách sạn mà chúng tôi tìm được ở {city} là:\n{hotel_links}\n Chúc {user_sex} {username} tìm được khách sạn phù hợp và trải nghiệm thật tuyệt vời cùng gia đình ạ."

        except requests.exceptions.RequestException as e:
            message = "Xin lỗi, chúng tôi không thể tìm thấy khách sạn nào theo yêu cầu của bạn vào lúc này."

        dispatcher.utter_message(message)
        return []
