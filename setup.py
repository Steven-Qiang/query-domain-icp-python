#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="query-domain-icp",
    version="0.0.1",
    author="StevenQ",
    url="https://github.com/qiangmouren/query-domain-icp-python",
    description="获取域名 ICP 备案信息 自动破解滑动验证码 支持翻页",
    packages=["query_domain_icp"],
    install_requires=["ddddocr", "requests"],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    entry_points={},
)
