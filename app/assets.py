from flask_assets import Bundle

common_css = Bundle(
    'css/bootstrap.min.css',
    'css/main.css',
    filters='cssmin',
    output='public/common.min.css'
)

common_js = Bundle(
    'js/jquery.min.js',
    'js/bootstrap.min.js',
    'js/main.js',
    filters='jsmin',
    output='public/common.min.js'
)
