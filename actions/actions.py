# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import urllib.parse
#
#
class ActionSearchHotel(Action):

    def name(self) -> Text:
        return "action_search_hotel"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            city = tracker.get_slot("city")
            start_date = tracker.get_slot("start_date")
            end_date = tracker.get_slot("end_date")
            adults = tracker.get_slot("adults")
            children = tracker.get_slot("children")
            rooms = tracker.get_slot("rooms")
            user_sex = tracker.get_slot("user_sex")
            username = tracker.get_slot("username")
            
            if not city:
                dispatcher.utter_message(text= f"Ở Việt Nam không có tên thành phố này ạ. {user_sex} {username} vui lòng nhập tên thành phố đúng giúp bot với nhé!!!")
                return []

        # Mã hóa city để sử dụng trong URL
            encoded_city = urllib.parse.quote(city)
            # params = {
            # "city": city
            # # "start_date": start_date,
            # # "start_date": start_date,
            # # "min": adults,
            # # "max": children,
            # # "rooms": rooms
            # }

            # query_params = {}
            # if start_date:
            #     query_params["startDate"] = start_date
            # if end_date:
            #     query_params["endDate"] = end_date
            # if adults is not None:  # Explicit None check for optional slots
            #     query_params["adult"] = adults
            # if children is not None:
            #     query_params["children"] = children
            # if rooms is not None:
            #     query_params["roomNumber"] = rooms
            
            # url = base_url.format(city) + "&" + "&".join([f"{k}={v}" for k, v in query_params.items()])
            
            # hotels = [
            #     {"name": "Hotels A", "link": "http://localhost:3000/"},
            #     {"name": "Hotels B", "link": "http://localhost:3000/reservations"},
            #     {"name": "Hotels C", "link": "http://localhost:3000/hotel/664a46d5bc9f42f3092a74d0"}
            # ]

            try:
                # base_url ="http://localhost:5000/api/hotel/getHotelByCity/{city}"
            
                # response = requests.get(base_url)
                # response.raise_for_status()
                # hotels = response.json()  
                api_url = f"http://localhost:5000/api/hotel/getHotelByCity/{encoded_city}"
                response = requests.get(api_url)
                response.raise_for_status()  # Kiểm tra nếu có lỗi
                hotels = response.json()

                if not hotels:
                    dispatcher.utter_message(text=f"Xin lỗi {user_sex} {username}, hệ thống không có khách sạn nào ở {city} trong thời điểm này ạ. ")
                    return []

                hotel_links = ""
                for hotel in hotels:
                    hotel_links += f"- [{hotel['hotelName']}](<http://localhost:3000/hotel/{hotel['_id']}>)\n"

                message = f"Danh sách khách sạn mà chúng tôi tìm được ở {city} là:\n{hotel_links}\n Chúc {user_sex} {username} tìm được khách sạn phù hợp và trải nghiệm thật tuyệt vời cùng gia đình ạ."
        
            except requests.exceptions.RequestException as e:
                message = "Xin lỗi, chúng tôi không thể tìm thấy khách sạn nào theo yêu cầu của bạn vào lúc này."

            dispatcher.utter_message(message)
            return []
        
# rasa run --cors "*"  