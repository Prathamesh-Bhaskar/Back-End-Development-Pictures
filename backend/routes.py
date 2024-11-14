from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all picture URLs in JSON format."""
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a single picture URL with its ID."""
    if 0 <= id < len(data):  # Check if the id is within the valid range
        picture = {
            "id": id,
            "url": data[id]
        }
        return jsonify(picture), 200  # Return the picture object with the id and url
    else:
        return {"message": "Picture not found"}, 404  # Return error if not found




######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Add a new picture to the data list if it doesn't already exist."""
    new_picture = request.get_json()
    picture_id = new_picture.get("id")

    # Check if picture with the given ID already exists
    if any(picture["id"] == picture_id for picture in data):
        return jsonify({"Message": f"picture with id {picture_id} already present"}), 302

    # Append the new picture to the data and return 201 Created status
    data.append(new_picture)
    return jsonify(new_picture), 201




######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture in the data list."""
    updated_picture = request.get_json()  # Get data from request body

    # Find and update the picture with the specified ID
    for picture in data:
        if picture["id"] == id:
            # Update only the fields provided in the request, leaving others intact
            for key, value in updated_picture.items():
                picture[key] = value
            return jsonify(picture), 200

    # If the picture is not found, return a 404 error
    return jsonify({"message": "picture not found"}), 404



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its ID."""
    global data
    # Filter out the picture with the specified ID
    new_data = [picture for picture in data if picture["id"] != id]

    if len(new_data) == len(data):  # No picture was deleted
        return jsonify({"message": "picture not found"}), 404

    # Update data list and confirm deletion
    data = new_data
    return jsonify({"message": "picture deleted successfully"}), 200

