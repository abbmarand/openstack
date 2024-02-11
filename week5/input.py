import serverhandler
import os

openstack = serverhandler.OpenstackHandler()
def show():
    os.system('clear')
    print(".: Web Server Automator :.")
    print("--------------------------")
    print("create | Create web server")
    print("delete | Delete web server")
    print("list   | List web server")
    print("--------------------------")
    option = str(input(">")).lower()

    if(option == "create"):
        try:
            data = str(input("message for server: ")).lower()
            openstack.createServer(data)
            input("continue...")
            show()
        except Exception as e:
            print(f"error creating: {e}")
            input("continue...")
            show()
    elif(option == "delete"):
        try:
            deleted = False
            servers = openstack.getTaggedServers()
            print("servers created by script:")
            for server in servers:
                print(server.name)
            index = int(input("index to delete: "))
            for server in servers:
                if server.name == f"server{index}":
                    openstack.deleteServer(index)
                    deleted = True
            if not deleted:
                print(f"could not find server{index}")
            input("continue...")
            show()
        except Exception as e:
            print(f"error deleting: {e}")
            input("continue...")
            show()
    elif(option == "list"):
        openstack.showServers()
        input("continue...")
        show()
    else:
        show()
show()