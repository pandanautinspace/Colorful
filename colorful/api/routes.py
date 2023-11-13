from datetime import datetime

from flask import Response, jsonify, render_template, request
from flask_login import current_user, login_required

import colorful.db as database

from . import api_bp


@api_bp.post('/setStatus/')
@login_required
def set_status():
    status = request.json['status']
    if (status is None):
        return Response(status=400)

    user_id = int(current_user.get_id())

    dbStatus = database.Status(
        time=str(datetime.now()),
        text=status,
        latitude=request.json['latitude'],
        longitude=request.json['longitude'],
        color="White",
        user=user_id)
    database.db.session.add(dbStatus)
    database.db.session.commit()

    user = database.User.query.get(user_id)
    user.currentStatusID = dbStatus.id
    database.db.session.add(user)
    database.db.session.commit()

    return Response(status=200)


@api_bp.get('/getStatusList/')
@login_required
def get_status_list():
    users = database.User.query.all()

    stati = []
    user: database.User
    for user in users:
        if user.currentStatusID:
            status = database.Status.query.get(user.currentStatusID)
            stati.append({
                'name': user.username,
                'status': status.text,
                'color': status.color,
                'longitude': status.longitude,
                'latitude': status.latitude,
                'time': status.time
            })

    return jsonify(stati)
