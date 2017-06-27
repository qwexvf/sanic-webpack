try:
    import ujson as json
except ImportError:
    import json


class Webpack:
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Mutate the application passed in as explained here:
        http://flask.pocoo.org/docs/0.10/extensiondev/

        :param app: Sanic application
        :return: None
        """

        # Setup a few sane defaults.
        app.config.setdefault('WEBPACK_MANIFEST_PATH',
                              '/tmp/themostridiculousimpossiblepathtonotexist')
        app.config.setdefault('WEBPACK_ASSETS_URL', None)

        self._set_asset_paths(app)

        # We only want to refresh the webpack stats in development mode,
        # not everyone sets this setting, so let's assume it's production.
        # if app.config.get('DEBUG', False):
        #    app.before_request(self._refresh_webpack_stats)
        # Not sure what it is.

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['webpack'] = self

        @app.middleware('request')
        async def add_webpack_to_request(request):
            if 'javascript_tag' not in request:
                request['javascript_tag'] = self.javascript_tag
                request['stylesheet_tag'] = self.stylesheet_tag
                request['asset_url_for'] = self.asset_url_for

    def _set_asset_paths(self, app):
        """
        Read in the manifest json file which acts as a manifest for assets.
        This allows us to get the asset path as well as hashed names.

        :param app: Sanic application
        :return: None
        """
        webpack_stats = app.config['WEBPACK_MANIFEST_PATH']

        try:
            with open(webpack_stats) as stats_json:
                stats = json.load(stats_json)

                if app.config['WEBPACK_ASSETS_URL']:
                    self.assets_url = app.config['WEBPACK_ASSETS_URL']
                else:
                    self.assets_url = stats['publicPath']

                self.assets = stats['assets']
        except IOError:
            raise RuntimeError(
                "Sanic-Webpack requires 'WEBPACK_MANIFEST_PATH' to be set and "
                "it must point to a valid json file.")

    def _refresh_webpack_stats(self):
        """
        Refresh the webpack stats so we get the latest version. It's a good
        idea to only use this in development mode.

        :return: None
        """
        self._set_asset_paths(self.app)

    def javascript_tag(self, *args):
        """
        Convenience tag to output 1 or more javascript tags.

        :param args: 1 or more javascript file names
        :return: Script tag(s) containing the asset
        """
        tags = []

        for arg in args:
            asset_path = self.asset_url_for('{0}.js'.format(arg))
            if asset_path:
                tags.append('<script src="{0}"></script>'.format(asset_path))

        return '\n'.join(tags)

    def stylesheet_tag(self, *args):
        """
        Convenience tag to output 1 or more stylesheet tags.

        :param args: 1 or more stylesheet file names
        :return: Link tag(s) containing the asset
        """
        tags = []

        for arg in args:
            asset_path = self.asset_url_for('{0}.css'.format(arg))
            if asset_path:
                tags.append(
                    '<link rel="stylesheet" href="{0}">'.format(asset_path))

        return '\n'.join(tags)

    def asset_url_for(self, asset):
        """
        Lookup the hashed asset path of a file name unless it starts with
        something that resembles a web address, then take it as is.

        :param asset: A logical path to an asset
        :type asset: str
        :return: Asset path or None if not found
        """
        if '//' in asset:
            return asset

        if asset not in self.assets:
            return None

        return '{0}{1}'.format(self.assets_url, self.assets[asset])
