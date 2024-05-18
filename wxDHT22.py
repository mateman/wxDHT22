#!/usr/bin/python3 

"""
Ventana para mostrar DHT22 en Raspberry Pi

"""

import wx, sys, time, adafruit_dht, board

# Configuracion del puerto GPIO al cual esta conectado  (GPIO 23)
pin = board.D23
# Configuracion del tipo de sensor DHT
sensor = adafruit_dht.DHT22(pin)

def obtenerSensor(s):
    humedad = s.humidity
    temperatura = s.temperature
    return (temperatura, humedad)

class Ventana(wx.Frame):

    def __init__(self, *args, **kw):
        super(Ventana, self).__init__(*args, **kw)
        icon = wx.Icon('~/wxDHT22/dht22.ico',wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        self.InitUI()


    def InitUI(self):
 
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        self.timer = wx.Timer(self)
        
        
        wx.StaticText(self, label='Temperatura:', pos=(10, 10))
        wx.StaticText(self, label='max:', pos=(12, 30))
        wx.StaticText(self, label='min:', pos=(120, 30))
        
        self.stt = wx.StaticText(self, label='', pos=(110, 10))
        self.sttmx = wx.StaticText(self, label='', pos=(60, 30))
        self.sttmn = wx.StaticText(self, label='', pos=(170, 30))

        wx.StaticText(self, label='Humedad:', pos=(10, 60))
        wx.StaticText(self, label='max:', pos=(12, 80))
        wx.StaticText(self, label='min:', pos=(120, 80))
        
        self.sth = wx.StaticText(self, label='', pos=(110, 60))
        self.sthmx = wx.StaticText(self, label='', pos=(60, 80))
        self.sthmn = wx.StaticText(self, label='', pos=(170, 80))
        
        temperatura,humedad = obtenerSensor(sensor)
        
        self.stt.SetLabel(str(temperatura) +' C')
        self.sttmx.SetLabel(str(temperatura))
        self.sttmn.SetLabel(str(temperatura))

        self.sth.SetLabel(str(humedad) + ' %')
        self.sthmx.SetLabel(str(humedad))
        self.sthmn.SetLabel(str(humedad))
        
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        
        self.timer.Start(2000) # 2 segundos de intervalo

        self.SetSize((350, 250))
        self.SetTitle('wx-DHT22')
        self.Centre()

    def update(self, event):

           temperatura,humedad = obtenerSensor(sensor)

           self.stt.SetLabel(str(temperatura) +' C')
           self.sth.SetLabel(str(humedad) + ' %')
           if not(temperatura is None) and(temperatura > float(self.sttmx.GetLabel()))  :
                           self.sttmx.SetLabel(str(temperatura))
           if  not(temperatura is None) and (temperatura < float(self.sttmn.GetLabel())) :
                           self.sttmn.SetLabel(str(temperatura))  
           if not(humedad is None) and (humedad > float(self.sthmx.GetLabel()))  :
                           self.sthmx.SetLabel(str(humedad))
           if  not(humedad is None) and (humedad < float(self.sthmn.GetLabel())) :
                           self.sthmn.SetLabel(str(humedad))  

    def OnQuit(self, e):
           self.Close()


def main():

    app = wx.App()
    win = Ventana(None)
    win.Show()
    app.MainLoop()


if __name__ == '__main__':
    main() 

