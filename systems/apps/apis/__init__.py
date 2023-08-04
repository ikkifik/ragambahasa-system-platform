from flask import Blueprint

# Defining a blueprint
bp = Blueprint('api', __name__)

from apps.apis import common_contrib_routes
from apps.apis import admin_contrib_routes
from apps.apis import manage_user_routes
from apps.apis import manage_sources_routes
from apps.apis import manage_domicile_routes
from apps.apis import manage_language_routes
from apps.apis import newsletter_routes