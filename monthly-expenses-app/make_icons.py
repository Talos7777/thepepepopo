from PIL import Image, ImageDraw

CREAM=(243,231,201); NAVY=(23,32,94); RED=(229,31,27); CYAN=(52,180,228); BLUE=(74,107,214)

def icon(size, maskable=False):
    S=1024
    img=Image.new("RGB",(S,S),NAVY)
    d=ImageDraw.Draw(img)
    # safe inset for content (bigger margin for maskable so nothing gets cropped by iOS mask)
    m=int(S*(0.16 if maskable else 0.085))
    # cream panel with navy frame
    d.rectangle([m,m,S-m,S-m],fill=CREAM)
    fr=int(S*0.028)
    d.rectangle([m,m,S-m,S-m],outline=NAVY,width=fr)
    inner_l=m+fr; inner_r=S-m-fr; inner_t=m+fr; inner_b=S-m-fr
    w=inner_r-inner_l
    # three Martini stripes down the right side
    sx=inner_r-int(w*0.30)
    bw=int(w*0.05); gap=int(w*0.028)
    for i,c in enumerate((CYAN,BLUE,RED)):
        x=sx+i*(bw+gap)
        d.rectangle([x,inner_t,x+bw,inner_b],fill=c)
    # big red roundel (the "coin")
    cx=inner_l+int(w*0.34); cy=(inner_t+inner_b)//2; r=int(w*0.26)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=RED)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=CREAM,width=int(S*0.02))
    # cream bar across the roundel (reads as a coin slot / minimal mark)
    bh=int(r*0.34)
    d.rectangle([cx-int(r*0.5),cy-bh//2,cx+int(r*0.5),cy+bh//2],fill=CREAM)
    # checkered strip along the bottom of the panel
    cs=int(w*0.055); ry=inner_b-cs*2
    n=(inner_r-inner_l)//cs
    for col in range(n):
        for row in range(2):
            if (col+row)%2==0:
                x0=inner_l+col*cs; y0=ry+row*cs
                d.rectangle([x0,y0,x0+cs,y0+cs],fill=NAVY)
    return img.resize((size,size),Image.LANCZOS)

icon(512).save("icon-512.png")
icon(192).save("icon-192.png")
icon(180).save("apple-touch-icon.png")
icon(512,maskable=True).save("icon-512-maskable.png")
print("icons written")
