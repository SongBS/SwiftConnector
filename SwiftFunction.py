#-*-coding:cp949-*-

'''
Created on 2013. 6. 24.
@author: sbs@gabia.com
'''

import wx
import os
import pycurl
import cStringIO
import DialogClass
import json



def progress(download_t, download_d, upload_t, upload_d):
    print "Total to download", download_t
    print "Total downloaded", download_d
    print "Total to upload", upload_t
    print "Total uploaded", upload_d 



def SwiftAuth(self):
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Storage-User: %s:%s\r\nX-Storage-Pass: %s\r\nX-Auth-New-Token: %s\r\nX-Auth-Token-Lifetime: %s\r\n\r\n" \
                %(self.swift_account, self.swift_user, self.swift_passwd, self.swift_tokenNew, self.swift_tokenTTL)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swift_url)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 200):
            wx.MessageBox('User Authentication Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">User Authentication Failed\r\n")
            #self.textControl.AppendText(requestHeader) 
            #self.textControl.AppendText(headerBuf.getvalue())          
            #self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")               
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))
        else:  
            for x in headerBuf.getvalue().splitlines():
                sLine = x.split(":", 1)
                if "X-Auth-Token" in sLine :
                    self.authToken = sLine[1].strip()  
                if "X-Storage-Url" in sLine :            
                    self.storageUrl = sLine[1].strip()
                if "X-Auth-Token-Expires" in sLine:
                    tokenTTL = sLine[1].strip()
            
            self.textControl.AppendText(">User Authentication Success\r\n")
            self.textControl.AppendText("X-Auth-Token: %s \r\n" %self.authToken)
            self.textControl.AppendText("X-Storage-Path: %s \r\n" %self.storageUrl)                        
            self.textControl.AppendText("Token Expire: %s \r\n" %tokenTTL)
            #self.textControl.AppendText(requestHeader) 
            #self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            #self.textControl.AppendText(headerBuf.getvalue())          
            #self.textControl.AppendText(bodyBuf.getvalue())    
            #self.textControl.AppendText("\r\n\r\n")               
            #self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))

        #self.textControl.Clear()             
        #self.textControl.SetValue(requestHeader)
        #self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
        #self.textControl.AppendText(headerBuf.getvalue())          
        #self.textControl.AppendText(bodyBuf.getvalue())        
        #self.textControl.SetInsertionPoint(1)
        headerBuf.close()
        bodyBuf.close()
        c.close()         
        return            



def ListContainer(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"?format=json")
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 200):
            if (rtn == 404):
                self.textControl.AppendText("<EMPTY>\r\n")
            else:
                wx.MessageBox('Show Container List Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)        
                self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
                self.textControl.AppendText(">Show Container List Failed\r\n")
                self.textControl.AppendText(headerBuf.getvalue())          
                self.textControl.AppendText(bodyBuf.getvalue())    
                self.textControl.AppendText("\r\n\r\n")           
                self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))   
        else:
            self.textControl.AppendText(">Show Container List Success\r\n")
            self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")
            self.textControl.AppendText("[Name]\t\t[Files]\t\t[Bytes]\r\n")    
            self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")       
            decoded = json.loads(bodyBuf.getvalue())    
            for i in decoded:
                self.textControl.AppendText("%s\t\t%s\t\t%s\t\t\r\n" %(i['name'], i['count'], i['bytes']))                        
            self.textControl.AppendText("\r\n")                 

        headerBuf.close()
        bodyBuf.close()
        c.close() 





def SelectContainer(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return

        textDialog = wx.TextEntryDialog(self, 'Enter a Container Name to Use', 'Notices', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            self.selectedContainer = textDialog.GetValue().strip()
            self.selectedContainer = self.selectedContainer.encode('utf-8')
            self.textControl.AppendText(">Container Change Success\r\n")
            self.textControl.AppendText("Container Selected: %s\r\n\r\n" %self.selectedContainer)
        textDialog.Destroy()  




def CreateContainer(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
        
        containerUrl = ""
        textDialog = wx.TextEntryDialog(self, 'Enter a Container Name to Create', 'Create Container', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            containerUrl = textDialog.GetValue().strip()
            containerUrl = containerUrl.encode('utf-8')
        textDialog.Destroy()
        
        if containerUrl == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Token: %s\r\n\r\n" %(self.authToken)

        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+containerUrl)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 201 or rtn == 202) :
            wx.MessageBox('Container Create Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION) 
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Container Create Failed\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Create Container Success\r\n")   
            self.textControl.AppendText("Created Container :%s\r\n\r\n" %containerUrl)   
                     
        headerBuf.close()
        bodyBuf.close()
        c.close() 
        return
    
       






def DeleteContainer(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
        
        containerUrl = ""
        textDialog = wx.TextEntryDialog(self, 'Enter a Container Name to Delete', 'Delete Container', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            containerUrl = textDialog.GetValue().strip()
            containerUrl = containerUrl.encode('utf-8')
        textDialog.Destroy()

        if containerUrl == "":
            self.EmptyInput()
            return
                
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n" %(self.authToken)

        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+containerUrl)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "DELETE")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 204) :
            wx.MessageBox('Container Delete Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Container Delete Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Container Delete Success\r\n")   
            self.textControl.AppendText("Deleted Container :%s\r\n\r\n" %containerUrl)   
         
        headerBuf.close()
        bodyBuf.close()
        c.close() 
        return







def ListObject(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 
 
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"?format=json") #?limit=2&marker=objectname
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        
        
        if not(rtn == 200 or rtn == 204) :
            if (rtn == 404):
                self.textControl.AppendText("<EMPTY>\r\n")
            else:
                wx.MessageBox('Show Object List Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
                self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
                self.textControl.AppendText(">Show Object List Failed\r\n")
                self.textControl.AppendText(headerBuf.getvalue())          
                self.textControl.AppendText(bodyBuf.getvalue())    
                self.textControl.AppendText("\r\n\r\n")             
                self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))              
        else:
            self.textControl.AppendText(">Show Object List Success\r\n")
            self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")
            self.textControl.AppendText("[Name]\t\t[Bytes]\t\t[Last_Modified]\r\n")    
            self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")       
            decoded = json.loads(bodyBuf.getvalue()) 
            totalObject = 0   
            for i in decoded:
                totalObject = totalObject + 1
                self.textControl.AppendText("%s\t\t%s\t\t%s\r\n" %(i['name'], i['bytes'], i['last_modified']))
            self.textControl.AppendText("\r\n")  
            self.textControl.AppendText("Tatal Object : %d\r\n" %totalObject)  
            marker = "&marker=%s" %(i['name'])
                   
        headerBuf.close()
        bodyBuf.close()
        c.close()  

        if totalObject == 10000:                 
            headerBuf = cStringIO.StringIO()
            bodyBuf = cStringIO.StringIO()
            requestHeader = "X-AUth-Token: %s\r\n\r\n\r\n" %(self.authToken)
            c = pycurl.Curl()
            c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"?format=json"+marker.encode('utf-8')) #?limit=2&marker=objectname
            c.setopt(pycurl.SSL_VERIFYPEER, False)
            c.setopt(pycurl.VERBOSE, False)
            c.setopt(pycurl.TCP_NODELAY, True)
            c.setopt(pycurl.HTTPHEADER, [requestHeader])
            c.setopt(pycurl.CUSTOMREQUEST, "GET")   
            c.setopt(c.HEADERFUNCTION, headerBuf.write)         
            c.setopt(c.WRITEFUNCTION, bodyBuf.write)
            c.perform()
            rtn = c.getinfo(c.HTTP_CODE)
            
            
            if not(rtn == 200 or rtn == 204) :
                if (rtn == 404):
                    self.textControl.AppendText("<EMPTY>\r\n")
                else:
                    wx.MessageBox('Show Object List Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
                    self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
                    self.textControl.AppendText(">Show Object List Failed\r\n")
                    self.textControl.AppendText(headerBuf.getvalue())          
                    self.textControl.AppendText(bodyBuf.getvalue())    
                    self.textControl.AppendText("\r\n\r\n")             
                    self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))              
            else:
                self.textControl.AppendText(">Show Object List Success\r\n")
                self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")
                self.textControl.AppendText("[Name]\t\t[Bytes]\t\t[Last_Modified]\r\n")    
                self.textControl.AppendText("--------------------------------------------------------------------------------------\r\n")       
                decoded = json.loads(bodyBuf.getvalue())   
                for i in decoded:
                    totalObject = totalObject + 1
                    self.textControl.AppendText("%s\t\t%s\t\t%s\r\n" %(i['name'], i['bytes'], i['last_modified']))
                self.textControl.AppendText("\r\n")  
                self.textControl.AppendText("Tatal Object : %d\r\n" %totalObject)  

                       
            headerBuf.close()
            bodyBuf.close()
            c.close()                 
        
                



def ObjectMeta(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 
        
        objectUrl = ""
        textDialog = wx.TextEntryDialog(self, 'Enter a Object Name to Show', 'Show Object Metadata', '', wx.OK|wx.CANCEL|wx.CENTRE)
        if textDialog.ShowModal() == wx.ID_OK:
            objectUrl = textDialog.GetValue().strip()
            objectUrl = objectUrl.encode('utf-8')
        textDialog.Destroy()
        
        if objectUrl == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"/"+objectUrl+"?format=json")
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 200 or rtn == 204) :
            wx.MessageBox('Show Object Metadata Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)  
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Show Object Metadata Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Show Object metadata Success\r\n")
            self.textControl.AppendText(headerBuf.getvalue())  
            self.textControl.AppendText("\r\n\r\n")
            
        headerBuf.close()
        bodyBuf.close()
        c.close() 
        return 
     
        




def UploadObject(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 
        
        dialog=wx.FileDialog(self, " Enter a Object Name to Upload", self.dirname, "", "*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename=dialog.GetFilename()
            self.dirname=dialog.GetDirectory()
            
            try:
                statinfo = os.stat(self.dirname+"/"+self.filename)
                f=open(self.dirname+"/"+self.filename, "rb")
            except os.error:
                wx.MessageBox('File Open failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
                return
        dialog.Destroy()     
        
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        #requestHeader = "X-AUth-Token: %s\r\nX-Delete-After: 86500\r\nContent-Length: %d\r\n" %(self.authToken, statinfo.st_size)
        requestHeader = "X-AUth-Token: %s\r\nX-Delete-After: 86500" %(self.authToken)
        #requestHeader = "X-AUth-Token: %s" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"/"+self.filename.encode('utf-8'))
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.NOPROGRESS, False)
        c.setopt(pycurl.PUT, True)        
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")   
        c.setopt(pycurl.INFILE, f)           
        c.setopt(pycurl.INFILESIZE, statinfo.st_size)    
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.setopt(c.PROGRESSFUNCTION, progress)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        upspeed = c.getinfo(c.SPEED_UPLOAD)
        totalTime = c.getinfo(c.TOTAL_TIME)
        f.close
        
        
        if not(rtn == 201 or rtn == 202) :
            wx.MessageBox('Object Upload Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION) 
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Object Upload Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Object Upload Successs\r\n")
            self.textControl.AppendText("Upload Speed: %s\t\tTotalTime: %s\r\n\r\n" %(upspeed, totalTime))
                          
        headerBuf.close()
        bodyBuf.close()
        c.close()  
        return
    
       
                 


def DownloadObject(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 

        downFileName = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Object Name to Download ', 'Object Download', '', wx.OK|wx.CANCEL|wx.CENTRE)
        if textDialog.ShowModal() == wx.ID_OK:
            downFileName = textDialog.GetValue().strip()
            downFileName = downFileName.encode('utf-8')
        textDialog.Destroy()
        
        if downFileName == "":
            self.EmptyInput()
            return
         
        dialog=wx.FileDialog(self, " Enter a Object Name to Save", self.dirname, downFileName, "*.*", wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename=dialog.GetFilename()
            self.dirname=dialog.GetDirectory()
            
            try:
                f=open(self.dirname+"/"+self.filename, "wb+")
            except os.error:
                wx.MessageBox('File Open failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
                return
        dialog.Destroy()
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"/"+downFileName)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, True)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.NOPROGRESS, False)
        #c.setopt(pycurl.BINARY_TRANSFER, False)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(pycurl.WRITEDATA, f) 
        c.setopt(c.WRITEFUNCTION, f.write)      
        c.setopt(c.HEADERFUNCTION, headerBuf.write)        
        c.setopt(c.PROGRESSFUNCTION, progress)                
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        downspeed = c.getinfo(c.SPEED_DOWNLOAD)
        totalTime = c.getinfo(c.TOTAL_TIME)
        f.close()

        if not(rtn == 200 or rtn == 204) :
            wx.MessageBox('Object Download Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)    
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Object Download Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Object Download Success\r\n")
            self.textControl.AppendText("Download Speed: %s\t\tTotalTime: %s\r\n\r\n" %(downspeed, totalTime))             

        headerBuf.close()
        bodyBuf.close()
        c.close() 
        return
                
    
                 




def CopyObject(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 


        dialog = DialogClass.dialogCopyObject(self, -1, 'Copy Object')
        dialog.ShowModal()
        dialog.Destroy()
        
        if dialog.sourceFile == "" or dialog.destFile == "" :
            self.EmptyInput()
            return

 
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\nX-Copy-From: %s/%s\r\nContent-Length: 0\r\n\r\n" %(self.authToken, self.selectedContainer, dialog.sourceFile)
                    
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"/"+dialog.destFile)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 200 or rtn == 201) :
            wx.MessageBox('File Copy Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)  
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Object Copy Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Object Copy Success\r\n")
            self.textControl.AppendText("File Copied: %s -> %s\r\n\r\n" %(dialog.sourceFile, dialog.destFile))                  

        headerBuf.close()
        bodyBuf.close()
        c.close()
        return
    
       
                 




def DeleteObject(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 
        
        objectUrl = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Object Name to Delete', 'Object Delete', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            objectUrl = textDialog.GetValue().strip()
            objectUrl = objectUrl.encode('utf-8')
        textDialog.Destroy()
        
        if objectUrl == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+self.selectedContainer+"/"+objectUrl)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "DELETE")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        if not(rtn == 204) :
            wx.MessageBox('Object Delete Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)  
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Object Delete Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Object Delete Success\r\n")
            self.textControl.AppendText("File Deleted: %s\r\n\r\n" %objectUrl) 
            
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return
    
      
                 


def DeleteContainerAll(self):
        if self.authToken == "":
            wx.MessageBox('Authentication has not been completed.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return
 
        if self.selectedContainer == "":
            wx.MessageBox('Container has not been selected.' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)            
            return 
        
        containerUrl = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Container Name to Delete\r\n All Object in Container will be Delete', 'Container Delete', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            containerUrl = textDialog.GetValue().strip()
            containerUrl = containerUrl.encode('utf-8')
        textDialog.Destroy()
        
        if containerUrl == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-AUth-Token: %s\r\n\r\n" %(self.authToken)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.storageUrl+"/"+containerUrl+"?format=json")
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)

        if not(rtn == 200 or rtn == 204) :
            wx.MessageBox('Container Delete Failed' ,'Notice' ,wx.OK|wx.ICON_INFORMATION)
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Container Delete Failed : %d \r\n" %rtn)
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))              
        else:     
            decoded = json.loads(bodyBuf.getvalue())    
            for i in decoded:
                object = i['name']
                object = object.encode('utf-8')
                print self.storageUrl+"/"+containerUrl+"/"+object
                c.setopt(pycurl.URL, self.storageUrl+"/"+containerUrl+"/"+object)
                c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
                c.perform()
                rtn = c.getinfo(c.HTTP_CODE)
                if not(rtn == 204) :
                    self.textControl.AppendText("File Delete Failed: %s  return[%d]\r\n" %(object, rtn))
                else:
                    self.textControl.AppendText("File Deleted: %s  return[%d] \r\n" %(object, rtn))
            
            c.setopt(pycurl.URL, self.storageUrl+"/"+containerUrl)
            c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
            c.perform()                        
            rtn = c.getinfo(c.HTTP_CODE)
            if not(rtn == 204 ) :
                self.textControl.AppendText("Container Delete Failed: %s [%s]\r\n%s\r\n" %(containerUrl, rtn, bodyBuf.getvalue()))
            else:
                self.textControl.AppendText("Container Deleted: %s [%s]\r\n" %(containerUrl, rtn))            
            
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return




