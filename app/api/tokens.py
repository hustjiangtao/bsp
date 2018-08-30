# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-

"""token for auth"""


from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['GET'])
@basic_auth.login_required
def get_token():
    """get a new token"""
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({"token": token})


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """revoke token"""
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
