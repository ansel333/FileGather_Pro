"""
Search Manager - Handles search mode configuration and cancellation
"""


def get_search_mode(self):
    """获取当前搜索模式"""
    if self.filename_radio.isChecked():
        return "filename"
    elif self.content_radio.isChecked():
        return "content"
    elif self.both_radio.isChecked():
        return "both"
    return "filename"


def on_gather_mode_changed(self):
    """归集模式改变时的处理"""
    gather_mode = self.gather_mode_combo.currentData()
    
    if gather_mode == "folder":
        # 文件夹归集模式：隐藏子文件夹和文件类型选项
        self.subfolders_container.setVisible(False)
        self.filetype_combo.setVisible(False)
        self.filetype_label.setVisible(False)
    else:
        # 文件归集模式（默认）：显示所有选项
        self.subfolders_container.setVisible(True)
        self.filetype_combo.setVisible(True)
        self.filetype_label.setVisible(True)


def cancel_search_action(self):
    """取消搜索"""
    self.cancel_search = True
    self.status_label.setText("搜索已取消")
    self.cancel_button.setEnabled(False)
    self.search_button.setEnabled(True)
    self.exact_search_button.setEnabled(True)
    self.add_log("取消搜索")
