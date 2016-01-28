# -*- conding: utf-8 -*-
from sqlalchemy import create_engine

scheme = 'mysql+pymysql://root:123456@localhost:3306/dev_shopping?charset=utf8' # noqa
engine = create_engine(scheme, pool_size=10)
connection = engine.connect()
print type(connection)


# connection = engine.connect()
# trans = connection.begin()
# sql = """
# INSERT INTO `tmp` (`id`, `name`, `target_type`, `target_name`, `target_param`, `image_hash`, `created_at`, `ranking_weight`, `is_need_mark`, `animation_type`) # noqa
# VALUES (6, 'xxxx', 1, '', 'http://zaocan.elenet.me', 'de6d5057729d87cacf7c5ccff70c3png', '2015-06-17 00:00:00', NULL, 0, 0); # noqa
# """
# try:
#     connection.execute(sql)
#     trans.commit()
# except:
#     trans.rollback()
#     raise
