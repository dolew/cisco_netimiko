from flask import Flask, Response, request, url_for, redirect, render_template
from netmiko import ConnectHandler
import sys
import os
import ast
app = Flask(__name__)
@app.route('/')
def hello():
    return "hello"
@app.route('/vlan', methods=['GET', 'POST'])
def vlan_creation():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        file = open(f.filename, "r")
        contents = file.read()
        dict = ast.literal_eval(contents)
        x = 0
        exp = []
        check = 0
        lst = []
        i = 0
        limit = len(dict)
        while( limit != 0):
            index1 = 0
            x += 1
            print('""""""""""""""""configuration for switch make => ' + str(x) + '\n')
            print(dict[limit])
            index_x = int(request.form['indexX'])
            index_y= int(request.form['indexY'])
            lst = ast.literal_eval(request.form['novlan'])
            lst1 = ast.literal_eval(request.form['interface'])
            index2 = len(lst1[index1]) - 1
            n = len(lst)
            net_connect = ConnectHandler(**dict[limit])
            vlan_names = request.form['vlanN']
            for n in range (index_x, index_y):
              while(len(lst) > i):
                if(lst[i] == n):
                    check = 1
                    break
                else:
                    check = 0
                i += 1
              i = 0
              if(check == 0):
                print ('creating vlan ' + str(n))
                config_commands = ['vlan ' + str(n), 'name ' + vlan_names +str(n)]
                output = net_connect.send_config_set(config_commands)
                print (output)
            while(index2 != -1):
                print('...........trunking setup for ' + lst1[index1][index2] + '..............')
                config_command = ['int ' + lst1[index1][index2], 'switchport trunk encapsulation dot1q']
                output = net_connect.send_config_set(config_command)
                index2 -= 1
                print (output)
            limit -= 1
            index1 += 1
        return 'DONE' 

    return (render_template('template.html'))
if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80, debug=True)

