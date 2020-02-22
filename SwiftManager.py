#-*-coding:cp949-*-

'''
Created on 2013. 6. 24.
@author: sbs@gabia.com
'''

import wx
import os
import SwiftFunction
import SwauthFunction
import DialogClass
import threading


#down side button
ID_BUTTON=100

#function
ID_EXIT=200

#windows
ID_SPLITTER=300




#menu
ID_SETTING=400
ID_ABOUT=401
ID_SWIFT_AUTH = 500
ID_SWIFT_CONTAINER_LIST = 501
ID_SWIFT_CONTAINER_SELECT = 502
ID_SWIFT_CREATE_CONTAINER = 503
ID_SWIFT_DELETE_CONTAINER = 504
ID_SWIFT_OBEJCT_LIST = 505
ID_SWIFT_OJBECT_METADATA = 506
ID_SWIFT_OBJECT_UPLOAD = 507
ID_SWIFT_OBJECT_DOWNLOAD = 508
ID_SWIFT_OBJECT_COPY = 509
ID_SWIFT_OBJECT_DELETE = 510

ID_SWAUTH_ACCOUNT_LIST = 600
ID_SWAUTH_ACCOUNT_DETAIL = 601
ID_SWAUTH_ADD_ACCOUNT = 602
ID_SWAUTH_DEL_ACCOUNT = 603
ID_SWAUTH_ADD_USER = 604
ID_SWAUTH_DEL_USER = 605
ID_SWAUTH_DEL_USER_ALL = 606

#Toolbar
ID_TOOLBAR_CONNECT = 700
ID_TOOLBAR_FOLDER = 701
ID_TOOLBAR_UPLOAD = 702
ID_TOOLBAR_DOWNLOAD = 703
ID_TOOLBAR_DELETE_FILE = 704
TD_TOOLBAR_DELETE_FOLDER = 705
ID_TOOLBAR_CONFIG = 706
ID_TOOLBAR_HELP = 707
ID_TOOLBAR_EXIT = 708

#side button
ID_SIDE_BUTTON = 800


class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(590,700), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE|wx.SYSTEM_MENU)

        self.dirname = "."      
        
        #----------------------------------------------------------------
        #config values
        self.authToken = ""                
        self.storageUrl = ""      
             
        #swift config values                   
        self.swift_url = ""
        self.swift_account = ""
        self.swift_user = ""
        self.swift_passwd = ""
        self.swift_tokenTTL = ""
        self.swift_tokenNew = ""
        self.selectedContainer = ""
        
        #swauth config values
        self.swauth_url = ""
        self.swauth_admin = ""
        self.swauth_adminpass = ""
        #----------------------------------------------------------------
        
        
        
        #set frame
        self.panel=wx.Panel(self,-1)
        self.textControl = wx.TextCtrl(self.panel, pos=(10, 35), size=(550, 500), style=wx.TE_MULTILINE|wx.TE_RICH)
        
        wx.StaticText(self.panel, label="Operation Display:", pos=(10, 15), size=wx.DefaultSize, style=0)

        
        # file 
        filemenu= wx.Menu()  
        filemenu.Append(ID_SETTING,"&Settings","")                 
        filemenu.Append(ID_EXIT,"&Exit","")
        
        swauthmenu= wx.Menu()  
        swauthmenu.Append(ID_SWAUTH_ACCOUNT_LIST,"&Show Account List","")     
        swauthmenu.Append(ID_SWAUTH_ACCOUNT_DETAIL,"&Show User List","")    
        swauthmenu.AppendSeparator()     
        swauthmenu.Append(ID_SWAUTH_ADD_ACCOUNT,"&Create Account","") 
        swauthmenu.Append(ID_SWAUTH_DEL_ACCOUNT,"&Delete Account","")      
        swauthmenu.AppendSeparator()      
        swauthmenu.Append(ID_SWAUTH_ADD_USER,"&Create User","") 
        swauthmenu.Append(ID_SWAUTH_DEL_USER,"&Delete User","")  
        swauthmenu.Append(ID_SWAUTH_DEL_USER_ALL,"&Delete User All","")      
        
        swiftmenu= wx.Menu()  
        swiftmenu.Append(ID_SWIFT_AUTH,"&Authentication","")  
        swiftmenu.AppendSeparator()                   
        swiftmenu.Append(ID_SWIFT_CONTAINER_LIST,"&Show Container List","") 
        swiftmenu.Append(ID_SWIFT_CONTAINER_SELECT,"&Select Container","")                      
        swiftmenu.Append(ID_SWIFT_CREATE_CONTAINER,"&Create Container","")              
        swiftmenu.Append(ID_SWIFT_DELETE_CONTAINER,"&Delete Container","")
        swiftmenu.AppendSeparator()   
        swiftmenu.Append(ID_SWIFT_OBEJCT_LIST,"&Show Object List","")                 
        swiftmenu.Append(ID_SWIFT_OJBECT_METADATA,"&Show Object Metadata","")     
        swiftmenu.Append(ID_SWIFT_OBJECT_UPLOAD,"&Upload Object ","")               
        swiftmenu.Append(ID_SWIFT_OBJECT_DOWNLOAD,"&Download Object","")     
        swiftmenu.Append(ID_SWIFT_OBJECT_COPY,"&Copy Object","")             
        swiftmenu.Append(ID_SWIFT_OBJECT_DELETE,"&Delete Object","") 

        # help 
        helpmenu = wx.Menu()
        helpmenu.Append(ID_ABOUT,"&About Program","")   
              
     
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Program")
        menuBar.Append(swauthmenu,"&Account")
        menuBar.Append(swiftmenu,"&Storage")                
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnModifyConfig, id=ID_SETTING)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        self.Bind(wx.EVT_MENU, self.AccountList, id=ID_SWAUTH_ACCOUNT_LIST)
        self.Bind(wx.EVT_MENU, self.AccountUserList, id=ID_SWAUTH_ACCOUNT_DETAIL) 
        self.Bind(wx.EVT_MENU, self.CreateAccount, id=ID_SWAUTH_ADD_ACCOUNT) 
        self.Bind(wx.EVT_MENU, self.DeleteAccount, id=ID_SWAUTH_DEL_ACCOUNT)
        self.Bind(wx.EVT_MENU, self.CreateUser, id=ID_SWAUTH_ADD_USER)
        self.Bind(wx.EVT_MENU, self.DeleteUser, id=ID_SWAUTH_DEL_USER) 
        self.Bind(wx.EVT_MENU, self.DeleteUserAll, id=ID_SWAUTH_DEL_USER_ALL) 
        
        self.Bind(wx.EVT_MENU, self.SwiftAuth, id=ID_SWIFT_AUTH)       
        self.Bind(wx.EVT_MENU, self.ListContainer, id=ID_SWIFT_CONTAINER_LIST)
        self.Bind(wx.EVT_MENU, self.SelectContainer, id=ID_SWIFT_CONTAINER_SELECT)
        self.Bind(wx.EVT_MENU, self.CreateContainer, id=ID_SWIFT_CREATE_CONTAINER)
        self.Bind(wx.EVT_MENU, self.DeleteContainer, id=ID_SWIFT_DELETE_CONTAINER)
        self.Bind(wx.EVT_MENU, self.ListObject, id=ID_SWIFT_OBEJCT_LIST)
        self.Bind(wx.EVT_MENU, self.ObjectMeta, id=ID_SWIFT_OJBECT_METADATA)
        self.Bind(wx.EVT_MENU, self.UploadObject, id=ID_SWIFT_OBJECT_UPLOAD)
        self.Bind(wx.EVT_MENU, self.DownloadObject, id=ID_SWIFT_OBJECT_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.CopyObject, id=ID_SWIFT_OBJECT_COPY)
        self.Bind(wx.EVT_MENU, self.DeleteObject, id=ID_SWIFT_OBJECT_DELETE)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_ABOUT)


        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        tb.SetBackgroundColour('white') 
        tb.AddSimpleTool(ID_TOOLBAR_CONNECT, wx.Bitmap('images/connect.png', wx.BITMAP_TYPE_PNG), 'Connect Container')  
        tb.AddSimpleTool(ID_TOOLBAR_FOLDER, wx.Bitmap('images/folder.png', wx.BITMAP_TYPE_PNG), 'Show Container List')    
        tb.AddSeparator()      
        tb.AddSimpleTool(ID_TOOLBAR_UPLOAD, wx.Bitmap('images/upload.png', wx.BITMAP_TYPE_PNG), 'Upload Object')
        tb.AddSimpleTool(ID_TOOLBAR_DOWNLOAD, wx.Bitmap('images/download.png', wx.BITMAP_TYPE_PNG), 'Download Object') 
        tb.AddSimpleTool(ID_TOOLBAR_DELETE_FILE, wx.Bitmap('images/delete.png', wx.BITMAP_TYPE_PNG), 'Delete Object') 
        tb.AddSimpleTool(TD_TOOLBAR_DELETE_FOLDER, wx.Bitmap('images/deletefolder.png', wx.BITMAP_TYPE_PNG), 'Delete Container')                  
        tb.AddSeparator()                    
        tb.AddSimpleTool(ID_TOOLBAR_CONFIG, wx.Bitmap('images/setting.png', wx.BITMAP_TYPE_PNG), 'Settings')
        tb.AddSimpleTool(ID_TOOLBAR_HELP, wx.Bitmap('images/help.png', wx.BITMAP_TYPE_PNG), 'Help')
        tb.AddSimpleTool(ID_TOOLBAR_EXIT, wx.Bitmap('images/exit.png', wx.BITMAP_TYPE_PNG), 'Exit Prgram')
        tb.Realize()
       
        self.Bind(wx.EVT_TOOL, self.TBarConnect, id=ID_TOOLBAR_CONNECT)
        self.Bind(wx.EVT_TOOL, self.ListContainer, id=ID_TOOLBAR_FOLDER)
        self.Bind(wx.EVT_TOOL, self.UploadObject, id=ID_TOOLBAR_UPLOAD)
        self.Bind(wx.EVT_TOOL, self.DownloadObject, id=ID_TOOLBAR_DOWNLOAD)
        self.Bind(wx.EVT_TOOL, self.DeleteObject, id=ID_TOOLBAR_DELETE_FILE)
        self.Bind(wx.EVT_TOOL, self.DeleteContainerAll, id=TD_TOOLBAR_DELETE_FOLDER)
        self.Bind(wx.EVT_TOOL, self.OnModifyConfig, id=ID_TOOLBAR_CONFIG)
        self.Bind(wx.EVT_TOOL, self.OnAbout, id=ID_TOOLBAR_HELP)
        self.Bind(wx.EVT_TOOL, self.OnExit, id=ID_TOOLBAR_EXIT)
                                                      
        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText(os.getcwd())
        self.Center()
        self.Show(True)


        try:
            configFile = open("./config.ini", "r")
        except:
            wx.MessageBox(' Load Configuration Failure' ,'Notice' ,wx.OK|wx.ICON_INFORMATION)
            configdig = DialogClass.dialogNewConfigure(self, -1, 'Settings')
            configdig.ShowModal()
            configdig.Destroy()
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
                
                self.textControl.SetValue("> Load Configuration.\r\n")
                self.textControl.AppendText("------------------------------------------------------------------------------------------\r\n")
                self.textControl.AppendText("swift_url              : %s\r\n" %self.swift_url)
                self.textControl.AppendText("swift_account      : %s\r\n" %self.swift_account)
                self.textControl.AppendText("swift_user            : %s\r\n" %self.swift_user)
                self.textControl.AppendText("swift_passwd        : %s\r\n" %self.swift_passwd)
                self.textControl.AppendText("selectedContainer  : %s\r\n" %self.selectedContainer)
                self.textControl.AppendText("swift_tokenTTL     : %s\r\n" %self.swift_tokenTTL)
                self.textControl.AppendText("swift_tokenNew    : %s\r\n" %self.swift_tokenNew)
                self.textControl.AppendText("swauth_url            : %s\r\n" %self.swauth_url)
                self.textControl.AppendText("swauth_admin       : %s\r\n" %self.swauth_admin)
                self.textControl.AppendText("swauth_adminpass  : %s\r\n" %self.swauth_adminpass)
                self.textControl.AppendText("-------------------------------------------------------------------------------------------\r\n\r\n")
        
                
            
    #event function
    def OnAbout(self, event):
        description = "   This program is.....                                            \r\n\r\n"
        licence = """        Do not allow ....        """
        info = wx.AboutDialogInfo()
        info.SetName('Swift Manager')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) Gabia inc.')
        info.SetWebSite('http://www.gabia.com')
        info.SetLicence(licence)
        info.AddDeveloper('  Gabia inc. (sbs@gabia.com)')
        wx.AboutBox(info)


    def TBarConnect(self, event):
        SwiftFunction.SwiftAuth(self)
        SwiftFunction.ListObject(self)

    def OnExit(self, event):
        self.Close(True)

    def OnModifyConfig(self, event):
        dialog = DialogClass.dialogModifyConfigure(self, -1, 'Settings')    
        dialog.ShowModal()
        dialog.Destroy()
        self.swift_url = dialog.swift_url
        self.swift_account = dialog.swift_account
        self.swift_user = dialog.swift_user
        self.swift_passwd = dialog.swift_passwd
        self.swift_tokenTTL = dialog.swift_tokenTTL
        self.swift_tokenNew = dialog.swift_tokenNew
        self.selectedContainer = dialog.selectedContainer
        self.swauth_url = dialog.swauth_url
        self.swauth_admin = dialog.swauth_admin
        self.swauth_adminpass = dialog.swauth_adminpass
        
    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        self.sb.SetStatusText(os.getcwd())
        event.Skip()

    def OnDoubleClick(self, event):
        size =  self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)



    #swauth functon
    def AccountList(self, event):
        SwauthFunction.AccountList(self)

    def AccountUserList(self, event):
        SwauthFunction.AccountUserList(self)

    def CreateAccount(self, event):
        SwauthFunction.CreateAccount(self)

    def DeleteAccount(self, event):
        SwauthFunction.DeleteAccount(self)

    def CreateUser(self, event):
        SwauthFunction.CreateUser(self)

    def DeleteUser(self, event):
        SwauthFunction.DeleteUser(self)
        
    def DeleteUserAll(self, event):
        SwauthFunction.DeleteUserAll(self)       
    
    # swift function
    def SwiftAuth(self, event):
        SwiftFunction.SwiftAuth(self)

    def ListContainer(self, event):
        SwiftFunction.ListContainer(self)

    def SelectContainer(self, event):
        SwiftFunction.SelectContainer(self)      

    def CreateContainer(self, event):
        SwiftFunction.CreateContainer(self)

    def DeleteContainer(self, event):
        SwiftFunction.DeleteContainer(self)
        
    def ListObject(self, event):
        SwiftFunction.ListObject(self)

    def ObjectMeta(self, event):
        SwiftFunction.ObjectMeta(self)

    def UploadObject(self, event):
        th=threading.Thread(SwiftFunction.UploadObject(self))
        th.start();

    def DownloadObject(self, event):
        th=threading.Thread(SwiftFunction.DownloadObject(self))
        th.start();
        
    def CopyObject(self, event):
        th=threading.Thread(SwiftFunction.CopyObject(self))
        th.start();
        
    def DeleteObject(self, event):
        th=threading.Thread(SwiftFunction.DeleteObject(self))
        th.start();
        
    def DeleteContainerAll(self, event):
        th=threading.Thread(SwiftFunction.DeleteContainerAll(self))
        th.start();   
            
    def EmptyInput(self):
        wx.MessageBox('Required fields was not entered.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)     



#main 
app = wx.App(0)
MainWindow(None, -1, 'Swift Manager v1.0 beta')
app.MainLoop()










