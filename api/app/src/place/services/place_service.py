import logging

from src.place.services.place_repository import PlaceRepository

logger = logging.getLogger('app')


def convert_direction_to_representation(direction):
    direction_dict = {
        'id': direction.id,
        'name': direction.name,
        'display': direction.display,
        'departments': [
            {
                'id': department.id,
                'name': department.name,
            } for department in direction.departments
        ]
    }
    return direction_dict


def convert_place_to_representation(place):
    place_dict = {
        'id': place.id,
        'name': place.name,
        'address': place.address,
        'departments': [
            {
                'id': department.id,
                'name': department.name,
            } for department in place.departments
        ]
    }
    directions = list()
    direction_ids = list()
    for department in place.departments:
        for direction in department.directions:
            if direction.id not in direction_ids:
                direction_ids.append(direction.id)
                directions.append(
                    {
                        'id': direction.id,
                        'name': direction.name
                    }
                )
    place_dict['directions'] = directions
    return place_dict


def get_directions():
    db = PlaceRepository()
    query_result = db.get_directions()
    result = [direction[0] for direction in query_result]
    return result


def get_direction_by_id(direction_id):
    db = PlaceRepository()
    return db.get_direction_by_id(direction_id)


def get_direction_by_name(direction_name):
    db = PlaceRepository()
    return db.get_direction_by_name(direction_name)


def check_department_exists(department_id):
    db = PlaceRepository()
    department = db.get_department_by_id(department_id)
    if department:
        return True
    return False


def update_direction(direction_id, update_direction_data):
    db = PlaceRepository()
    if update_direction_data["name"] or update_direction_data["display"]:
        direction = db.update_direction(direction_id, update_direction_data)
        if not direction:
            return None
    if update_direction_data["departments"] is None:
        return get_direction_by_id(direction_id)
    db.delete_direction_departments_by_direction_id(direction_id)
    if len(update_direction_data["departments"]) > 0:
        department_ids = [department["id"] for department in update_direction_data["departments"]]
        db.save_direction_departments(direction_id, department_ids)
    return get_direction_by_id(direction_id)


def get_places():
    db = PlaceRepository()
    query_result = db.get_places()
    result = [place[0] for place in query_result]
    return result


def get_place_by_id(place_id):
    db = PlaceRepository()
    return db.get_place_by_id(place_id)


def get_place_by_name(place_name):
    db = PlaceRepository()
    return db.get_place_by_name(place_name)


def update_place(place_id, update_place_data):
    db = PlaceRepository()
    if update_place_data["name"] or update_place_data["address"]:
        place = db.update_place(place_id, update_place_data)
        if not place:
            return None
    if update_place_data["departments"] is None:
        return get_place_by_id(place_id)
    db.delete_place_departments_by_place_id(place_id)
    if len(update_place_data["departments"]) > 0:
        department_ids = [department["id"] for department in update_place_data["departments"]]
        db.save_place_departments(place_id, department_ids)
    return get_place_by_id(place_id)


def create_place(place_data):
    db = PlaceRepository()
    new_place_id = db.create_place(place_data["name"], place_data["address"])
    if place_data["departments"] is not None:
        if len(place_data["departments"]) > 0:
            department_ids = [department["id"] for department in place_data["departments"]]
            db.save_place_departments(new_place_id, department_ids)
    new_place = get_place_by_id(new_place_id)
    return new_place


def delete_place(place_id):
    db = PlaceRepository()
    db.delete_place_by_id(place_id)
    return True
