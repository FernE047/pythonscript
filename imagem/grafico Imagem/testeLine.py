from PIL import Image, ImageDraw

lineImage=Image.new('RGB',(100,100),(255,255,255,255))
draw = ImageDraw.Draw(lineImage)
draw.line((50,25,80,0), fill=0,width=1)
#(firstX,firstY,secondX,secondY)
lineImage.save("teste.png")
