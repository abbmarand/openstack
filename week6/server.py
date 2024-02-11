from flask import Flask, request
import serverhandler
openstack = serverhandler.OpenstackHandler()
app = Flask(__name__)

@app.route('/list-wp-instances')
def list():
    data = openstack.showServers()
    return f"{data}"

@app.route('/create-wp-instance')
def create():
    data = openstack.createServer()
    return f"{data}"

@app.route('/delete-wp-instance')
def delete():
    ip = request.args.get("ip")
    data = openstack.deleteServer(ip)
    return f"{data}"

if __name__ == '__main__':
    app.run(debug=True, port=8080)
