"""
This script uses PyQt4 to create a gui which allows tabbed matplotlib figures. Boomshaka!
"""
import sys
from six.moves import zip_longest #python 2 compat

#from PyQt4 import QtCore
from matplotlib.backends.qt_compat import QtGui, QtCore
SIGNAL = QtCore.SIGNAL

from matplotlib import use
use('QT4Agg')

from matplotlib.backends.backend_qt4 import (FigureCanvasQT as FigureCanvas,
                                            NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

import numpy as np
#from decor import expose, profile

#__all__ = []

#****************************************************************************************************
class MultiTabNavTool(QtGui.QWidget):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, canvases, tabs, parent=None):
        '''Create one navigation toolbar per tab, switching between them upon tab change'''
        QtGui.QWidget.__init__(self, parent)
        self.canvases = canvases
        self.tabs = tabs
        self.toolbars = [NavigationToolbar(canvas, parent) for canvas in self.canvases]
        
        self.vbox = QtGui.QVBoxLayout()
        
        for toolbar in self.toolbars:
            self.add( toolbar )
        self.setLayout(self.vbox)
        
        #switch between toolbars when tab is changed
        self.tabs.currentChanged.connect(self.switch_toolbar)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add(self, canvas, parent):
        tool = NavigationToolbar(canvas, parent)
        self.toolbars.append( tool )
        self.vbox.addWidget( tool )
        tool.setVisible(False)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def switch_toolbar(self):
        for toolbar in self.toolbars:
            toolbar.setVisible(False)
        
        self.toolbars[self.tabs.currentIndex()].setVisible(True)

    
   
        
#######################################################################################################################    
class MplMultiTab(QtGui.QMainWindow):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, parent=None, figures=[], labels=[], title=None):
        QtGui.QMainWindow.__init__(self, parent)
        title = title or 'MplMultiTab'
        self.setWindowTitle( title )
        
        self.canvases = []
        
        self.create_menu()
        self.create_main_frame( figures, labels )
        self.create_status_bar()

        #self.textbox.setText('1 2 3 4')
        #self.on_draw()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save_plots(self, filenames, path=''):
        import os
        #file_choices = "PNG (*.png)|*.png"
        #path = str(QFileDialog.getSaveFileName(self, 
                        #'Save file', '', 
                        #file_choices))
        path = os.path.realpath(path) + os.path.sep
        ntabs = len(self.canvases)
        if isinstance(filenames, str):
            if not '{' in filenames:            #no format str specifier
                filenames = filenames + '{}'    #append numerical
            filenames = [filenames.format(i) for i in range(ntabs)]
          
        for i, canvas in enumerate(self.canvases):
            filename = filenames[i]
            root, name = os.path.split(filename)
            if root:
                savename = filename
            else:
                savename = os.path.join(path, filename)
            
            canvas.figure.savefig(savename)
            
        #if path:
            #self.canvas.print_figure(path, dpi=self.dpi)
            #self.statusBar().showMessage('Saved to %s' % path, 2000)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def on_about(self):
        msg = """ doom dooom doom... doom di doom DOOOOOOM!!!!
        """
        QtGui.QMessageBox.about(self, "About the demo", msg.strip())
    
    #def on_pick(self, event):
        ## The event received here is of the type
        ## matplotlib.backend_bases.PickEvent
        ##
        ## It carries lots of information, of which we're using
        ## only a small amount here.
        ## 
        #box_points = event.artist.get_bbox().get_points()
        #msg = "You've clicked on a bar with coords:\n %s" % box_points
        
        #QMessageBox.information(self, "Click!", msg)
    
    #def on_draw(self):
        #""" Redraws the figure
        #"""
        #string = str(self.textbox.text())
        #self.data = list(map(int, string.split()))
        
        #x = list(range(len(self.data)))

        ## clear the axes and redraw the plot anew
        #self.axes.clear()        
        #self.axes.grid(self.grid_cb.isChecked())
        
        #self.axes.bar(
            #left=x, 
            #height=self.data, 
            #width=self.slider.value() / 100.0, 
            #align='center', 
            #alpha=0.44,
            #picker=5)
        
        #self.canvas.draw()
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #@print_args()
    def create_tabs(self, figures, labels):
        for fig, lbl in zip_longest(figures, labels):
            self.add_tab(fig, lbl)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #@print_args()
    def create_main_frame(self, figures, labels):
        
        self.main_frame = QtGui.QWidget()
        self.tabWidget = QtGui.QTabWidget( self.main_frame )
        
        # Create the navigation toolbar NOTE: still empty
        self.mpl_toolbar = MultiTabNavTool(self.canvases, self.tabWidget, self.main_frame)
        
        #NavigationToolbar(canvas, parent) for canvas in self.canvases
        
        #tabs = QtGui.QTabWidget()
        
        self.create_tabs( figures, labels )
        
        
        
        # Bind the 'pick' event for clicking on one of the bars
        #canvas.mpl_connect('pick_event', self.on_pick)
        
        
        
        
        # Other GUI controls
        #self.textbox = QtGui.QLineEdit()
        #self.textbox.setMinimumWidth(200)
        #self.connect(self.textbox, SIGNAL('editingFinished ()'), self.on_draw)
        
        #self.draw_button = QtGui.QPushButton("&Draw")
        #self.connect(self.draw_button, SIGNAL('clicked()'), self.on_draw)
        
        #self.grid_cb = QtGui.QCheckBox("Show &Grid")
        #self.grid_cb.setChecked(False)
        #self.connect(self.grid_cb, SIGNAL('stateChanged(int)'), self.on_draw)
        
        #slider_label = QtGui.QLabel('Bar width (%):')
        #self.slider = QtGui.QSlider(Qt.Horizontal)
        #self.slider.setRange(1, 100)
        #self.slider.setValue(20)
        #self.slider.setTracking(True)
        #self.slider.setTickPosition(QSlider.TicksBothSides)
        #self.connect(self.slider, SIGNAL('valueChanged(int)'), self.on_draw)
        
    
        # Layout with box sizers
        #hbox = QHBoxLayout()
        
        #for w in [  self.textbox, self.draw_button, self.grid_cb,
                    #slider_label, self.slider]:
            #hbox.addWidget(w)
            #hbox.setAlignment(w, Qt.AlignVCenter)
        
        #print( self.mpl_toolbar.toolbars )
        
        self.vbox = vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.tabWidget)
        #vbox.addLayout(hbox)
        
        self.main_frame.setLayout(vbox)
        
        self.setCentralWidget(self.main_frame)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #@print_args()
    def add_tab(self, fig, name=None):
        '''dynamically add tabs with embedded matplotlib canvas using this function.'''
        
        # initialise FigureCanvas
        canvas = fig.canvas     or      FigureCanvas(fig)
        canvas.setParent(self.tabWidget)
        canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvases.append( canvas )
        
        self.mpl_toolbar.add(canvas, self.main_frame )
        
        name = 'Tab %i'%(self.tabWidget.count()+1) if name is None else name
        self.tabWidget.addTab(canvas, name)
        
        plt.close( fig )
        
        return canvas
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_figure(self):
        '''Create a figure from data and add_tab.  To be over-written by subclass.
        Useful when multiple figures of the same kind populate the tabs.'''
        fig = Figure()
        fig.add_subplot(111)
        # Since we have only one plot, we can use add_axes instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't  work.
        
        self.add_tab( fig )
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #def _default_figure(self):

    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_status_bar(self):
        self.status_text = QtGui.QLabel("This is a demo")
        self.statusBar().addWidget(self.status_text, 1)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_menu(self):        
        self.file_menu = self.menuBar().addMenu("&File")
        
        load_file_action = self.create_action("&Save plot",
            shortcut="Ctrl+S", slot=self.save_plots, 
            tip="Save the plot")
        quit_action = self.create_action("&Quit", slot=self.close, 
            shortcut="Ctrl+Q", tip="Close the application")
        
        self.add_actions(self.file_menu, 
            (load_file_action, None, quit_action))
        
        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", 
            shortcut='F1', slot=self.on_about, 
            tip='About the demo')
        
        self.add_actions(self.help_menu, (about_action,))

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_action(  self, text, slot=None, shortcut=None, 
                        icon=None, tip=None, checkable=False, 
                        signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action




#****************************************************************************************************
class MplMultiTab2D(QtGui.QMainWindow):
    '''Combination tabs display matplotlib canvas'''
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, figures=[], labels=[], shape=None, title=None):
        #TODO: ND
        ''' '''
        super().__init__()
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle(title or self.__class__.__name__)
        
        self.figures = np.array(figures).reshape(shape)
        self.labels = labels    #np.array(labels).reshape(self.figures.shape)
        
        #create main widget
        self.main_widget = QtGui.QWidget(self)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        
        #Create the navigation toolbar stack
        self.toolstack = QtGui.QStackedWidget(self.main_widget)
        
        #stack switches display for central pannel
        self.stack = QtGui.QStackedWidget(self.main_widget)
        
        #create the tab bars
        self.tabbars = []
        for loc, lbls in zip((QtGui.QTabBar.RoundedWest, QtGui.QTabBar.RoundedNorth), 
                             self.labels):
            tabs = self._create_tabs(loc, lbls)
            tabs.currentChanged.connect(self.tab_change)
            self.tabbars.append(tabs)
        self.tabsWest, self.tabsNorth = self.tabbars
        
        #define layout
        grid = QtGui.QGridLayout(self.main_widget)
        #grid.setSpacing(10)
        
        #add widgets to layout
        grid.addWidget(self.toolstack, 0, 0, 1, 2)
        grid.addWidget(self.tabsNorth, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        grid.addWidget(self.tabsWest, 2, 0, 1, 1, QtCore.Qt.AlignTop)
        grid.addWidget(self.stack, 2, 1)
        
        #add canvasses to stack
        for row in self.figures:
            for fig in row:
                #print(self._rows*i + j)
                #print(fig)
                canvas = fig.canvas
                navtool = NavigationToolbar(canvas, self.toolstack)
                self.stack.addWidget(canvas)
                self.toolstack.addWidget(navtool)
                
                plt.close()
                
        #self.show()
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def _create_tabs(self, loc, labels):
        '''create the tab bars at location with labels'''
        tabs = QtGui.QTabBar(self.main_widget)
        tabs.setShape(loc)
        for i, d in enumerate(labels):
            tabs.addTab(d)
        
        return tabs
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def tab_change(self):
        '''Called upon change of tab'''
        i, j = self.tabsWest.currentIndex(), self.tabsNorth.currentIndex()
        nrows, ncols = self.figures.shape
        ix = i*ncols + j
        #print( 'shape:', self.figures.shape )
        #print(i,j, ix)
        #print()
        #print(self.stack.currentWidget())
        
        self.stack.setCurrentIndex(ix)
        self.toolstack.setCurrentIndex(ix)
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def save_plots(self, filenames, path=''):
        import os
        #file_choices = "PNG (*.png)|*.png"
        #path = str(QFileDialog.getSaveFileName(self, 
                        #'Save file', '', 
                        #file_choices))
        path = os.path.realpath(path) + os.path.sep
        ntabs = len(self.canvases)
        if isinstance(filenames, str):
            if not '{' in filenames:            #no format str specifier
                filenames = filenames + '{}'    #append numerical
            filenames = [filenames.format(i) for i in range(ntabs)]
          
        for i, canvas in enumerate(self.canvases):
            filename = filenames[i]
            root, name = os.path.split(filename)
            if root:
                savename = filename
            else:
                savename = os.path.join(path, filename)
            
            canvas.figure.savefig(savename)

#def main():



if __name__ == "__main__":
    import numpy as np
    
    #Example use
    colours = 'rgb'
    figures, labels = [], []
    for i in range(3):
        fig, ax = plt.subplots()
        ax.plot( np.random.randn(100), colours[i]        )
        figures.append( fig )
        labels.append( 'Tab %i'%i )
    
    app = QtGui.QApplication(sys.argv)
    ui = MplMultiTab( figures=figures, labels=labels)
    ui.show()
    #from IPython import embed
    #embed()
    sys.exit( app.exec_() )
    
    #main()
