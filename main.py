import wx
import wx.html
import wx.html2
import feedparser

app = wx.App()

class FinanznachrichtentickerFrame(wx.Frame):

    _pnl = None
    _htmlFeld = None
    _previousCell = None
    _subNewsFrame = None
    _newsFeed = None

    def __init__(self, *args, **kw):

        # ensure the parent's __init__ is called
        super(FinanznachrichtentickerFrame, self).__init__(*args, **kw)

        self._pnl = wx.Panel(self)

        # and create a sizer to manage the layout of child widgets
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # füge RichTextControl Feld hinzu

        self._htmlFeld = wx.html.HtmlWindow(self._pnl, size=(1000, 27), style=wx.html.HW_SCROLLBAR_NEVER) #wx.TextCtrl(self._pnl, size=(400, 350), style=wx.TE_MULTILINE)
        self.Bind(wx.html.EVT_HTML_CELL_HOVER, self.OnLinkHovered, self._htmlFeld)

        logo = wx.StaticBitmap( self._pnl, wx.ID_ANY, wx.Bitmap( "Logo.PNG", wx.BITMAP_TYPE_ANY ))
        sizer.Add(logo,-1, wx.ALIGN_CENTER)

        sizer.Add(self._htmlFeld,-1)

        # assign layout to panel
        self._pnl.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        self.OnLoadNews(None)

    def makeMenuBar(self):
        """
        """
        fileMenu = wx.Menu()
        loadItem = fileMenu.Append(-1, "&Laden...\tCtrl-H")


        # baue die Menüleiste ein
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnLoadNews, loadItem)

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnLoadNews(self, event):

        '''Wir laden die neuesten Finanznachrichten von
        https://www.finanznachrichten.de/rss-nachrichten-meistgelesen.'''

        feedURL = "https://www.finanznachrichten.de/rss-nachrichten-meistgelesen"
        self._newsFeed = feedparser.parse(feedURL)

        for i in self._newsFeed.entries:
            self._htmlFeld.AppendToPage("<a href=" + i.link + ">" + i.title + "</a> // ")


    def OnLinkHovered(self, event):

        if (self._subNewsFrame != None):
            self._subNewsFrame.Move(event.Cell.PosX + self.Rect.Left, self.Rect.Top-240)

        if (event.Cell.Link != None and event.Cell.Link.Href!=self._previousCell):

            try:
                self._subNewsFrame.Close()
                self._subNewsFrame = None
            except:
                None

            # Speichern des Links, den wir überfahren
            linkClicked =  event.Cell.Link.Href

            # Erzeugen des SubNewsFrame
            self._subNewsFrame = wx.Frame(None, title="NEWS!", size=(320,240), style=(wx.STAY_ON_TOP|wx.FRAME_TOOL_WINDOW),
                                     pos=wx.Point(event.Cell.PosX + self.Rect.Left, self.Rect.Top-240))

            htmlWin = wx.html.HtmlWindow(self._subNewsFrame, size=(320,240))
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(htmlWin)
            self._subNewsFrame.SetSizer(sizer)

            # Holen der eigentlichen Nachricht
            newsItem = self.getNewsText(linkClicked)
            htmlToDisplay = "<h4>" + newsItem.title + "</h4>" + newsItem.summary
            htmlWin.AppendToPage(htmlToDisplay)

            # Darstellung
            self._subNewsFrame.Show()

            # Speichern des Links, damit Fenster nicht erneut geöffnet wird,
            # wenn es bereits offen ist
            self._previousCell = linkClicked

    def getNewsText(self, url):
        for i in self._newsFeed.entries:
            if i.link == url:
                return i




if __name__ == '__main__':
    frm = FinanznachrichtentickerFrame(None, title='Finanznachrichten-Ticker', size=(800,90))
    frm.Show()
    app.MainLoop()