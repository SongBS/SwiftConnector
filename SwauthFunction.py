#-*-coding:cp949-*-

'''
Created on 2013. 6. 24.
@author: sbs@gabia.com
'''

import wx
import pycurl
import cStringIO
import DialogClass
import json




def AccountList(self):
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        
        if not(rtn == 200) :
            wx.MessageBox('Show Account List Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Show Account List Failed\r\n\r\n")
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))                    
        else:
            self.textControl.AppendText(">Show Account List Success\r\n") 
            self.textControl.AppendText("--------------------------------------\r\n")
            self.textControl.AppendText("[Account]\r\n")
            self.textControl.AppendText("--------------------------------------\r\n")           
            decoded = json.loads(bodyBuf.getvalue())    
            for i in decoded:
                for k in decoded[i]:
                    self.textControl.AppendText("%s\r\n" %k['name'])  
            self.textControl.AppendText("\r\n")     
            
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return
        
         


def AccountUserList(self):
        accountName = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Account Name to Show', 'Notices', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            accountName = textDialog.GetValue().strip()
            accountName = accountName.encode('utf-8')
            self.SetStatusText('You entered: %s\n' % textDialog.GetValue())
        textDialog.Destroy()
        
        if accountName == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+accountName)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        
        if not(rtn == 200) :
            wx.MessageBox('Show Account User List Failed' ,'Notices',wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Show Account User List Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")           
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))         
        else:
            self.textControl.AppendText(">Show Account User List Success\r\n") 
            self.textControl.AppendText("--------------------------------------\r\n")             
            self.textControl.AppendText("[User]\r\n")
            self.textControl.AppendText("--------------------------------------\r\n")
            totalNum = 0;
                           
            decoded = json.loads(bodyBuf.getvalue())    
            for i in decoded:
                if i=="users":
                    for k in decoded[i]:
                        totalNum = totalNum+1
                        self.textControl.AppendText("%s\r\n" %k['name'])  
            self.textControl.AppendText("\r\n") 
            self.textControl.AppendText("Total Users : %s\r\n" %(totalNum)) 

        headerBuf.close()
        bodyBuf.close()
        c.close()
        return





def CreateAccount(self):
        accountName = ""             
        textDialog = wx.TextEntryDialog(self, ' Enter a Account Name to Create', 'Notices', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            accountName = textDialog.GetValue().strip()
            accountName = accountName.encode('utf-8')
        textDialog.Destroy()
        
        if accountName == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+accountName)
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
            wx.MessageBox('Create Account Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Create Account Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Create Account Success\r\n")   
            self.textControl.AppendText("Created Account: %s\r\n\r\n" %accountName)   
                           
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return
        
        



def DeleteAccount(self):
        accountName = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Account Name to Delete', 'Notices', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            accountName = textDialog.GetValue().strip()
            accountName = accountName.encode('utf-8')
        textDialog.Destroy()
        
        if accountName == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+accountName)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "DELETE")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        if not(rtn == 200 or rtn == 204) :
            wx.MessageBox('Delete Account Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)   
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Delete Account Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))  
        else:
            self.textControl.AppendText(">Delete Account Success\r\n") 
            self.textControl.AppendText("Deleted Account: %s\r\n\r\n" %accountName)                   

        headerBuf.close()
        bodyBuf.close()
        c.close()
        return        
        



def CreateUser(self):
        dialog = DialogClass.dialogAddUser(self, -1, 'Create User')
        dialog.ShowModal()
        dialog.Destroy()
        
        if dialog.accountName == "" or dialog.userName == "" or dialog.userPasswd == "" :
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\nX-Auth-User-Admin: true\r\nX-Auth-User-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass, dialog.userPasswd)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+dialog.accountName+"/"+dialog.userName)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        if not(rtn == 201) :
            wx.MessageBox('Create User Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Create User Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK)) 
        else:
            self.textControl.AppendText(">Create User Success\r\n") 
            self.textControl.AppendText("Created Account: %s\r\n\r\n" %dialog.userName)  
                            
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return




def DeleteUser(self):
        dialog = DialogClass.dialogDeleteUser(self, -1, 'Delete User')
        dialog.ShowModal()
        dialog.Destroy()
        
        if dialog.accountName == "" or dialog.userName == "" :
            self.EmptyInput()
            return

        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+dialog.accountName+"/"+dialog.userName)
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
            wx.MessageBox('Delete User Failed' ,'Notices' ,wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Delete User Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")             
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK)) 
        else:
            self.textControl.AppendText(">Delete User Successr\n") 
            self.textControl.AppendText("Deleted Account: %s\r\n\r\n" %dialog.userName)  
                    
        headerBuf.close()
        bodyBuf.close()
        c.close()
        return 




def DeleteUserAll(self):
        accountName = ""
        textDialog = wx.TextEntryDialog(self, ' Enter a Account Name to Delete', 'Notices', '', wx.OK|wx.CANCEL|wx.CENTRE)        
        if textDialog.ShowModal() == wx.ID_OK:
            accountName = textDialog.GetValue().strip()
            accountName = accountName.encode('utf-8')
            self.SetStatusText('You entered: %s\n' % textDialog.GetValue())
        textDialog.Destroy()
        
        if accountName == "":
            self.EmptyInput()
            return
        
        headerBuf = cStringIO.StringIO()
        bodyBuf = cStringIO.StringIO()
        requestHeader = "X-Auth-Admin-User: %s\r\nX-Auth-Admin-Key: %s\r\n\r\n" \
                %(self.swauth_admin, self.swauth_adminpass)
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.swauth_url+"/"+accountName)
        c.setopt(pycurl.SSL_VERIFYPEER, False)
        c.setopt(pycurl.VERBOSE, False)
        c.setopt(pycurl.TCP_NODELAY, True)
        c.setopt(pycurl.HTTPHEADER, [requestHeader])
        c.setopt(pycurl.CUSTOMREQUEST, "GET")   
        c.setopt(c.HEADERFUNCTION, headerBuf.write)         
        c.setopt(c.WRITEFUNCTION, bodyBuf.write)
        c.perform()
        rtn = c.getinfo(c.HTTP_CODE)
        
        if not(rtn == 200) :
            wx.MessageBox('Show Account User List Failed' ,'Notices',wx.OK|wx.ICON_INFORMATION)        
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.textControl.AppendText(">Show Account User List Failed\r\n")
            self.textControl.AppendText(headerBuf.getvalue())          
            self.textControl.AppendText(bodyBuf.getvalue())    
            self.textControl.AppendText("\r\n\r\n")           
            self.textControl.SetDefaultStyle(wx.TextAttr(wx.BLACK))         
        else:   
            decoded = json.loads(bodyBuf.getvalue())
            for i in decoded:
                if i=="users":
                    for k in decoded[i]:
                        deleteuser = k['name']
                        deleteuser = deleteuser.encode('utf-8')
                        print self.storageUrl+"/"+accountName+"/"+deleteuser
                        c.setopt(pycurl.URL, self.swauth_url+"/"+accountName+"/"+deleteuser)
                        c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
                        c.perform()
                        rtn = c.getinfo(c.HTTP_CODE)
                        if not(rtn == 204) :
                            self.textControl.AppendText("User Delete Failed: %s  return[%d]\r\n" %(deleteuser, rtn))
                        else:
                            self.textControl.AppendText("User Deleted: %s  return[%d] \r\n" %(deleteuser, rtn))
            

          
#            c.setopt(pycurl.URL, self.swauth_url+"/"+accountName)
#            c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
#            c.perform()                        
#            rtn = c.getinfo(c.HTTP_CODE)
#            if not(rtn == 204 ) :
#                self.textControl.AppendText("Container Delete Failed: %s [%s]\r\n%s\r\n" %(accountName, rtn, bodyBuf.getvalue()))
#            else:
#                self.textControl.AppendText("Container Deleted: %s [%s]\r\n" %(accountName, rtn))    
     

        headerBuf.close()
        bodyBuf.close()
        c.close()
        return




