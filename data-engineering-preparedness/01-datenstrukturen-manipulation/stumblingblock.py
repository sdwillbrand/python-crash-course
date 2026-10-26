user = {
    "id": 2,
    "name": "Bo",
    "email": "bo@example.de",
    "status": "inactive",
}


def add_tag(user, tags=[]):  # FALLE
    user["tags"] = tags
    tags.append("processed")
    return user


add_tag(user)
add_tag(user)
add_tag(user)

print(user)
