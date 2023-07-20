from flask import Flask, render_template, json, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)

filename = "orders.txt"
now = datetime.now() # current date and time

def formatorderlist(orderlist):
    orderdict = {}

    for n in range (0,len(orderlist)):

        tmp = orderlist[n].split(";")
        for m in tmp:
            if "ordertime" in m:
                orderdict["Order time"] = m.split(":")[1]
            elif "ordernum" in m:
                orderdict["Order number"] = m.split(":")[1]
            elif "flavor" in m:
                orderdict["Flavor"] = m.split(":")[1]
            elif "sugar" in m:
                orderdict["Sugar"] = m.split(":")[1]
            elif "size" in m:
                orderdict["Size"] = m.split(":")[1]
            elif "name" in m:
                orderdict["Name on the order"] = m.split(":")[1]
            elif "instructions" in m:
                orderdict["Special instruction(s)"] = m.split(":")[1]
            elif "orderstatus" in m:
                orderdict["Order status"] = m.split(":")[1]
            elif "ordernotes" in m:
                orderdict["Order notes"] = m.split(":")[1]
        orderlist[n] = orderdict
        orderdict = {}
    return orderlist

@app.route('/',methods=["GET", "POST"])
def main():
    return render_template('order.html')

@app.route('/order',methods=["GET", "POST"])
def order():
    orderlist = []
    _action = request.form["action"]
    if _action == "Submit Order":
        _ordertime = now.strftime("%m/%d/%Y, %H-%M")
        _flavor = request.form["flavor"]
        _sugar = request.form["sugar"]
        _size = request.form["size"]
        _name = request.form["name"]
        _instructions = request.form["instructions"]

        if _flavor and _sugar and _size and _name:
            pass
        else:
            _message = "Please Enter ALL required fields"
            return render_template('order.html',message= _message)
    elif _action == "Check Status":
        return render_template('orderstatus.html')
    elif _action == "Don't push this button!":
        return render_template('orderlogin.html')


    try:

        with open(filename) as orderfile:
            for order in orderfile:
                orderlist.append(order)
            orderfile.close()
            _ordernum = str(len(orderlist) + 1)
            orderlist.append("ordernum:{};ordertime:{};flavor:{};sugar:{};size:{};name:{};instructions:{};orderstatus:{};ordernotes:{}{}".format(_ordernum,_ordertime,_flavor,_sugar,_size,_name,_instructions,"Order Received","Thank you for your order - it will be processed shortly!","\n"))
            orderfile = open(filename,"w")
            for order in orderlist:
                orderfile.write(order)
            orderfile.close()
    except IOError:
        _ordernum = "1"
        orderfile = open(filename,"w")
        orderfile.write("ordernum:{};ordertime:{};flavor:{};sugar:{};size:{};name:{};instructions:{};orderstatus:{};ordernotes:{}{}".format(_ordernum,_ordertime,_flavor,_sugar,_size,_name,_instructions,"Order Received","Thank you for your order - it will be processed shortly!","\n"))
        orderfile.close()
    _message = "Thank you for your order! Your order number is - " + _ordernum
    return render_template('order.html',message = _message)

@app.route('/orderstatus',methods = ['POST', 'GET'])
def orderstatus():

    _orderlist = []
    _action = request.form["action"]
    if _action == "Home":
        return render_template('order.html')

    _ordernum = request.form["ordernum"]
    _ordername = request.form["ordername"]
    if _ordernum.isnumeric():
        pass
    else:
        _message = "Please enter a valid order number"
        return render_template('orderstatus.html',message = _message)

    with open(filename) as orderfile:
        for order in orderfile:
            _orderlist.append(order.rstrip("\n"))
        orderfile.close()

    orderfound = False
    for order in _orderlist:
        if _ordernum == order.split(":")[1].replace(";ordertime","") and  _ordername == order.split(":")[6].replace(";instructions",""):
            orderfound = True
            _orderlist = formatorderlist([order])
            break
    if orderfound:
        return render_template('orderstatus.html',orderlist = _orderlist)
    else:
        _message = "Your order has not been found"
        return render_template('orderstatus.html',message =_message)

@app.route('/orderlogin',methods = ['POST', 'GET'])
def orderlogin():
    def buildorderlist():
        _orderlist = []
        with open(filename) as orderfile:
            for order in orderfile:
                _orderlist.append(order)
            orderfile.close()
        return (formatorderlist(_orderlist))

    _password = request.form["password"]
    if _password == "supersecret123":
        _orderlist = buildorderlist()
        return render_template('ordermanage.html',orderlist=_orderlist)
    else:
        _message = "Don't you ever go to that page again!!!"
        return render_template('order.html',message=_message)

@app.route('/ordermanage',methods = ['POST', 'GET'])
def ordermanage():

    _action = request.form["action"]
    if _action == "Home":
        return render_template('order.html')

@app.route('/orderupdate',methods = ['POST', 'GET'])
def orderupdate():

    _orderlist = []
    _action = request.form["action"]
    if _action == "Update":
        _ordernum = request.form["ordernum"]
        _oldorderstatus = request.form["oldorderstatus"]
        _oldordernotes = request.form["oldordernotes"]
        _neworderstatus = request.form["neworderstatus"]
        _newordernotes = request.form["newordernotes"]

        with open(filename) as orderfile:
            for order in orderfile:
                _orderlist.append(order.rstrip("\n"))
            orderfile.close()
        for n in range (0,len(_orderlist)):
            if "ordernum:{}".format(_ordernum) in _orderlist[n]:
                tmp =  _orderlist[n].split(";")
                for m in range (0,len(tmp)):
                    if "orderstatus:" in tmp[m]:
                        if _oldorderstatus != _neworderstatus:
                            tmp[m] = "orderstatus:{}".format(_neworderstatus)
                    if "ordernotes:" in tmp[m]:
                        if _oldordernotes != _newordernotes:
                            tmp[m] = "ordernotes:{}".format(_newordernotes)
                _orderlist[n] = ";".join(tmp)

        orderfile = open(filename,"w")
        for order in _orderlist:
            orderfile.write(order + "\n")
        orderfile.close()

        _orderlist = []

        with open(filename) as orderfile:
            for order in orderfile:
                _orderlist.append(order.rstrip("\n"))
            orderfile.close()

        _orderlist = formatorderlist(_orderlist)

        _message = "Order has been updated successfuly"
        return render_template('ordermanage.html',message=_message,orderlist = _orderlist)

if __name__ == "__main__":
    app.run()
