import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sumy", "name": "sumy"},
    {"id": 2, "title": "Kyiv", "name": "kyiv"},
]


@app.get("/")
def get_hotels(
        id: int | None = Query(None, description="ID of the hotel"),
        title: str | None = Query(None, description="Hotel name"),
):
    if id or title:
        return [hotel for hotel in hotels if hotel["id"] == id or hotel["title"] == title]
    return hotels


@app.post("/hotels")
def create_hotel(
        title: str = Body(),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def update_hotel_(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    global hotels
    if title or name:
        for hotel in hotels:
            if hotel["id"] == hotel_id:
                if title and name:
                    hotel["title"] = title
                    hotel["name"] = name
                if title:
                    hotel["title"] = title
                if name:
                    hotel["name"] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
