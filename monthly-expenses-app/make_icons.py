from PIL import Image, ImageDraw

PAPER=(233,224,203); BLUE=(31,82,216); RED=(238,59,35); YELLOW=(255,206,31)
GREEN=(14,122,74); INK=(20,18,16)

def icon(size, maskable=False):
    S=1024
    img=Image.new("RGB",(S,S),BLUE)
    d=ImageDraw.Draw(img)
    pad=int(S*(0.18 if maskable else 0.0))
    fr=int(S*0.055)
    # rounded black-keyline frame with blue field
    d.rounded_rectangle([pad,pad,S-pad,S-pad],radius=int(S*0.14),fill=BLUE,outline=INK,width=fr)
    cx=int(S*0.47); cy=int(S*0.53); R=int((S-2*pad)*0.30)
    lw=int(S*0.022)
    # stacked yellow globe behind (offset down-right)
    off=int(R*0.24)
    d.ellipse([cx-R+off,cy-R+off,cx+R+off,cy+R+off],fill=YELLOW,outline=INK,width=lw)
    # red globe front
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=RED,outline=INK,width=lw)
    # grid: meridians (vertical ellipses) + latitudes (horizontal lines) clipped to the globe
    globe=Image.new("RGBA",(S,S),(0,0,0,0)); gd=ImageDraw.Draw(globe)
    for rx in (int(R*0.34), int(R*0.68)):
        gd.ellipse([cx-rx,cy-R,cx+rx,cy+R],outline=INK,width=lw)
    gd.line([cx,cy-R,cx,cy+R],fill=INK,width=lw)
    gd.line([cx-R,cy,cx+R,cy],fill=INK,width=lw)
    for fy in (0.5,):
        yy=int(R*fy); import math
        xx=int(R*math.cos(math.asin(fy)))
        gd.line([cx-xx,cy-yy,cx+xx,cy-yy],fill=INK,width=lw)
        gd.line([cx-xx,cy+yy,cx+xx,cy+yy],fill=INK,width=lw)
    mask=Image.new("L",(S,S),0); ImageDraw.Draw(mask).ellipse([cx-R,cy-R,cx+R,cy+R],fill=255)
    img.paste(globe,(0,0),Image.composite(globe,Image.new("RGBA",(S,S),(0,0,0,0)),mask).split()[3])
    # yellow sparkle top-right
    sx=int(S*0.74); sy=int(S*0.28); s=int(S*0.085)
    star=[(sx,sy-s),(sx+s*0.28,sy-s*0.28),(sx+s,sy),(sx+s*0.28,sy+s*0.28),
          (sx,sy+s),(sx-s*0.28,sy+s*0.28),(sx-s,sy),(sx-s*0.28,sy-s*0.28)]
    d.polygon(star,fill=YELLOW,outline=INK)
    d.line(star+[star[0]],fill=INK,width=int(S*0.012),joint="curve")
    return img.resize((size,size),Image.LANCZOS)

icon(512).save("icon-512.png")
icon(192).save("icon-192.png")
icon(180).save("apple-touch-icon.png")
icon(512,maskable=True).save("icon-512-maskable.png")
print("icons written")
