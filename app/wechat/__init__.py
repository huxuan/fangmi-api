#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: huxuan
Email: i(at)huxuan.org
Description: Init file for wechat blueprint.
"""

from flask import Blueprint
from flask import jsonify
from flask import url_for
from flask_oauthlib.client import OAuth
from flask_oauthlib.client import OAuthRemoteApp
from werkzeug.urls import url_parse
from werkzeug.urls import url_encode
import requests


bp_wechat = Blueprint('wechat', __name__)
oauth = OAuth()


class WechatOAuthRemoteApp(OAuthRemoteApp):

    def authorize(self, *args, **kwargs):
        response = super(WechatOAuthRemoteApp, self).authorize(*args, **kwargs)
        url = url_parse(response.headers['Location'])
        args = url.decode_query()

        # replace the nonstandard argument
        args['appid'] = args.pop('client_id')
        args['state'] = 'testing'
        # replace the nonstandard fragment
        url = url.replace(query=url_encode(args), fragment='wechat_redirect')

        response.headers['Location'] = url.to_url()
        return response

    def authorized_response(self, *args, **kwargs):
        self.access_token_params.update({
            'appid': self.consumer_key,
            'secret': self.consumer_secret,
        })
        response = super(WechatOAuthRemoteApp, self).authorized_response(
            *args, **kwargs)
        return response


# NOTE(huxuan): Reference: https://gist.github.com/tonyseek/c31557e70065948a849d
wechat = WechatOAuthRemoteApp(
    oauth,
    'wechat',
    app_key='wechat',
    consumer_key='wx9405f71ba4f268ae',
    consumer_secret='99e4f4a3c2daea6ea5cd015e810d26d5',
    request_token_params={'scope': 'snsapi_base'},
    base_url='https://api.weixin.qq.com',
    authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize',
    access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token',
    # important: ignore the 'text/plain' said by weixin api and enforce the
    #            response be parsed as json.
    content_type='application/json',
)


def hack_rubbish_wechat(uri, headers, body):
    return uri, headers, body

wechat.pre_request = hack_rubbish_wechat

@bp_wechat.record_once
def on_load(state):
    oauth.init_app(state.app)


@bp_wechat.route('/login')
def login():
    callback = url_for('.authorized', _external=True)
    return wechat.authorize(callback=callback)

ACCESS_TOKEN = ''

@bp_wechat.route('/authorized')
def authorized():
    res = wechat.authorized_response()
    if res is None:
        code = request.args['errcode']
        message = request.args['errmsg']
        raise utils.APIException(state_code=code, message=message)
    global ACCESS_TOKEN
    ACCESS_TOKEN = res['access_token']
    data = {
        'openid': res['openid'],
        'access_token': res['access_token'],
    }
    oauth_res = wechat.get('sns/auth', data=data)
    data = {
        'grant_type': 'password',
        'username': res['openid'],
        'password': res['access_token'],
        'client_id': 'fangmi-ios',
        'sns': 'wechat',
    }
    res = requests.post('http://127.0.0.1/oauth/token', data=data)
    return jsonify(res.json())

@wechat.tokengetter
def get_wechat_oauth_token():
    return (ACCESS_TOKEN, )
