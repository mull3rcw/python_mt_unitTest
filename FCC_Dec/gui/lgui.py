from Tkinter import *
root = Tk()
def hello(event): print 'Got tag event'


text = Text()
text.config(font=('courier', 15, 'normal'))                 
text.config(width=20, height=12)
text.pack(expand=YES, fill=BOTH)
text.insert(END, 'Insert Card\n')  


text.tag_add('demo', '1.5', '1.7')                      
text.tag_add('demo', '3.0', '3.3')                      
text.tag_add('demo', '5.3', '5.7')                      
text.tag_bind('demo', '<Double-1>', hello)              
root.mainloop()
