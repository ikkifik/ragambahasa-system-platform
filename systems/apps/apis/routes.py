from flask import render_template
from apps.apis import bp

# # # # # # # # #
#     Base      #
# # # # # # # # #

@bp.route('/', methods=['GET'])
def index():
    return render_template('dashboard/index.html')

@bp.route('/tables', methods=['GET'])
def tables():
    return render_template('dashboard/tables.html')

@bp.route('/profile', methods=['GET'])
def profile():
    return render_template('dashboard/profile.html')

@bp.route('/forms', methods=['GET'])
def forms():
    return render_template('dashboard/forms.html')

