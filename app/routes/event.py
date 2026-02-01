from fastapi import APIRouter, Response, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.models import Event
from app.utils.db_populate import bill_dict, user_dict, event_dict

router = APIRouter(prefix="/users/{user_id}", tags=["events"])

@router.get("/events", status_code=200)
def get_user_events(user_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    all_user_events = {}
    for event_id , event_data in event_dict.items():
        if event_data.get("user_id") == user_id:
            all_user_events[event_id] = event_data
    return all_user_events

@router.get("/events/{bill_id}", status_code=200)
def get_user_event_by_id(user_id:int,event_id:int , response = Response):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    if event_id not in event_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"Event {event_id} not found"
        )
    if event_dict[event_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot access since user id doesnt match"
        )
    return event_dict[event_id]

@router.post("/events", status_code=201)
def create_event(user_id:int , event:Event):
    if user_id not in user_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
        )
    event_dict[event.event_id] = jsonable_encoder(event)
    return event

@router.patch("/events/{event_id}" , status_code=200)
def update_event(user_id:int , event_id:int , event:Event):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if event_id not in event_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"event {event_id} not found"
        )
    
    if event_dict[event_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot update since user id doesnt match"
        )
    stored_event = event_dict[event_id]
    stored_event_data = Event(**stored_event)

    update_data = event.model_dump(exclude_unset=True)
    updated_data = stored_event_data.model_copy(update=update_data)
    event_dict[event_id] = jsonable_encoder(updated_data)
    return event_dict[event_id]

@router.delete("/events/{event_id}" , status_code=204)
def delete_event(user_id:int , event_id:int ):
    if user_id not in user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if event_id not in event_dict:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail=f"event {event_id} not found"
        )
    if event_dict[event_id].get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="cannot delete since user id doesnt match"
        )
    del event_dict[event_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)