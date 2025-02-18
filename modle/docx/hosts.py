#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ------------------------------------------------------------
# File: hosts.py
# Created Date: 2020/6/24
# Created Time: 0:14
# Author: Hypdncy
# Author Mail: hypdncy@outlook.com
# Copyright (c) 2020 Hypdncy
# ------------------------------------------------------------
#                       .::::.
#                     .::::::::.
#                    :::::::::::
#                 ..:::::::::::'
#              '::::::::::::'
#                .::::::::::
#           '::::::::::::::..
#                ..::::::::::::.
#              ``::::::::::::::::
#               ::::``:::::::::'        .:::.
#              ::::'   ':::::'       .::::::::.
#            .::::'      ::::     .:::::::'::::.
#           .:::'       :::::  .:::::::::' ':::::.
#          .::'        :::::.:::::::::'      ':::::.
#         .::'         ::::::::::::::'         ``::::.
#     ...:::           ::::::::::::'              ``::.
#    ````':.          ':::::::::'                  ::::..
#                       '.:::::'                    ':'````..
# ------------------------------------------------------------
import logging

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from modle.common.loophole.loopholes import Loopholes
from modle.docx.base import DocxBase
from cnf.const import template_loops_file
from cnf.data import cnf_data, host_loop_ports, system_host_names


class DocxHosts(DocxBase):

    def __init__(self, LOOPHOLES: Loopholes):
        super(DocxHosts, self).__init__(LOOPHOLES)
        self.doc = Document(template_loops_file)

    def save(self):
        filename = "./{0}主机扫描报告-{1}-主机排序.docx".format(cnf_data["user"]["name"], cnf_data["date"]["end"])
        logging.info("---保存主机排序文档：{filename}".format(filename=filename))
        self.doc.save(filename)
        return filename

    def draw_loophole_info(self, plugin_id, host, ports):
        """
        画漏洞信息
        :return:
        """
        info = self.LOOPHOLES[plugin_id]
        paragraph0 = self.doc.add_paragraph(
            "【{risk_cn}】{name_cn}".format(risk_cn=info["risk_cn"], name_cn=info["name_cn"]))
        paragraph0.style = "安恒信息--标题 3"
        paragraph1_1 = self.doc.add_paragraph("漏洞描述：")
        paragraph1_1.style = "安恒信息--列表（符号一级）"
        paragraph1_2 = self.doc.add_paragraph(
            "{describe_cn}".format(describe_cn=info["describe_cn"].replace("\\u", "_")))
        paragraph1_2.style = "安恒信息--列表（无符号一级）"

        paragraph2_1 = self.doc.add_paragraph("受影响主机：")
        paragraph2_1.style = "安恒信息--列表（符号一级）"

        table = self.doc.add_table(rows=len(ports) + 1, cols=2, style="安恒信息表格缩进")

        def write_table_rows(row_idx, row_datas):
            row = table.row_cells(row_idx)
            row[0].paragraphs[0].text, row[1].paragraphs[0].text = row_datas
            row[0].paragraphs[0].alignment = row[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        write_table_rows(0, ("主机", "端口"))
        for idx, port in enumerate(ports):
            idx = idx + 1
            write_table_rows(idx, (host, port))

        paragraph3_1 = self.doc.add_paragraph("加固建议：")
        paragraph3_1.style = "安恒信息--列表（符号一级）"
        paragraph3_2 = self.doc.add_paragraph("{solution}".format(solution=info["solution_cn"].replace("\\u", "_")))
        paragraph3_2.style = "安恒信息--列表（无符号一级）"

    def draw_host_loop_ports(self):
        """
        画漏洞
        :return:
        """
        for host, loop_ports in host_loop_ports.items():
            paragraph0 = self.doc.add_paragraph(
                "【{risk_cn}】{name}（{host}）".format(name=system_host_names.get(host, ''), host=host,
                                                   risk_cn=self.LOOPHOLES[next(iter(loop_ports))]["risk_cn"]))
            paragraph0.style = "安恒信息--标题 2"

            for plugin_id, ports in loop_ports.items():
                self.draw_loophole_info(plugin_id, host, ports)

    def run(self):
        super(DocxHosts, self).run()

        self.draw_host_loop_ports()
        self.update_doc_toc()
