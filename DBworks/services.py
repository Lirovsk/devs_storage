import json

# from DBworks.models import hability as Hability
# from DBworks.models import user as User
from DBworks.sql_services import SQLService


def create_user(dados):
    # Check if user with the same name or email already exists and return an error message if it does.
    user_by_email = SQLService.search_user_by_email(dados['email'])
    if user_by_email:
        return json.dumps({"status": 1,
                           "message": "User with the same email already exists."})

    # Create the user
    SQLService.create_user(name=dados['name'], age=dados['age'], email=dados['email'])

    # Search if the user was created and return a message confirming the creation of the user.
    user = SQLService.search_user_by_email(dados['email'])
    if user:
        return json.dumps({"status": 0,
                          "message": f"User {user.name} created successfully!"})
    else:
        return json.dumps({"status": 1,
                          "message": "User not created."})


def search_user_by_name(name):
    users = SQLService.search_user_by_name(name)
    response = []
    
    for user in users:
        response.append({"name": user.name, "email": user.email})
        
    if users:
        return json.dumps({"status": 0,
                          "message": f"Users found!",
                          "user_data": response})
    else:
        return json.dumps({"status": 1,
                          "message": "User not found."})


def search_user_by_email(email):
    user = SQLService.search_user_by_email(email)
    if user:
        return json.dumps({"status": 0,
                          "message": f"User {user.name} found!",
                          "user_data": {"name": user.name,
                                        "age": user.age,
                                        "email": user.email}})
    else:
        return json.dumps({"status": 1,
                          "message": "User not found."})


def delete_user(email):
    user = SQLService.search_user_by_email(email)
    if user:
        returned = SQLService.delete_user(user_email=email)
        if returned == 0:
            return json.dumps({"status": 0,
                                "message": f"User {user.name} deleted successfully!"})
        else:
            return json.dumps({"status": 1,
                              "message": "User not deleted."})
    else:
        return json.dumps({"status": 1,
                          "message": "User not found."})

def create_hability(hability_name: str, hability_level: int, user_email: str, hability_description=None):
    user = SQLService.search_user_by_email(user_email)
    if user is None:
        return json.dumps({"status": 1,
                          "message": "User not found."})

    existin_hability = SQLService.search_hability_by_name(hability_name.lower(), user.id)

    if existin_hability is not None:
        return json.dumps({"status": 1,
                          "message": f"Hability with the name {hability_name} already exists for this user."})
    else:
        level = 4 if hability_level > 4 else hability_level
        SQLService.create_hability(user_name=user.name, hability_name=hability_name, hability_level=level, hability_description=hability_description)
        return json.dumps({"status": 0,
                          "message": f"Hability {hability_name} created successfully for user {user.name}!"})


def search_hability_by_name(hability_name: str, user_email: str):
    user = SQLService.search_user_by_email(user_email)
    if user is None:
        return json.dumps({"status": 1,
                          "message": "User not found."})

    hability = SQLService.search_hability_by_name(hability_name, user.id)
    if hability:
        return json.dumps({"status": 0,
                          "message": f"Hability {hability.name.title()} found for user {user.name}!",
                          "hability_data": {"name": hability.name.title(), "level": hability.level, "description": hability.description}})
    else:
        return json.dumps({"status": 1,
                          "message": f"Hability {hability_name} not found for user {user.name}."})


def delete_hability(hability_name: str, user_email: str):
    user = SQLService.search_user_by_email(user_email)
    if user is None:
        return json.dumps({"status": 1,
                          "message": "User not found."})

    hability = SQLService.search_hability_by_name(hability_name.lower(), user.id)
    if hability:
        returned = SQLService.delete_hability(hability_name, user.id)
        if returned == 0:
            return json.dumps({"status": 0,
                                "message": f"Hability {hability.name.title()} deleted successfully for user {user.name}!"})
        else:
            return json.dumps({"status": 1,
                              "message": "Hability not deleted."})
    else:
        return json.dumps({"status": 1,
                          "message": f"Hability {hability_name} not found for user {user.name}."})


def update_user (user_email: str, user_name: str, user_age: int):
    user = SQLService.search_user_by_email(user_email)
    if user is None:
        return json.dumps({"status": 1,
                          "message": "User not found."})

    returned = SQLService.update_user(user_email=user_email, user_name=user_name, user_age=user_age)
    if returned == 0:
        return json.dumps({"status": 0,
                          "message": f"User {user_name} updated successfully!"})
    else:
        return json.dumps({"status": 1,
                          "message": "User not updated."})


def update_user_email(user_email: str, new_email: str):
    user = SQLService.search_user_by_email(user_email)
    if user is None:
        return json.dumps({"status": 1,
                          "message": "User not found."})

    returned = SQLService.update_user_email(user_email=user_email, new_email=new_email)
    if returned == 0:
        return json.dumps({"status": 0,
                          "message": f"User email updated successfully!"})
    else:
        return json.dumps({"status": 1,
                          "message": "User email not updated."})
