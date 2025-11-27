from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import math
import time
import random

def main():
    i2c = I2C(id=0 ,scl=Pin(9), sda=Pin(8), freq=400000)
    LED = Pin(25, Pin.OUT, value=0)

    B1 = Pin(13, Pin.IN, Pin.PULL_UP)
    B2 = Pin(14, Pin.IN, Pin.PULL_UP)
    B3 = Pin(15, Pin.IN, Pin.PULL_UP)
    B1P=0
    B2P=0
    B3P=0
    oled_buff = SSD1306_I2C(width=80, height=64, i2c=i2c, addr=60)
    accual_pic = SSD1306_I2C(width=128, height=64, i2c=i2c, addr=60)
    
    mess = ADC(Pin(28))
    #DEBL=[0]
    FLIST=[funktion_1,funktion_2,funktion_3,funktion_4]
    nav="<B1< >B2> B3=ok"
    text=[ #["","","","","",nav]
        ["Mandelbrot zoom","koordinaten:","(-1.7499 0i)","","1/4",nav],
        ["(x * y) / n ","Heller Pixel ","bedeutet kein","Rest ","2/4",nav],
        ["Archimedische","Spirale","(dreht sich)","","3/4",nav],
        ["Fehler bei der","Messung feat.","Umgeb. Signale +","dich als Antenne","4/4",nav]
        ]
    Function = FLIST[ask_Function(B1,B1P,B2,B2P,B3,B3P,FLIST,text,accual_pic)]
    
    FLIST2=[[False,1], [True,1],[False,8], [False,32]]
    text2=[
        ['"Debug" modus',"zeigt den pixel","an der gerade","berechnet wird","AUS 1/4",nav],
        ["","","","","AN  2/4",nav],
        ["ungenauere","statusleiste","wird seltener","aktualisiert","AUS 3/4 but fast",nav],
        ["","","extrem","schnell","AUS 4/4",nav],
        ]
    DEB_select = FLIST2[ask_Function(B1,B1P,B2,B2P,B3,B3P,FLIST2,text2,accual_pic)]
    #DEB = ask_debug(B1,B1P,B2,B2P,accual_pic)
    DEB, prog_bar_speed=DEB_select
    Fast_DEB=1  #Zahl erhöhen für schnellere anzeige im Debug modus
    TIME=0
    transfer=[]
    while True:
        for n in range(64):
            t1=time.ticks_us()
            n=n+1
            for y in range(64):
                if y%prog_bar_speed==0: show_stats(accual_pic,(n-1),TIME,y,transfer)
                for x in range(80):
                    
                    
                    if not DEB:LED.toggle()
                    if DEB:oled_buff.pixel(x,y,1)
                    if DEB&(x%Fast_DEB==0)&(y%Fast_DEB==0):
                        accual_pic.blit(oled_buff, 0, 0)
                        accual_pic.show()
                    
                    a, transfer = Function(x,y,n,transfer,mess)
                    
                    if a==1:
                        oled_buff.pixel(x,y,1)
                        #print(x+1,y+1)		#debug
                    else:
                        oled_buff.pixel(x,y,0)
                    
                    
                    
            t2=time.ticks_us()
            TIME=round(time.ticks_diff(t2, t1)/1000000, 3)
            accual_pic.blit(oled_buff, 0, 0)
            accual_pic.show()
            
            #print(max(DEBL),len(DEBL))		#debug

def ask_Function(b1,b1p,b2,b2p,b3,b3p,FList,text,oled):
    leng=len(FList)-1
    sel=0
    while True:
        if b2.value()==b2p:
            sel=sel+1
            if leng<sel: sel=0
            while b2.value()==b2p:
                time.sleep_ms(10)
        if b1.value()==b1p:
            sel=sel-1
            if sel<0: sel=leng
            while b1.value()==b1p:
                time.sleep_ms(10)
        if b3.value()==b3p:
            break
        #print(sel)	#debug
        oled.fill(0)
        textunpack=text[sel]
        text0=textunpack[0]
        text1=textunpack[1]
        text2=textunpack[2]
        text3=textunpack[3]
        text4=textunpack[4]
        text5=textunpack[5]
        oled.text(str(text0),0,0)
        oled.text(str(text1),0,8)
        oled.text(str(text2),0,16)
        oled.text(str(text3),0,24)
        oled.text(str(text4),0,32)
        oled.text(str(text5),0,40)
        oled.show()
        
        time.sleep_ms(10)
        
    while b1.value()==b1p or b2.value()==b2p or b3.value()==b3p: pass
    oled.fill(0)
    return sel
    
def show_stats(oled,n,t,prog=0,itop=0):
    if type(itop) is list: itop=0
    a="n= "+str(n)
    ITOP="i="+str(itop)
    b=str(t)
    x=81
    oled.fill_rect(x, 0, 48, oled.height, 0)
    oled.text(a, x, 0)
    oled.fill_rect(x, 8, int((prog/64)*47), 8, 1)
    if not(itop==0): oled.text(ITOP, x,24)
    oled.text("Zeit", x, 32)
    oled.text("fuer", x, 40)
    oled.text("Bild:", x, 48)
    oled.text(b, x, 56)
    oled.show()

def funktion_1(x,y,n,itop,mess):
    if type(itop) is int: pass
    else: itop=10
    if n==1:
        xc=(x-(58))/(16*2**n)
        yc=(y-(32))/(16*2**n)
    else:
        xc=(x-(16))/(16*2**n)-1.7499 #0.25 #-0.109149328
        yc=(y-(32))/(16*2**n)+0.00 #0.01 -0.896379138
    i=0
    c=complex(xc,yc)
    z=complex(0,0)
    imax=itop+20
    while True:
        i=i+1
        z=(z*z)+c
        if abs(z)>4:
            a=0
            if itop<i:
                itop=i
                #print(itop)	#debug
            break
        if imax<i:
            a=1
            #print(i)		#debug
            break
    return a, itop

def funktion_2(x,y,n,trans,mess):
    return (x*y)%(n)==0, 0


def funktion_3(x,y,n,trans,mess):
    
    xc=(x-(40))/(8)
    yc=(y-(32))/(8)
    
    fun=math.tan((math.sqrt(xc*xc+yc*yc)-n*0.5))*xc
        
    
    return math.isclose(fun,yc,abs_tol=0.3), 0

def funktion_4(x,y,n,trans,mess):
    trans.append(mess.read_u16())
    trans.append(mess.read_u16())
    #print(trans)	#debug
    mean=sum(trans)/len(trans)
    trans.append(mess.read_u16())
    if trans[-1]<mean:a=0
    if trans[-1]==mean:a=0
    if mean<trans[-1]:a=1
    
    if 200<len(trans):
        del trans[0]
        del trans[0]
        del trans[0]
        del trans[0]
    return a, trans

if __name__=="__main__":
    main()
