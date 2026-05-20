from flask import Flask, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flask app
app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)

app.secret_key = "secretkey"
