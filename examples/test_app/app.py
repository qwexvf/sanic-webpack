from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic_webpack import Webpack

# init sanic app
app = Sanic(__name__)
# we are using jinaj2
jinja = SanicJinja2(app)

# webpack manifest path
params = {
    'DEBUG': True,
    'WEBPACK_MANIFEST_PATH': './build/manifest.json'
}

# update configs
app.config.update(params)
# init webpack extension
Webpack.init_app(app)


@app.route('/')
async def index(request):
    return jinja.render('index.html', request)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
