from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

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
        pagination: PaginationDep,
        id: int | None = Query(None, description="ID of the hotel"),
        title: str | None = Query(None, description="Hotel name"),
):
    if id or title:
        filtered_hotels = [hotel for hotel in hotels if hotel["id"] == id or hotel["title"] == title]
        return filtered_hotels
    if pagination.page and pagination.per_page:
        start_index = (pagination.page - 1) * pagination.per_page
        end_index = start_index + pagination.per_page
        return hotels[start_index:end_index]
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
