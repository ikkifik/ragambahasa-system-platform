from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database

try:
    from config import config
except:
    import sys
    sys.path.append("../..")
    from config import config

db = SQLAlchemy()

if not database_exists(config.SQLALCHEMY_DATABASE_URI):
    create_database(config.SQLALCHEMY_DATABASE_URI)
elif config.DB_RECREATE:
    drop_database(config.SQLALCHEMY_DATABASE_URI)
    create_database(config.SQLALCHEMY_DATABASE_URI)

from apps.models.users import Users
from apps.models.roles import Roles
from apps.models.source_types import SourceTypes
from apps.models.domiciles import Domiciles
from apps.models.languages import Languages
from apps.models.printed_data import PrintedData
from apps.models.printed_content import PrintedContent
from apps.models.digital_data import DigitalData
from apps.models.password_reset_token import PasswordResetToken
# from apps.models.extracted_content import ExtractedContent