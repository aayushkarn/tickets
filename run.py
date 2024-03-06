from main import create_app

app = create_app()

# @app.route("/static/<path:path>")
# def serve_static(path):
#     path = os.path.join(app.config['STATIC_PATH'],path)
#     return send_file(path)

if __name__ == "__main__":
    app.run(threaded=True)