import os

print(os.getcwd())
os.chdir('/Users/linuxing3/workspace/')
print(os.getcwd())

file = os.open('youtube.zip', 1)
print(file)
