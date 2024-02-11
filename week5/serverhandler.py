import openstack
import base64

class OpenstackHandler:
    def __init__(self):
        self.conn = openstack.connect(cloud='openstack')


    def showServers(self):
        try:
            for server in self.conn.compute.servers():
                floatingip = "no ip found"
                if server.addresses:
                    for network_name, addresses in server.addresses.items():
                        for address in addresses:
                            if address['OS-EXT-IPS:type'] == 'floating':
                                floatingip = address['addr']
                print(f"{server.name} {floatingip}")
        except Exception as e:
            print(f"Error listing servers: {str(e)}")


    
    def createServer(self, message):
        try:
            userData = f'''#!/bin/bash
            sudo su
            cd
            apt update
            apt install nginx -y
            echo "<h1>{message}</h1>" > /var/www/html/index.nginx-debian.html
            '''
            encodedUserData = base64.b64encode(userData.encode('utf-8')).decode('utf-8')
            serverlen = sum(1 for _ in self.conn.compute.servers())
            image = self.conn.image.find_image("Ubuntu Server 22.04")
            flavor = self.conn.compute.find_flavor("f1.small")
            network = self.conn.network.find_network("Internal2")
            keypair = self.conn.compute.find_keypair("test")
            server = self.conn.compute.create_server(
                name=f"server{serverlen}",
                image_id=image.id,
                flavor_id=flavor.id,
                networks=[{"uuid": network.id}],
                key_name=keypair.name,
                tags=["scripted"],
                user_data=encodedUserData,
                security_groups=[{"name":"week1"}],
            )
            server = self.conn.compute.wait_for_server(server)
            floating = self.conn.network.create_ip(floating_network_id="d465430b-1572-43e7-b162-1a4ad5fb3a74")
            self.conn.compute.add_floating_ip_to_server(server, floating.floating_ip_address)
            print(f'Created server named "server{serverlen}" with ip {floating.floating_ip_address}')
        except Exception as e:
            print(f"Error creating server: {str(e)}")


    def deleteServer(self, num):
        try:
            deleted = False
            floatingip = ""
            for server in self.conn.compute.servers():
                if 'scripted' in server.tags:
                    if server.name == f'server{num}':
                        if server.addresses:
                            for network_name, addresses in server.addresses.items():
                                for address in addresses:
                                    if address['OS-EXT-IPS:type'] == 'floating':
                                        floatingip = address['addr']
                        ip = self.conn.network.find_ip(floatingip)
                        self.conn.network.delete_ip(ip)
                        self.conn.delete_server(server)
                        print(f'deleted server "server{num}" and its floating ip')
                        deleted = True
            if not deleted:
                print(f'could not find server "server{num}"')
        except Exception as e:
            print(f'failed to delete server: {e}')

    def getTaggedServers(self):
        servers = []
        for server in self.conn.compute.servers():
                if 'scripted' in server.tags:
                        servers.append(server)
        return servers