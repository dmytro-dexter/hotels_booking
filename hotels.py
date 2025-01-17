from fastapi import FastAPI, Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sumy", "name": "Суми"},
    {"id": 2, "title": "Kyiv", "name": "Київ"},
    {"id": 3, "title": "Lviv", "name": "Львів"},
    {"id": 4, "title": "Konotop", "name": "Конотоп"},
    {"id": 5, "title": "Dnipro", "name": "Дніпро"},
    {"id": 6, "title": "Odesa", "name": "Одеса"},
    {"id": 7, "title": "Frankivsk", "name": "Франківськ"},
]


@router.get("/")
def get_hotels(
        id: int | None = Query(None, description="ID of the hotel"),
        title: str | None = Query(None, description="Hotel name"),
        page: int | None = Query(None),
        per_page: int | None = Query(2),
):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    if id or title:
        filtered_hotels = [hotel for hotel in hotels if hotel["id"] == id or hotel["title"] == title]

        return filtered_hotels[start_index:end_index]

    return hotels[start_index:end_index]


@router.post("/")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Sumy", "value": {
        "title": "Hotel Sumy 5 stars",
        "name": "Sumy nearby Cheshka",
    }},
    "2": {"summary": "Kyiv", "value": {
        "title": "Hotel Kyiv 4 stars",
        "name": "Kyiv nearby Dnipro",
    }},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def update_hotel_(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
