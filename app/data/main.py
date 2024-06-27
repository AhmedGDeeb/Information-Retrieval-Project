import textract
text = textract.process("1.docx")
print(text, file=open("output.txt", "w"))