# main 目录: 包含主业务逻辑的路由和视图
# 将 main 声明成蓝图的程序

from flask import Blueprint
main = Blueprint('main',__name__)
from . import views