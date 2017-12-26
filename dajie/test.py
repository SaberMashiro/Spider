
#id 录入编号 主键自增
#title 工作名称  data[i]['title']
#corp 公司名称 data[i]['corp']
#salary 薪水 data[i]['salary']
#url 详情 data[i][salary]
#position   工作地点  data[i]['keywords'][0]
#year   工作经验  data[i]['keywords'][1]
#education   需求学历  data[i]['keywords'][2]
#otrher   要求      data[i]['keywords']

'''
create table message(
    id int  not null primary key auto_increment,
    title varchar(100),
    corp varchar(100),
    salary varchar(100),
    url varchar(100),
    position varchar(100),
    year varchar(50),
    education varchar(50),
    other varchar(200));
'''