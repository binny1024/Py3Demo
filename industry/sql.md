```slq
use industry;
-- auto-generated definition
create table announcement_summary
(
    id                                int auto_increment
        primary key,
    procurement_type                  varchar(50)  null comment '采购类型',
    info_url                          varchar(500) null comment '此采购信息的地址',
    project_name                      varchar(500) null comment '采购项目名称',
    items                             varchar(500) null comment '品目',
    procurement_unit                  varchar(500) null comment '采购单位',
    administrative_region             varchar(500) null comment '行政区域',
    notice_time                       varchar(100) null comment '公告时间',
    tender_get_time                   varchar(100) null comment '获取招标的时间',
    tender_documents_selling_price    varchar(100) null comment '招标文件售价',
    tender_documents_address          varchar(500) null comment '获取招标文件的地点',
    bidding_opening_time              varchar(100) null comment '开标时间',
    bidding_opening_address           varchar(500) null comment '开标地点',
    budget_amount                     varchar(100) null comment '预算金额',
    project_contacts                  varchar(200) null comment '项目联系人',
    project_phone                     varchar(100) null comment '项目联系电话',
    procurement_unit_address          varchar(500) null comment '采购单位地址',
    procurement_unit_phone            varchar(500) null comment '采购单位联系方式',
    agency_name                       varchar(500) null comment '代理机构名称',
    agency_place                      varchar(500) null comment '代理机构地址',
    agency_phone                      varchar(500) null comment '代理机构联系方式',
    main_body                         mediumtext   null comment '公告正文',
    negotiation_doc_get_address       varchar(500) null comment '获取谈判文件的地点',
    negotiation_doc_get_date          varchar(100) null comment '获取谈判文件的时间',
    submission_deadline               varchar(100) null comment '提交文件截止时间',
    qualification_date                varchar(100) null comment '资格审查日期',
    project_tender_notice_date        varchar(100) null comment '本项目招标公告日期',
    bidding_get_date                  varchar(100) null comment '中标日期',
    professor_name_list               varchar(500) null comment '评审专家名单',
    bidding_get_total_amount          varchar(500) null comment '总中标金额',
    first_time_notice_date            varchar(100) null comment '首次公告日期',
    modify_date                       varchar(100) null comment '更正日期',
    consultation_document_get_time    varchar(100) null comment '获取磋商文件时间',
    consultation_document_get_address varchar(500) null comment '获取磋商文件地点',
    response_file_delivery_time       varchar(100) null comment '响应文件递交时间',
    response_file_delivery_address    varchar(500) null comment '响应文件递交地点',
    response_file_opening_time        varchar(100) null comment '响应文件开启时间',
    response_file_opening_address     varchar(500) null comment '响应文件开启地点',
    person_names                      varchar(500) null comment '谈判小组、询价小组成员、磋商小组成员名单及单一来源采购人员名单',
    total_transaction_amount          varchar(100) null comment '总成交金额',
    title                             varchar(500) null,
    signing_up_time                   varchar(100) null comment '报名时间',
    signing_up_address                varchar(500) null comment '报名地点',
    deal_time                         varchar(100) null comment '成交日期',
    constraint announcement_summary_info_url_uindex
        unique (info_url)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
-- auto-generated definition
create table gov_accessory_info
(
    id            int auto_increment
        primary key,
    owner         varchar(200)         null comment '公告的名字',
    download_url  varchar(255)         null comment '下载链接',
    file_name     varchar(200)         null comment '文件名',
    main_url      varchar(250)         null comment '下载链接所属的页面地址',
    download_done tinyint(1) default 0 null
)
    ENGINE=InnoDB DEFAULT CHARSET=utf8 comment '政府采购网附件信息';
-- auto-generated definition
create table gov_main_info_url_list
(
    id        int auto_increment
        primary key,
    url       varchar(256)         not null comment '采购信息',
    done      tinyint(1) default 0 null comment '是否采集完成',
    type_name varchar(10)          null,
    constraint gov_main_info_url_list_company_url_uindex
        unique (url)
)
   ENGINE=InnoDB DEFAULT CHARSET=utf8  comment '中国政府采购网';
-- auto-generated definition
create table inds_chain
(
    id       int auto_increment comment '编号'
        primary key,
    name     varchar(128) null comment '名称',
    createdt datetime     null comment '创建时间',
    creater  int          null comment '创建人'
)
ENGINE=InnoDB DEFAULT CHARSET=utf8 ;


-- auto-generated definition
create table inds_chain_company
(
    id            int auto_increment comment '编号'
        primary key,
    module_id     int          null comment '父模块编号',
    inds_chain_id int          null comment '产业链编号',
    name          varchar(128) null comment '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
-- auto-generated definition
create table inds_chain_cpy
(
    id            int auto_increment comment '编号'
        primary key,
    inds_chain_id int          null comment '产业链编号',
    module_id     int          null comment '名称',
    cyp_name      varchar(128) null comment '企业名称简称',
    cpy_fullname  varchar(128) null comment '企业名称简称',
    cpy_id        int          null comment '企业库编号'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
-- auto-generated definition
create table inds_chain_module
(
    id            int auto_increment comment '编号'
        primary key,
    parentid      int          null comment '父模块编号',
    inds_chain_id int          null comment '产业链编号',
    name          varchar(128) null comment '名称'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
-- auto-generated definition
create table inds_pro
(
    id            int auto_increment comment '编号'
        primary key,
    inds_chain_id int          null,
    name          varchar(128) null comment '名称',
    createdt      datetime     null comment '创建时间',
    creater       int          null comment '创建人'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;
-- auto-generated definition
create table industry_category
(
    id             int auto_increment comment '编号'
        primary key,
    parent_id      int default 0 null comment '父亲项目编号',
    name           varchar(128)  null comment '名称',
    stock_type     varchar(16)   null comment '上市类型',
    org_code       varchar(32)   null,
    ext_info       varchar(64)   null comment '扩展信息',
    org_data       text          null comment '原始数据',
    level          int default 0 null,
    category_url   varchar(256)  null,
    company_counts int           null comment '某一类别对应的公司数量'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 
    comment '行业类别' charset = utf8;

-- auto-generated definition
create table industry_category_whole_companies_info
(
    id          int auto_increment
        primary key,
    command_url     varchar(200) null,
    category_id int          null comment '在 industry_category 表中的 id',
    org_code    varchar(128) null,
    stock_type  varchar(3)   null comment '股票类型',
    stock_code  varchar(20)  null comment '股票代码'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;


-- auto-generated definition
create table industry_company_profile_detail
(
    id                                int auto_increment comment '编号'
        primary key,
    name_cn                           varchar(128)  null comment '中文名字',
    name_en                           varchar(128)  null comment '英文名字',
    name_old                          varchar(500)  null comment '曾用名',
    area                              varchar(256)  null comment '所属地域',
    category_description              varchar(128)  null comment '行业类别描述',
    command_url                           varchar(500)  null comment '公司网址',
    stock_name                        varchar(128)  null comment '股票名字',
    main_business                     varchar(1500) null comment '主营业务',
    product_name                      varchar(500)  null comment '产品名称',
    controller_stock                  varchar(500)  null comment '控股股东',
    stock_code                        varchar(20)   null comment '股票代码',
    controller_actual                 varchar(500)  null comment '实际控股人',
    controller_ultimate               varchar(128)  null comment '最终控股人',
    president                         varchar(1000) null comment '董事长',
    president_secretary               varchar(500)  null comment '董事长秘书',
    representative_legal              varchar(500)  null comment '法人代表',
    general_manager                   varchar(500)  null comment '总经理',
    registered_capital                varchar(128)  null comment '注册资金',
    employees_number                  varchar(50)   null comment '员工人数',
    telephone                         varchar(500)  null comment '电　　话',
    fax                               varchar(500)  null comment '传真',
    postcode                          varchar(500)  null comment '邮编',
    company_address                   varchar(500)  null comment '办公地址',
    company_profile                   mediumtext    null comment '公司简介',
    president_chairman                varchar(500)  null comment '董事会主席',
    representative_securities_affairs varchar(500)  null comment '证券事务代表',
    balance_sheet_date                varchar(128)  null comment '年结日',
    registered_address                varchar(500)  null comment '注册地址',
    corporate_headquarters            varchar(500)  null comment '公司总部',
    auditor                           varchar(500)  null comment '核数师',
    legal_adviser                     varchar(500)  null comment '法律顾问',
    e_mail                            varchar(500)  null comment '电邮',
    collection_url                    varchar(255)  null comment '数据采集地址',
    datetime                          varchar(10)   null comment '上市时间'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 ;

-- auto-generated definition
create table industry_company_profile_simple
(
    id             int auto_increment
        primary key,
    company_url    varchar(256)         not null comment '公司简介的链接',
    done           tinyint(1) default 0 null comment '公司简介信息是否被爬取',
    stock_code     varchar(10)          null,
    stock_name     varchar(30)          null,
    company_name   varchar(500)         null,
    company_type   varchar(200)         null,
    main_business varchar(500)         null,
    datetime       varchar(10)          null
)
   ENGINE=InnoDB DEFAULT CHARSET=utf8  comment '爬完公司简介信息,相应的done置为true';
```