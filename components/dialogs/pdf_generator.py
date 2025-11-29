"""
PDF日志生成器模块
生成包含搜索结果和操作记录的PDF文档
"""

import datetime
import traceback

from PyQt5.QtWidgets import QMessageBox, QInputDialog
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from ..utils import format_size, extract_filename_for_log


class PDFLogGenerator:
    """PDF日志生成器"""
    
    @staticmethod
    def generate_pdf_log(parent, file_path):
        """
        生成操作日志PDF文件
        
        Args:
            parent: 父窗口（包含操作日志等数据）
            file_path: PDF输出文件路径
            
        Returns:
            bool: 是否成功生成
        """
        # 让用户选择导出条数
        options = ["前20条", "前50条", "全部"]
        choice, ok = QInputDialog.getItem(
            parent, "导出操作记录", 
            "请选择导出操作过程的条数：", 
            options, 0, False
        )
        
        if not ok:
            return False
        
        # 根据选择获取操作日志
        if choice == "前20条":
            op_logs = parent.operation_log[:20]
        elif choice == "前50条":
            op_logs = parent.operation_log[:50]
        else:
            op_logs = parent.operation_log
            if len(parent.operation_log) > 100:
                QMessageBox.warning(
                    parent, "提示", 
                    "导出全部操作记录可能导致PDF文档过大，请耐心等待。"
                )

        try:
            doc = SimpleDocTemplate(str(file_path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # 配置样式
            title_style = styles['Title']
            title_style.fontName = 'SimSun'

            heading_style = styles['Heading2']
            heading_style.fontName = 'SimSun'

            normal_style = styles['Normal']
            normal_style.fontName = 'SimSun'

            # 添加标题
            PDFLogGenerator._add_title(story, title_style)
            story.append(Spacer(1, 12))

            # 添加基本信息表
            PDFLogGenerator._add_info_table(story, parent, heading_style)
            story.append(Spacer(1, 24))

            # 添加操作过程记录
            if op_logs:
                PDFLogGenerator._add_operation_logs(
                    story, op_logs, heading_style, normal_style
                )
                story.append(Spacer(1, 24))

            # 添加操作过的文件名
            if parent.operated_files:
                PDFLogGenerator._add_operated_files(
                    story, parent.operated_files, heading_style, normal_style
                )
                story.append(Spacer(1, 24))

            # 添加搜索结果文件列表
            if parent.search_results:
                PDFLogGenerator._add_search_results(
                    story, parent.search_results, heading_style, normal_style
                )

            doc.build(story)
            return True

        except Exception as e:
            QMessageBox.critical(
                parent, "错误", 
                f"生成PDF日志时出错: {str(e)}"
            )
            print(traceback.format_exc())
            return False

    @staticmethod
    def _add_title(story, style):
        """添加标题"""
        title = Paragraph("<b>文件归集管理器操作日志</b>", style)
        story.append(title)

    @staticmethod
    def _add_info_table(story, parent, heading_style):
        """添加基本信息表"""
        search_mode = parent.get_search_mode()
        search_mode_text = {
            "filename": "仅文件名",
            "content": "仅内容",
            "both": "两者同时"
        }.get(search_mode, "仅文件名")

        info_data = [
            ["操作日期", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["软件版本", f"文件归集管理器 V{parent.version}"],
            ["搜索文件夹", "\n".join(parent.search_folders)],
            ["目标文件夹", parent.target_folder or "未设置"],
            ["关键词", parent.keyword_entry.toPlainText() or "无"],
            ["搜索模式", search_mode_text],
            ["文件类型", parent.filetype_combo.currentText()],
            ["文件数量", str(len(parent.search_results))]
        ]
        
        info_table = Table(info_data, colWidths=[150, 350])
        info_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'SimSun', 10),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(info_table)

    @staticmethod
    def _add_operation_logs(story, op_logs, heading_style, normal_style):
        """添加操作过程记录"""
        op_title = Paragraph("<b>操作过程记录</b>", heading_style)
        story.append(op_title)
        story.append(Spacer(1, 12))
        
        op_data = [["序号", "时间与操作"]]
        for idx, log in enumerate(op_logs, 1):
            log_short = extract_filename_for_log(log)
            op_data.append([
                str(idx),
                Paragraph(log_short, normal_style)
            ])
        
        op_table = Table(op_data, colWidths=[40, 460])
        op_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'SimSun', 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONT', (0, 1), (-1, -1), 'SimSun', 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(op_table)

    @staticmethod
    def _add_operated_files(story, operated_files, heading_style, normal_style):
        """添加操作过的文件名"""
        file_title = Paragraph("<b>操作过的文件名</b>", heading_style)
        story.append(file_title)
        story.append(Spacer(1, 12))
        
        file_data = [["序号", "文件名"]]
        for idx, fname in enumerate(sorted(operated_files), 1):
            file_data.append([
                str(idx),
                Paragraph(fname, normal_style)
            ])
        
        file_table = Table(file_data, colWidths=[40, 460])
        file_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'SimSun', 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONT', (0, 1), (-1, -1), 'SimSun', 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(file_table)

    @staticmethod
    def _add_search_results(story, search_results, heading_style, normal_style):
        """添加搜索结果文件列表"""
        files_title = Paragraph("<b>文件列表</b>", heading_style)
        story.append(files_title)
        story.append(Spacer(1, 12))

        file_data = [["文件名", "大小", "修改日期"]]
        for file_info in search_results:
            file_data.append([
                Paragraph(file_info['name'], normal_style),
                format_size(file_info['size']),
                file_info['mod_date']
            ])

        file_table = Table(file_data, colWidths=[350, 100, 100])
        file_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, 0), 'SimSun', 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONT', (0, 1), (-1, -1), 'SimSun', 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(file_table)
