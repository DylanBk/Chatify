from datetime import timedelta
from dotenv import load_dotenv
import eventlet
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import subprocess

from . import db_functions as db
from .log_config import log_error