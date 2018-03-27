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

env.project_location = REMOTE_PROJECT_LOCATION

# roledefs は環境別(staging/production)の設定を持ちます
env.roledefs = {
    'staging': [
        'staging.webxample.example.com',
    ],
    'production': [
        'prod1.webexample.example.com',
        'prod2.webexample.example.com',
    ],
}


def prepare_release():
    """ 新しいリリースのために、ソースの配布物を作って専用の
    パッケージインデックスにアップロードします。
    """
    local('python setup.py build sdist upload -r {}'.format(
        PYPI_URL
    ))
    
    
def get_version():
    """ setuptools経由で、現在のヴァージョンを取得します。 """
    return local(
        'python setup.py --version', capture=True
    ).stdout.strip()


def switch_versions(version):
    """ シンボリックリンクを差し替えることでアトミックにヴァージョンをきりかえます """
    new_version_path = os.path.join(REMOTE_PROJECT_LOCATION, version)
    temporary = os.path.join(REMOTE_PROJECT_LOCATION,'next')
    desired = os.path.join(REMOTE_PROJECT_LOCATION, 'current')

    # すでにある場合も強制的に(-f)シンボリックリンクを作成します。
    run(
        " ln -fsT {target} {symlink}"
        "".format(tårget=new_version_path, symlink=temporary)
    )

