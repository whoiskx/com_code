关注者总数：778

抓取方式：
    1. 得到所有好友的首页url                     get_friends_urls.py
    2. 根据好友首页url得到 简介div 解析 存储      parse_url

Facebook 属性含义
    account_name = 账户名
    home_page 本人主页
    location 所在地
    come_form 来自
    job 职业
    sex 性别
    degree 学历
    followers 粉丝

小时  小时：分钟  月/日 月  月日年

# 类选择器
.timestampContent   发帖时间
UFIShareLink        分享
_ipp  赞  分享
_3t54  赞