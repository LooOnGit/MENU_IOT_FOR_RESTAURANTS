import qrcode
img = qrcode.make('https://www.youtube.com/watch?v=3ZH2IibOmgI')
print(type(img))  # qrcode.image.pil.PilImage
img.save("some_file.png")