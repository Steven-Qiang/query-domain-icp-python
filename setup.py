#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="query-domain-icp",
    version="0.0.3",
    author="StevenQ",
    url="https://github.com/qiangmouren/query-domain-icp-python",
    description="获取域名 ICP 备案信息 自动破解滑动验证码 支持翻页",
    packages=["query_domain_icp"],
    install_requires=["ddddocr", "requests"],
    long_description="Python 获取域名 ICP 备案信息 自动破解滑动验证码 支持翻页\n\n数据来源工信部备案系统 https://beian.miit.gov.cn/\n\n本项目仅供学习交流请勿用于非法用途",
    long_description_content_type="text/markdown",
    entry_points={},
)
