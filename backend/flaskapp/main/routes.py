from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/home/")
def home():
	return jsonify("This is homepage.")

