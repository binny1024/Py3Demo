import prettytable as pt


def test():
    table_titles = [
        '采购类型',
        '此采购信息的地址',
        '采购项目名称',
        '品目',
        '采购单位',
        '行政区域',
        '公告时间',
        '获取招标的时间',
        '招标文件售价',
        '获取招标文件的地点',
        '开标时间',
        '开标地点',
        '预算金额',
        '项目联系人',
        '项目联系电话',
        '采购单位地址',
        '采购单位联系方式',
        '代理机构名称',
        '代理机构地址',
        '代理机构联系方式',
        '公告正文',
        '获取谈判文件的地点',
        '获取谈判文件的时间',
        '附件地址',
        '提交文件截止时间',
        '资格审查日期',
        '本项目招标公告日期',
        '中标日期	',
        '评审专家名单',
        '总中标金额',
        '首次公告日期',
        '更正日期',
        '获取磋商文件时间',
        '获取磋商文件地点',
        '响应文件递交时间',
        '响应文件递交地点',
        '响应文件开启时间',
        '响应文件开启地点',
        '谈判小组、询价小组成员、磋商小组成员名单及单一来源采购人员名单',
        '总成交金额'
    ]
    table_row_1 = [
        'procurement_type',
        'info_url',
        'project_name',
        'items',
        'procurement_unit',
        'administrative_region',
        'notice_time',
        'tender_get_time',
        'tender_documents_selling_price',
        'tender_documents_address',
        'bidding_opening_time',
        'bidding_opening_address          ',
        'budget_amount',
        'project_contacts',
        'project_phone',
        'procurement_unit_address',
        'procurement_unit_phone',
        'agency_name',
        'agency_place',
        'agency_phone',
        'main_body',
        'negotiation_doc_get_address',
        'negotiation_doc_get_date',
        'attachment_address',
        'submission_deadline',
        'qualification_date',
        'project_tender_notice_date',
        'bidding_get_date',
        'professor_name_list',
        'bidding_get_total_amount',
        'first_time_notice_date',
        'modify_date',
        'consultation_document_get_time',
        'consultation_document_get_address',
        'response_file_delivery_time',
        'response_file_delivery_address',
        'response_file_opening_time',
        'response_file_opening_address',
        'person_names',
        'total_transaction_amount'
    ]
    pretty_table = pt.PrettyTable()
    pretty_table.field_names = table_titles
    pretty_table.add_row(table_row_1)
    for table_title in table_titles:
        pretty_table.align[table_title] = 'c'
    pretty_table.border = True
    # pretty_table.junction_char = '$'
    # pretty_table.horizontal_char = '+'
    # pretty_table.vertical_char = '%'
    print(pretty_table)


def test2():
    import prettytable as pt

    tb = pt.PrettyTable()
    tb.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
    tb.add_row(["Adelaide", 1295, 1158259, 600.5])
    tb.add_row(["Brisbane", 5905, 1857594, 1146.4])
    tb.add_row(["Darwin", 112, 120900, 1714.7])
    tb.add_row(["Hobart", 1357, 2099999995556, 619.5])

    tb.align["City name"] = "l"
    tb.align["Area"] = "c"
    tb.align["Population"] = "r"
    tb.align["Annual Rainfall"] = "c"

    print(tb)


if __name__ == '__main__':
    test()
    # test2()
