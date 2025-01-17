from fastapi import FastAPI, Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sumy", "name": "sumy"},
    {"id": 2, "title": "Kyiv", "name": "kyiv"},
]


@router.get("/")
def get_hotels(
        id: int | None = Query(None, description="ID of the hotel"),
        title: str | None = Query(None, description="Hotel name"),
):
    if id or title:
        return [hotel for hotel in hotels if hotel["id"] == id or hotel["title"] == title]
    return hotels


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
