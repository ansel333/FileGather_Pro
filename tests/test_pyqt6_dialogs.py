#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests: PyQt6 Dialog Enums (components.dialogs)
Tests for QDialog and QDialogButtonBox enum handling in PyQt6
"""

import sys
import os
import pytest

# Set QT_QPA_PLATFORM to offscreen to avoid GUI issues
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QDialogButtonBox
from PyQt6.QtCore import Qt


@pytest.fixture(scope="session", autouse=True)
def setup_qt_app():
    """Setup QApplication for all tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield
    # Keep the app alive


class TestQDialogEnums:
    """Test PyQt6 QDialog enum handling"""
    
    def test_qdialog_accepted_enum(self):
        """Test QDialog.DialogCode.Accepted enum"""
        # PyQt6 uses QDialog.DialogCode.Accepted
        assert hasattr(QDialog, 'DialogCode')
        assert hasattr(QDialog.DialogCode, 'Accepted')
        
        dialog = QDialog()
        dialog.accept()
        
        # Verify DialogCode.Accepted value is correct
        assert QDialog.DialogCode.Accepted.value == 1
    
    def test_qdialog_rejected_enum(self):
        """Test QDialog.DialogCode.Rejected enum"""
        assert hasattr(QDialog, 'DialogCode')
        assert hasattr(QDialog.DialogCode, 'Rejected')
        
        dialog = QDialog()
        dialog.reject()
        
        # Verify DialogCode.Rejected value is correct
        assert QDialog.DialogCode.Rejected.value == 0
    
    def test_qdialogebuttonbox_standard_buttons(self):
        """Test QDialogButtonBox StandardButton enum"""
        # PyQt6 uses QDialogButtonBox.StandardButton for button constants
        assert hasattr(QDialogButtonBox, 'StandardButton')
        
        # Test individual buttons
        assert hasattr(QDialogButtonBox.StandardButton, 'Ok')
        assert hasattr(QDialogButtonBox.StandardButton, 'Cancel')
        assert hasattr(QDialogButtonBox.StandardButton, 'Save')
        assert hasattr(QDialogButtonBox.StandardButton, 'Discard')
        assert hasattr(QDialogButtonBox.StandardButton, 'Open')
        
        # Verify button values are not None
        assert QDialogButtonBox.StandardButton.Ok is not None
        assert QDialogButtonBox.StandardButton.Cancel is not None
    
    def test_qdialogebuttonbox_combined_buttons(self):
        """Test combining multiple QDialogButtonBox StandardButtons"""
        # Test bitwise OR operation for combining buttons
        combined = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        
        assert combined is not None
        # The combined value should be a valid StandardButton
        assert hasattr(combined, 'value')
    
    def test_qmessagebox_standard_buttons(self):
        """Test QMessageBox StandardButton enum"""
        # PyQt6 uses QMessageBox.StandardButton for button constants
        assert hasattr(QMessageBox, 'StandardButton')
        
        # Test common buttons
        assert hasattr(QMessageBox.StandardButton, 'Ok')
        assert hasattr(QMessageBox.StandardButton, 'Cancel')
        assert hasattr(QMessageBox.StandardButton, 'Yes')
        assert hasattr(QMessageBox.StandardButton, 'No')
    
    def test_qmessagebox_icon_enum(self):
        """Test QMessageBox Icon enum"""
        assert hasattr(QMessageBox, 'Icon')
        assert hasattr(QMessageBox.Icon, 'Information')
        assert hasattr(QMessageBox.Icon, 'Warning')
        assert hasattr(QMessageBox.Icon, 'Critical')
        assert hasattr(QMessageBox.Icon, 'Question')


class TestDialogReturnValueHandling:
    """Test proper handling of dialog return values"""
    
    def test_dialog_accepted_value(self):
        """Test that dialog accepted returns correct enum value"""
        dialog = QDialog()
        dialog.accept()
        
        # The value of Accepted should be 1
        assert QDialog.DialogCode.Accepted.value == 1
    
    def test_dialog_rejected_value(self):
        """Test that dialog rejected returns correct enum value"""
        dialog = QDialog()
        dialog.reject()
        
        # The value of Rejected should be 0
        assert QDialog.DialogCode.Rejected.value == 0
    
    def test_dialog_comparison_with_enum(self):
        """Test comparing dialog result with enum value"""
        dialog = QDialog()
        
        # Simulate checking if dialog was accepted
        # In actual code: if dialog.exec() == QDialog.DialogCode.Accepted:
        dialog.accept()
        result = dialog.result()
        
        # Compare with enum
        assert result == QDialog.DialogCode.Accepted.value


class TestButtonBoxEnumCombinations:
    """Test QDialogButtonBox enum combinations"""
    
    def test_ok_cancel_combination(self):
        """Test Ok | Cancel button combination"""
        button_box = QDialogButtonBox()
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        button_box.setStandardButtons(buttons)
        
        # Verify buttons were added
        assert button_box.button(QDialogButtonBox.StandardButton.Ok) is not None
        assert button_box.button(QDialogButtonBox.StandardButton.Cancel) is not None
    
    def test_yes_no_combination(self):
        """Test Yes | No button combination"""
        button_box = QDialogButtonBox()
        buttons = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        button_box.setStandardButtons(buttons)
        
        # Verify buttons were added
        assert button_box.button(QDialogButtonBox.StandardButton.Yes) is not None
        assert button_box.button(QDialogButtonBox.StandardButton.No) is not None
    
    def test_save_discard_cancel_combination(self):
        """Test Save | Discard | Cancel button combination"""
        button_box = QDialogButtonBox()
        buttons = (
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Discard |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.setStandardButtons(buttons)
        
        # Verify all buttons were added
        assert button_box.button(QDialogButtonBox.StandardButton.Save) is not None
        assert button_box.button(QDialogButtonBox.StandardButton.Discard) is not None
        assert button_box.button(QDialogButtonBox.StandardButton.Cancel) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
