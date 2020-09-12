import redis
import datetime

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)


class VisitCountMiddleware(object):
    """ 访问统计 """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取request属性，
        request_meta = request.META
        response = self.get_response(request)

        # ip地址
        if request_meta.get("HTTP_X_FORWARDED_FOR"):
            ip = request_meta["HTTP_X_FORWARDED_FOR"]
        else:
            ip = request_meta["REMOTE_ADDR"]
        # 起始路径，可以统计在网站内部的访问记录，如：从A到B,起始路径就是A
        if request_meta.get('HTTP_REFERER'):
            HTTP_REFERER = request_meta['HTTP_REFERER']
        else:
            HTTP_REFERER = False
        # 目标路径，就是上面说到的B
        if request_meta.get('PATH_INFO'):
            PATH_INFO = request_meta['PATH_INFO']
        else:
            PATH_INFO = False
        # User-agent，这一项也可以用来过滤请求
        if request_meta.get('HTTP_USER_AGENT'):
            HTTP_USER_AGENT = request_meta['HTTP_USER_AGENT']
        else:
            HTTP_USER_AGENT = False
        # 请求方式
        if request_meta.get('REQUEST_METHOD'):
            REQUEST_METHOD = request_meta['REQUEST_METHOD']
        else:
            REQUEST_METHOD = False
        # 连接方式，
        if request_meta.get('HTTP_CONNECTION'):
            HTTP_CONNECTION = request_meta['HTTP_CONNECTION']
        else:
            HTTP_CONNECTION = False
        # 响应码
        response_code = response.status_code
        visit_time = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        # 组装数据，添加访问时间visit_time
        info_list = {
            'IP': ip,
            'Begin_path': HTTP_REFERER,
            'End_path': PATH_INFO,
            'User_agent': HTTP_USER_AGENT,
            'Request_method': REQUEST_METHOD,
            'Connection': HTTP_CONNECTION,
            'Response_code': response_code,
            'Visit_time': visit_time
        }

        # 调用存储数据库函数，存入数据库
        self.save_to_redis(info_list)
        return response

    def save_to_redis(self, result):
        """
        保存至Redis数据库
        :param result: type: dict
        :return:
        """
        visit_count = 0
        try:
            conn = redis.Redis(connection_pool=pool)
            if conn.get('visit_count'):
                visit_count = int(conn.get('visit_count'))
        except ConnectionError as e:
            print(e, '连接redis数据库失败')

        # 储存数据
        try:
            visit_count += 1
            conn.hmset(f'visit_info_{visit_count}', result)
            conn.set('visit_count', visit_count)
            print(f'总流量: {visit_count}')
        except Exception as e:
            print(e, '储存redis数据库失败')