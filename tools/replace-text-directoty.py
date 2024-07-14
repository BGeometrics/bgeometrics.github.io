import os
import re

def replace_text_in_directory(directory, old_text, new_text, file_extension=None):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        if os.path.isfile(file_path) and (file_extension is None or filename.endswith(file_extension)):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            modified_content = re.sub(re.escape(old_text), new_text, content)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)
                
            print(f"Processed file: {file_path}")

# Usage
#old_text = """<link href="assets/vendor/boxicons/css/boxicons.min.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.snow.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/quill/quill.bubble.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/remixicon/remixicon.css" rel="stylesheet">"""
#old_text = """<link href="assets/vendor/simple-datatables/style.css" rel="stylesheet">"""
#old_text = """<script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-ZR3ZFTF2FK'); </script>"""

#old_text = """<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">"""
#new_text = """<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Nunito:300,300i,400,400i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" media="print" onload="this.onload=null;this.removeAttribute('media');" fetchpriority="high">"""


#old_text = """<script src="assets/vendor/apexcharts/apexcharts.min.js"></script>"""
#old_text = """<script src="assets/vendor/chart.js/chart.umd.js"></script>"""
#old_text = """<script src="assets/vendor/echarts/echarts.min.js"></script>"""
#old_text = """<script src="assets/vendor/quill/quill.min.js"></script>"""
#old_text = """<script src="assets/vendor/simple-datatables/simple-datatables.js"></script>"""
#old_text = """<script src="assets/vendor/tinymce/tinymce.min.js"></script>"""
#old_text = """<script src="assets/vendor/php-email-form/validate.js"></script>"""

file_extension = '.html'  
directory_path = '/home/pi/bgeometrics.github.io/tools'
old_text = """"""
new_text = """"""

replace_text_in_directory(directory_path, old_text, new_text, file_extension)

