# -*- coding:utf-8 -*-
import os

from fabric.api import *  # nopa
from fabric.contrib.files import exists


# 'devpi'を使って専用のパケージインデックスを作ったとします
PYPI_URL = 'http://devpi.webxample.example.com'

'''
これはリリース版をインストールするリモートサーバーのパスです。
リリースディレクトリはプロジェクトのヴァージョンごとに分かれていて
それぞれが独立した仮想環境ディレクトリです。
'current'は最後にデプロイされたヴァージョンを指すシンボリックリンクです。
このシンボリックリンクはプロセス監視ツールなどで参照されるディレクトリパスです。
例:
|---0.0.1
|---0.0.2
|---0.0.3
|---0.1.0
|---current -> 0.1.0/

REMOTE_PROJECT_LOCATION = "/var/projects//webxample"

env.project_locations
