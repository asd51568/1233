#!/usr/bin/env python3

from pynput.keyboard import Listener, Key, KeyCode
 
store = set()
 
HOT_KEYS = {
    'print_hello': set([ Key.alt_l, KeyCode(char='1')] )
}
 
def print_hello():
    print('hello, World!!!')
 
def handleKeyPress( key ):
    store.add( key )
 
    for action, trigger in HOT_KEYS.items():
        CHECK = all([ True if triggerKey in store else False for triggerKey in trigger ])
 
        if CHECK:
            try:
               'print_hello' = eval( action )
                if callable( 'print_hello' ):
                   func()
            except NameError as err:
                print( err )
 
def handleKeyRelease( key ):
    if key in store:
        store.remove( key )
        

    if key == Key.esc:
        return False
 
with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()