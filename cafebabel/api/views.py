from flask import request, jsonify
from flask_login import current_user, login_required

from .. import app
from ..users.models import User, UserProfile, Role, user_datastore


@app.route('/api/user/', methods=['put'])
@login_required
def api_user_put():
    user = User.objects.get(id=current_user.id)
    data = request.get_json()
    profile_data = {k: data[k]
                    for k in ['name', 'socials', 'website', 'about']}
    current_user.profile = UserProfile(**profile_data)
    current_user.save()
    editor = Role.objects.get(name='editor')
    if data.get('is_editor'):
        user_datastore.add_role_to_user(user=user, role=editor)
    else:
        user_datastore.remove_role_from_user(user=user, role=editor)
    return jsonify(user.to_dict())


@app.route('/api/user/<id>/', methods=['delete'])
@login_required
def api_user_delete(id):
    User.objects.get(id=current_user.id).delete()
    return '', 204
