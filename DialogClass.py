#-*-coding:cp949-*-

'''
Created on 2013. 6. 24.
@author: sbs@gabia.com
'''

import wx




class dialogAddUser(wx.Dialog):
    accountName = ""
    userName = ""
    userPasswd = ""
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(330, 250))
        wx.StaticText(self, label="*Account Name", pos=(10, 15), size=wx.DefaultSize, style=0)
        self.textCtrlAccount = wx.TextCtrl(self, pos=(10, 30), size=(300, 20))
        wx.StaticText(self, label="*User Name", pos=(10, 60), size=wx.DefaultSize, style=0)
        self.textCtrlUser = wx.TextCtrl(self, pos=(10, 75), size=(300, 20))
        wx.StaticText(self, label="*User Password", pos=(10, 105), size=wx.DefaultSize, style=0)
        self.textCtrlPass = wx.TextCtrl(self, pos=(10, 120), size=(300, 20))
        wx.StaticLine(self, pos=(10, 155), size=(300,2))
        wx.Button(self, 100, "OK", pos=(120, 170), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.accountName = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.userName = self.textCtrlUser.GetValue().strip().encode('utf-8')
        self.userPasswd = self.textCtrlPass.GetValue().strip().encode('utf-8')
        self.Close()



class dialogDeleteUser(wx.Dialog):
    accountName = ""
    userName = ""
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(330, 200))
        wx.StaticText(self, label="*User Account", pos=(10, 15), size=wx.DefaultSize, style=0)
        self.textCtrlAccount = wx.TextCtrl(self, pos=(10, 30), size=(300, 20))
        wx.StaticText(self, label="*User Name", pos=(10, 60), size=wx.DefaultSize, style=0)
        self.textCtrlUser = wx.TextCtrl(self, pos=(10, 75), size=(300, 20))
        wx.StaticLine(self, pos=(10, 110), size=(300,2))
        wx.Button(self, 100, "OK", pos=(120, 125), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.accountName = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.userName = self.textCtrlUser.GetValue().strip().encode('utf-8')
        self.Close()



class dialogDeleteUserAll(wx.Dialog):
    accountName = ""
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(330, 200))
        wx.StaticText(self, label="*User Account", pos=(10, 15), size=wx.DefaultSize, style=0)
        self.textCtrlAccount = wx.TextCtrl(self, pos=(10, 30), size=(300, 20))

        wx.StaticLine(self, pos=(10, 110), size=(300,2))
        wx.Button(self, 100, "OK", pos=(120, 125), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.accountName = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.Close()



class dialogCopyObject(wx.Dialog):
    sourceFile = ""
    destFile = ""
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(330, 200))
        wx.StaticText(self, label="*Orignal Object Name", pos=(10, 15), size=wx.DefaultSize, style=0)
        self.textCtrlAccount = wx.TextCtrl(self, pos=(10, 30), size=(300, 20))
        wx.StaticText(self, label="*Target Object Name", pos=(10, 60), size=wx.DefaultSize, style=0)
        self.textCtrlUser = wx.TextCtrl(self, pos=(10, 75), size=(300, 20))
        wx.StaticLine(self, pos=(10, 110), size=(300,2))
        wx.Button(self, 100, "OK", pos=(120, 125), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.sourceFile = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.destFile = self.textCtrlUser.GetValue().strip().encode('utf-8')
        self.Close()




class dialogNewConfigure(wx.Dialog):
    #config values                
    swift_url = ""
    swift_account = ""
    swift_user = ""
    swift_passwd = ""
    swift_tokenTTL = ""
    swift_tokenNew = ""
    selectedContainer = ""
    swauth_url = ""
    swauth_admin = ""
    swauth_adminpass = ""


    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(690, 420))
        
        wx.StaticBox(self, label='SWIFT', pos=(15, 15), size=(320, 290))
        wx.StaticText(self, label="*Siwft Url", pos=(25, 45), size=wx.DefaultSize, style=0)
        self.textCtrlSwiftUrl = wx.TextCtrl(self, pos=(25, 60), size=(300, 20))
        
        wx.StaticText(self, label="*Account", pos=(25, 90), size=wx.DefaultSize, style=0)        
        self.textCtrlAccount = wx.TextCtrl(self, pos=(25, 105), size=(300, 20))
        
        wx.StaticText(self, label="*User", pos=(25, 135), size=wx.DefaultSize, style=0)  
        self.textCtrlUser = wx.TextCtrl(self, pos=(25, 150), size=(300, 20))
        
        wx.StaticText(self, label="*User Password", pos=(25, 180), size=wx.DefaultSize, style=0)  
        self.textCtrlPass = wx.TextCtrl(self, pos=(25, 195), size=(300, 20))      
         
        wx.StaticText(self, label="Default Container", pos=(25, 225), size=wx.DefaultSize, style=0)  
        self.textCtrlContainer = wx.TextCtrl(self, pos=(25, 240), size=(300, 20)) 
                 
        wx.StaticText(self, label="*Token Life Time", pos=(25, 270), size=wx.DefaultSize, style=0) 
        self.textCtrlTokenTTL = wx.TextCtrl(self, pos=(95, 270), size=(90, 20))
        self.textCtrlTokenTTL.SetValue("86400") 
                 
        self.checkNewToken = wx.CheckBox(self, label='New Token', pos=(210, 272))
        
        wx.StaticBox(self, label='SWAUTH', pos=(350, 15), size=(320, 290))
        wx.StaticText(self, label="*Swauth Url", pos=(360, 45), size=wx.DefaultSize, style=0)
        self.textCtrlSwauthUrl = wx.TextCtrl(self, pos=(360, 60), size=(300, 20))    
            
        wx.StaticText(self, label="*Admin", pos=(360, 90), size=wx.DefaultSize, style=0) 
        self.textCtrlAdmin = wx.TextCtrl(self, pos=(360, 105), size=(300, 20))
        
        wx.StaticText(self, label="*Admin Password", pos=(360, 135), size=wx.DefaultSize, style=0)  
        self.textCtrlAdminPass = wx.TextCtrl(self, pos=(360, 150), size=(300, 20))        

        wx.StaticLine(self, pos=(15, 320), size=(655,2))       
        wx.Button(self, 100, "OK", pos=(305, 335), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.swift_url = self.textCtrlSwiftUrl.GetValue().strip().encode('utf-8')
        self.swift_account = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.swift_user = self.textCtrlUser.GetValue().strip().encode('utf-8')
        self.swift_passwd = self.textCtrlPass.GetValue().strip().encode('utf-8')
        self.selectedContainer = self.textCtrlContainer.GetValue().strip().encode('utf-8')
        self.swift_tokenTTL = self.textCtrlTokenTTL.GetValue().strip().encode('utf-8')
        self.swift_tokenNew = self.checkNewToken.GetValue()
        self.swauth_url = self.textCtrlSwauthUrl.GetValue().strip().encode('utf-8')
        self.swauth_admin = self.textCtrlAdmin.GetValue().strip().encode('utf-8')
        self.swauth_adminpass = self.textCtrlAdminPass.GetValue().strip().encode('utf-8')        
        
        #check values
        if(self.swift_url=="" or self.swift_account=="" or self.swift_user=="" or self.swift_passwd==""):
            wx.MessageBox(' Required fields was not entered.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close()
            return 

        if(self.selectedContainer==""):
            wx.MessageBox(' Container is not selected.\r\nCan be selected  in the menu.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            
        if(self.swift_tokenTTL=="" or self.swift_tokenTTL=="0" or self.swift_tokenTTL<0):
            wx.MessageBox(' Token expiration time has been entered incorrectly.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close()
            return 

        if(self.swauth_url=="" or self.swauth_admin=="" or self.swauth_adminpass==""):
            wx.MessageBox(' Required fields was not entered.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close() 
            return
        

        #save config
        try:
            configFile = open("./config.ini", "w+")
        except:
            wx.MessageBox(' Failed to Create the Configuration file' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close() 
            return        
        else:
            configFile.write("swift_url=%s\r\n" %self.swift_url)
            configFile.write("swift_account=%s\r\n" %self.swift_account)
            configFile.write("swift_user=%s\r\n" %self.swift_user)
            configFile.write("swift_passwd=%s\r\n" %self.swift_passwd)
            configFile.write("selectedContainer=%s\r\n" %self.selectedContainer)
            configFile.write("swift_tokenTTL=%s\r\n" %self.swift_tokenTTL)
            configFile.write("swift_tokenNew=%s\r\n" %self.swift_tokenNew)
            configFile.write("swauth_url=%s\r\n" %self.swauth_url)
            configFile.write("swauth_admin=%s\r\n" %self.swauth_admin)
            configFile.write("swauth_adminpass=%s\r\n" %self.swauth_adminpass)
            configFile.close()
            self.Close()
            return
        


class dialogModifyConfigure(wx.Dialog):
    swift_url = ""
    swift_account = ""
    swift_user = ""
    swift_passwd = ""
    swift_tokenTTL = ""
    swift_tokenNew = ""
    selectedContainer = ""
    swauth_url = ""
    swauth_admin = ""
    swauth_adminpass = ""

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(690, 420))


        try:
            configFile = open("./config.ini", "r")
        except:
            wx.MessageBox(' Failed to Create the Configuration File.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            return
        else:
            config = configFile.read()
            config = config.encode('utf-8')
            for x in config.splitlines():
                sLine = x.split("=", 1)   
                if "swift_url" in sLine :
                    self.swift_url = sLine[1].strip() 
                if "swift_account" in sLine :            
                    self.swift_account = sLine[1].strip()
                if "swift_user" in sLine :            
                    self.swift_user = sLine[1].strip()                    
                if "swift_passwd" in sLine :            
                    self.swift_passwd = sLine[1].strip()                    
                if "selectedContainer" in sLine :            
                    self.selectedContainer = sLine[1].strip()
                if "swift_tokenTTL" in sLine :            
                    self.swift_tokenTTL = sLine[1].strip()                    
                if "swift_tokenNew" in sLine :            
                    self.swift_tokenNew = sLine[1].strip()                    
                if "swauth_url" in sLine :            
                    self.swauth_url = sLine[1].strip()                    
                if "swauth_admin" in sLine :            
                    self.swauth_admin = sLine[1].strip()                    
                if "swauth_adminpass" in sLine :            
                    self.swauth_adminpass = sLine[1].strip() 
                    
        
        wx.StaticBox(self, label='SWIFT', pos=(15, 15), size=(320, 290))
        wx.StaticText(self, label="*Siwft Url", pos=(25, 45), size=wx.DefaultSize, style=0)        
        self.textCtrlSwiftUrl = wx.TextCtrl(self, pos=(25, 60), size=(300, 20))
        self.textCtrlSwiftUrl.SetValue(self.swift_url)
                
        wx.StaticText(self, label="*Account", pos=(25, 90), size=wx.DefaultSize, style=0)        
        self.textCtrlAccount = wx.TextCtrl(self, pos=(25, 105), size=(300, 20))
        self.textCtrlAccount.SetValue(self.swift_account)
        
        wx.StaticText(self, label="*User", pos=(25, 135), size=wx.DefaultSize, style=0)  
        self.textCtrlUser = wx.TextCtrl(self, pos=(25, 150), size=(300, 20))
        self.textCtrlUser.SetValue(self.swift_user)
        
        wx.StaticText(self, label="*User Password", pos=(25, 180), size=wx.DefaultSize, style=0)  
        self.textCtrlPass = wx.TextCtrl(self, pos=(25, 195), size=(300, 20))       
        self.textCtrlPass.SetValue(self.swift_passwd)
        
        wx.StaticText(self, label="Default Container", pos=(25, 225), size=wx.DefaultSize, style=0)  
        self.textCtrlContainer = wx.TextCtrl(self, pos=(25, 240), size=(300, 20))    
        self.textCtrlContainer.SetValue(self.selectedContainer)
              
        wx.StaticText(self, label="*Token Life Time", pos=(25, 270), size=wx.DefaultSize, style=0) 
        self.textCtrlTokenTTL = wx.TextCtrl(self, pos=(95, 270), size=(90, 20))        
        self.textCtrlTokenTTL.SetValue(self.swift_tokenTTL)
                
        self.checkNewToken = wx.CheckBox(self, label='New Token', pos=(210, 272))
        if self.swift_tokenNew == "True":
            self.checkNewToken.SetValue(True)
        else:
            self.checkNewToken.SetValue(False)
        
        wx.StaticBox(self, label='SWAUTH', pos=(350, 15), size=(320, 290))
        
        wx.StaticText(self, label="*Swauth Url", pos=(360, 45), size=wx.DefaultSize, style=0)
        self.textCtrlSwauthUrl = wx.TextCtrl(self, pos=(360, 60), size=(300, 20))        
        self.textCtrlSwauthUrl.SetValue(self.swauth_url)
        
        wx.StaticText(self, label="*Admin", pos=(360, 90), size=wx.DefaultSize, style=0)        
        self.textCtrlAdmin = wx.TextCtrl(self, pos=(360, 105), size=(300, 20))
        self.textCtrlAdmin.SetValue(self.swauth_admin)
        
        wx.StaticText(self, label="*Admin Password", pos=(360, 135), size=wx.DefaultSize, style=0)  
        self.textCtrlAdminPass = wx.TextCtrl(self, pos=(360, 150), size=(300, 20))        
        self.textCtrlAdminPass.SetValue(self.swauth_adminpass)
        
        wx.StaticLine(self, pos=(15, 320), size=(655,2))       
        wx.Button(self, 100, "OK", pos=(305, 335), size=(80, 30), style=wx.CENTER) 
        self.Bind(wx.EVT_BUTTON, self.GetResult, id=100)   

    def GetResult(self, event):
        self.swift_url = self.textCtrlSwiftUrl.GetValue().strip().encode('utf-8')
        self.swift_account = self.textCtrlAccount.GetValue().strip().encode('utf-8')
        self.swift_user = self.textCtrlUser.GetValue().strip().encode('utf-8')
        self.swift_passwd = self.textCtrlPass.GetValue().strip().encode('utf-8')
        self.selectedContainer = self.textCtrlContainer.GetValue().strip().encode('utf-8')
        self.swift_tokenTTL = self.textCtrlTokenTTL.GetValue().strip().encode('utf-8')
        self.swift_tokenNew = self.checkNewToken.GetValue()
        self.swauth_url = self.textCtrlSwauthUrl.GetValue().strip().encode('utf-8')
        self.swauth_admin = self.textCtrlAdmin.GetValue().strip().encode('utf-8')
        self.swauth_adminpass = self.textCtrlAdminPass.GetValue().strip().encode('utf-8')        
        
        #check values
        if(self.swift_url=="" or self.swift_account=="" or self.swift_user=="" or self.swift_passwd==""):
            wx.MessageBox(' Required fields was not entered.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close()
            return 

        if(self.selectedContainer==""):
            wx.MessageBox(' Container is not selected.\r\nCan be selected  in the menu.' ,'�˸�' ,wx.OK|wx.ICON_INFORMATION)
            self.Close()
            return 
            
        if(self.swift_tokenTTL=="" or self.swift_tokenTTL=="0" or self.swift_tokenTTL<0):
            wx.MessageBox(' Token expiration time has been entered incorrectly.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close()
            return 

        if(self.swauth_url=="" or self.swauth_admin=="" or self.swauth_adminpass==""):
            wx.MessageBox(' Required fields was not entered.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close() 
            return
        

        #save config
        try:
            configFile = open("./config.ini", "w+")
        except:
            wx.MessageBox(' Failed to Create the Configuration File.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.Close() 
            return        
        else:
            configFile.write("swift_url=%s\r\n" %self.swift_url)
            configFile.write("swift_account=%s\r\n" %self.swift_account)
            configFile.write("swift_user=%s\r\n" %self.swift_user)
            configFile.write("swift_passwd=%s\r\n" %self.swift_passwd)
            configFile.write("selectedContainer=%s\r\n" %self.selectedContainer)
            configFile.write("swift_tokenTTL=%s\r\n" %self.swift_tokenTTL)
            configFile.write("swift_tokenNew=%s\r\n" %self.swift_tokenNew)
            configFile.write("swauth_url=%s\r\n" %self.swauth_url)
            configFile.write("swauth_admin=%s\r\n" %self.swauth_admin)
            configFile.write("swauth_adminpass=%s\r\n" %self.swauth_adminpass)
            configFile.close()
            self.Close()
            return
        




