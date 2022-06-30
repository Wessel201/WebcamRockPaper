with open('GUI_mooier_ui.py', 'r') as file:
    filedata = file.read()

# Replace the target string
filedata = filedata.replace('import logo_rc', '# import logo_rc')
filedata = filedata.replace('self.label_4.setText(_translate(\"MainWindow\", \"<html><head/><body><p><img src=\\":/logo/logo2.png\\"/></p></body></html>\"))',
                            'self.label_4.setText(_translate(\"MainWindow\", \"<html><head/><body><p><img src=\\"logo2.png\\"/></p></body></html>\"))')

# Write the file out again
with open('GUI_mooier_ui.py', 'w') as file:
    file.write(filedata)
