"""
Show/Modify/Append registry env-vars (ie `PATH`) and notify Windows-applications to pickup changes.

First attempts to show/modify HKEY_LOCAL_MACHINE (all users), and 
if not accessible due to admin-rights missing, fails-back 
to HKEY_CURRENT_USER.
Write and Delete operations do not proceed to user-tree if all-users succeed.

Syntax: 
    {prog}                  : Print all env-vars. 
    {prog}  VARNAME         : Print value for VARNAME. 
    {prog}  VARNAME   VALUE : Set VALUE for VARNAME. 
    {prog}  +VARNAME  VALUE : Append VALUE in VARNAME delimeted with ';' (i.e. used for `PATH`). 
    {prog}  -VARNAME        : Delete env-var value. 

Note that the current command-window will not be affected, 
changes would apply only for new command-windows.
"""

import winreg
import os, sys, win32gui, win32con

def reg_key(tree, path, varname):
    return {
        'tree': tree,
        'path': path,
        'varname': varname
    }

def reg_entry(tree, path, varname, value):
    return {
        'reg_key': reg_key(tree, path, varname),
        'value': value
    }

def query_value(key, varname):
    value, type_id = winreg.QueryValueEx(key, varname)
    return value

def show_all(tree, path, key):
    i = 0
    entries = []
    while True:
        try:
            n,v,t = winreg.EnumValue(key, i)
            entries.append(reg_entry(tree, path, n, v))
            i += 1
        except OSError:
            break ## Expected, this is how iteration ends.
    return entries

def notify_windows(action, tree, path, varname, value):
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
    return { 
        'action': action, 
        'reg_entry': reg_entry(tree, path, varname, value)
    }

def manage_registry_env_vars(varname=None, value=None):
    reg_keys = [
        ('HKEY_LOCAL_MACHINE', r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'),
        ('HKEY_CURRENT_USER', r'Environment'),
    ]
    for (tree_name, path) in reg_keys:
        tree = eval('winreg.%s'%tree_name)
        try:
            with winreg.ConnectRegistry(None, tree) as reg:
                with winreg.OpenKey(reg, path, 0, winreg.KEY_ALL_ACCESS) as key:
                    if not varname:
                        return show_all(tree_name, path, key)
                    else:
                        if not value:
                            if varname.startswith('-'):
                                varname = varname[1:]
                                value = query_value(key, varname)
                                winreg.DeleteValue(key, varname)
                                return notify_windows("Deleted", tree_name, path, varname, value)
                                break  ## Don't propagate into user-tree.
                            else:
                                value = query_value(key, varname)
                                return reg_entry(tree_name, path, varname, value)
                        else:
                            if varname.startswith('+'):
                                varname = varname[1:]
                                value = query_value(key, varname) + ';' + value
                            winreg.SetValueEx(key, varname, 0, winreg.REG_EXPAND_SZ, value)
                            return notify_windows("Updated", tree_name, path, varname, value)
                            break  ## Don't propagate into user-tree.
        except PermissionError as ex:
            print("!!!Cannot access %s due to: %s" % 
                    (reg_key(tree_name, path, varname), ex))
        except FileNotFoundError as ex:
            print("!!!Cannot find %s due to: %s" % 
                    (reg_key(tree_name, path, varname), ex))
