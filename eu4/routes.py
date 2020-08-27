from eu4 import app, log, api
from flask import jsonify, Response, request, render_template, flash
from flask_restplus import Resource, fields, reqparse, inputs
import numpy as np
import pandas as pd
from random import randrange
import requests
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from .endpoints.paradox import get_paradox_data
from .endpoints.steam import get_steam_data, get_player_stats, map_paradox_with_steam, map_user_with_steam
from .forms import FilteresForm


arguments = reqparse.RequestParser()
arguments.add_argument("achieved", type=int, required=False, default=None, help="1 - TRUE; 0 - FALSE")
arguments.add_argument("difficult", type=str, required=False, default=None, help="""Chose one of the:
    \'Easy\', \'Medium\', \'Hard\', \'Very Hard\', \'Insane\', \'Uncategorized\'""")
arguments.add_argument("version", type=str, required=False, default=None)
arguments.add_argument("random", type=inputs.boolean, required=False, default=False)


def filter_data(data, args):
    output = []
    for achiev in data:
        match = True
        
        if args.get("achieved"):
            if not str(args.get("achieved")) == str(achiev.get("achieved")):
                match = False

        if args.get("difficult"):
            if not achiev.get("difficult") == args.get("difficult"):
                match = False

        if args.get("version"):
            if not achiev.get("version") == args.get("version"):
                match = False

        if match:
            output.append(achiev)

    if len(output) > 0:
        if args.get("random"):
            return [output[randrange(len(output))]]
    
    return output


def get_map():
    data_paradox = get_paradox_data()
    data_steam = get_steam_data()

    data = map_paradox_with_steam(data_paradox, data_steam)

    data_user = get_player_stats(steam_id=app.config.get("STEAM_ID"))
    data = map_user_with_steam(data, data_user)

    return data


@app.route("/", methods=["GET", "POST"])
def home():
    return index()


def make_response(data):
    resp = {}
    resp["count"] = len(data)
    resp["data"] = data

    # return Response(json.dumps(resp, indent=2),
    #                 headers={"content-type": "application/json"})
    return resp


@api.route("/paradox")
class Paradox(Resource):

    def get(self):
        log.info("/get_paradox")
        data = get_paradox_data()

        return data


@api.route("/steam")
class Steam(Resource):

    def get(self):
        log.info("/get_steam")
        data = get_steam_data()

        return data


@api.route("/user")
class User(Resource):
    def get(self):
        log.info("/get_user")
        data = get_player_stats(steam_id=app.config.get("STEAM_ID"))

        return data


@api.route("/map")
class Map(Resource):

    @api.expect(arguments, validate=True)
    def get(self):
        log.info("/get_map")

        args = arguments.parse_args()
        log.debug(f"ARGS={args}")

        data = get_map()

        data = filter_data(data, args)

        return make_response(data)


@app.route("/index", methods=["GET", "POST"])
def index():
    log.info("/index")

    data = get_map()

    form = FilteresForm()
    if form.validate_on_submit():
        log.info("SUBMIT PRESS")

        args = {}
        args['achieved'] = form.achieved.data
        args['difficult'] = form.difficult.data
        args['version'] = form.version.data
        args['random'] = form.random.data
        log.debug(f"Form args = {args}")

        data = get_map()
        data = filter_data(data, args)

        flash("DONE!", "success")        
    

    return render_template("index.html", title="EU4", data=data, form=form)