
import os
from flask import Flask
from app.model.models import db
from app.app1.user_views import app1_blueprint
from app.app2.user_views import app2_blueprint
from app.app3.user_views import app3_blueprint
from app.main import main
from flask_migrate import Migrate
from flask import Blueprint, render_template
config = {
    'DEBUG': False,  # 是否开启Debug模式
    'TESTING': False,  # 是否开启测试模式
    'PROPAGATE_EXCEPTIONS': None,  # 异常传播(是否在控制台打印LOG) 当Debug或者testing开启后,自动为True
    'PRESERVE_CONTEXT_ON_EXCEPTION': None,  # 一两句话说不清楚,一般不用它
    'SECRET_KEY': None,  # 之前遇到过,在启用Session的时候,一定要有它
    'PERMANENT_SESSION_LIFETIME': 31,  # days , Session的生命周期(天)默认31天
    'USE_X_SENDFILE': False,  # 是否弃用 x_sendfile
    'LOGGER_NAME': None,  # 日志记录器的名称
    'LOGGER_HANDLER_POLICY': 'always',
    'SERVER_NAME': None,  # 服务访问域名
    'APPLICATION_ROOT': None,  # 项目的完整路径
    'SESSION_COOKIE_NAME': 'session',  # 在cookies中存放session加密字符串的名字
    'SESSION_COOKIE_DOMAIN': None,  # 在哪个域名下会产生session记录在cookies中
    'SESSION_COOKIE_PATH': None,  # cookies的路径
    'SESSION_COOKIE_HTTPONLY': True,  # 控制 cookie 是否应被设置 httponly 的标志，
    'SESSION_COOKIE_SECURE': False,  # 控制 cookie 是否应被设置安全标志
    'SESSION_REFRESH_EACH_REQUEST': True,  # 这个标志控制永久会话如何刷新
    'MAX_CONTENT_LENGTH': None,  # 如果设置为字节数， Flask 会拒绝内容长度大于此值的请求进入，并返回一个 413 状态码
    'SEND_FILE_MAX_AGE_DEFAULT': 12,  # hours 默认缓存控制的最大期限
    'TRAP_BAD_REQUEST_ERRORS': False,
    # 如果这个值被设置为 True ，Flask不会执行 HTTP 异常的错误处理，而是像对待其它异常一样，
    # 通过异常栈让它冒泡地抛出。这对于需要找出 HTTP 异常源头的可怕调试情形是有用的。
    'TRAP_HTTP_EXCEPTIONS': False,
    # Werkzeug 处理请求中的特定数据的内部数据结构会抛出同样也是“错误的请求”异常的特殊的 key errors 。
    # 同样地，为了保持一致，许多操作可以显式地抛出 BadRequest 异常。
    # 因为在调试中，你希望准确地找出异常的原因，这个设置用于在这些情形下调试。
    # 如果这个值被设置为 True ，你只会得到常规的回溯。
    'EXPLAIN_TEMPLATE_LOADING': False,
    'PREFERRED_URL_SCHEME': 'http',  # 生成URL的时候如果没有可用的 URL 模式话将使用这个值
    'JSON_AS_ASCII': True,
    # 默认情况下 Flask 使用 ascii 编码来序列化对象。如果这个值被设置为 False ，
    # Flask不会将其编码为 ASCII，并且按原样输出，返回它的 unicode 字符串。
    # 比如 jsonfiy 会自动地采用 utf-8 来编码它然后才进行传输。
    'JSON_SORT_KEYS': True,
    #默认情况下 Flask 按照 JSON 对象的键的顺序来序来序列化它。
    # 这样做是为了确保键的顺序不会受到字典的哈希种子的影响，从而返回的值每次都是一致的，不会造成无用的额外 HTTP 缓存。
    # 你可以通过修改这个配置的值来覆盖默认的操作。但这是不被推荐的做法因为这个默认的行为可能会给你在性能的代价上带来改善。
    'JSONIFY_PRETTYPRINT_REGULAR': True,
    'JSONIFY_MIMETYPE': 'application/json',
    'TEMPLATES_AUTO_RELOAD': None,
}


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    #初始配置
    """ static_folder = 'static',  # 静态文件目录的路径 默认当前项目中的static目录
        static_host = None,  # 远程静态文件所用的Host地址,默认为空
        static_url_path = None,  # 静态文件目录的url路径 默认不写是与static_folder同名,远程静态文件时复用
        # host_matching是否开启host主机位匹配,是要与static_host一起使用,如果配置了static_host, 则必须赋值为True
        # 这里要说明一下,@app.route("/",host="localhost:5000") 就必须要这样写
        # host="localhost:5000" 如果主机头不是 localhost:5000 则无法通过当前的路由
        host_matching = False,  # 如果不是特别需要的话,慎用,否则所有的route 都需要host=""的参数
        subdomain_matching = False,  # 理论上来说是用来限制SERVER_NAME子域名的,但是目前还没有感觉出来区别在哪里
        template_folder = 'templates'  # template模板目录, 默认当前项目中的 templates 目录
        instance_path = None,  # 指向另一个Flask实例的路径
        instance_relative_config = False  # 是否加载另一个实例的配置
        root_path = None  # 主模块所在的目录的绝对路径,默认项目目录"""
    app = Flask(__name__,static_folder=static_dir,template_folder=templates_dir)
    app.register_blueprint(blueprint=main)
    app.register_blueprint(blueprint=app1_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=app2_blueprint, url_prefix='/index')
    app.register_blueprint(blueprint=app3_blueprint, url_prefix='/home')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Oneday0313@192.168.1.241:3306/Htai'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 设置session密钥
    app.config['SECRET_KEY'] = 'secret_key'
    # 设置连接的redis数据库 默认连接到本地6379
    # app.config['SESSION_TYPE'] = 'redis'
    # 设置远程
    # app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
    db.init_app(app=app)
    return app