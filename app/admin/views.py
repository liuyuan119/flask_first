from app.admin import admin


@admin.route("/")
def index():
    return "<h1 style='color:red'> this is admin.</h1>"


@admin.route("/test/")
def test():
    return "<h1 style='color:red'> this is admin.test</h1>"