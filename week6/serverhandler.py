import openstack
import base64

class OpenstackHandler:
    def __init__(self):
        self.conn = openstack.connect(cloud='openstack')


    def showServers(self):
        try:
            responses = []
            for server in self.conn.compute.servers():
                floatingip = "no ip found"
                if "wordpress" in server.tags:
                    if server.addresses:
                        for network_name, addresses in server.addresses.items():
                            for address in addresses:
                                if address['OS-EXT-IPS:type'] == 'floating':
                                    floatingip = address['addr']
                    responses.append({"id":server.id, "ip":floatingip, "state":server.status})
            return responses
        except Exception as e:
           return (f"Error listing servers: {str(e)}")


    
    def createServer(self):
        try:
            f = open("web.bash", "r")
            userData = f.read()
            encodedUserData = base64.b64encode(userData.encode('utf-8')).decode('utf-8')
            serverlen = sum(1 for _ in self.conn.compute.servers())
            image = self.conn.image.find_image("Ubuntu Server 22.04")
            flavor = self.conn.compute.find_flavor("f1.small")
            network = self.conn.network.find_network("Internal2")
            keypair = self.conn.compute.find_keypair("test")
            server = self.conn.compute.create_server(
                name=f"wordpress{serverlen}",
                image_id=image.id,
                flavor_id=flavor.id,
                networks=[{"uuid": network.id}],
                key_name=keypair.name,
                tags=["wordpress"],
                user_data=encodedUserData,
                security_groups=[{"name":"week1"}],
            )
            server = self.conn.compute.wait_for_server(server)
            floating = self.conn.network.create_ip(floating_network_id="d465430b-1572-43e7-b162-1a4ad5fb3a74")
            self.conn.compute.add_floating_ip_to_server(server, floating.floating_ip_address)
            return {"id": server.id, "ip":floating.floating_ip_address}
        except Exception as e:
            return (f"Error creating server: {str(e)}")


    def deleteServer(self,  ip):
            try:
                deleted = False
                for server in self.conn.compute.servers():
                    if 'wordpress' in server.tags:
                            if server.addresses:
                                for network_name, addresses in server.addresses.items():
                                    for address in addresses:
                                        if address['OS-EXT-IPS:type'] == 'floating':
                                            if str(ip) == str(address['addr']):
                                                deleteip = self.conn.network.find_ip(ip)
                                                self.conn.network.delete_ip(deleteip)
                                                self.conn.delete_server(server)
                                                deleted = True
                                                return {}
                if not deleted:
                    return (f'could not find server')
            except Exception as e:
                return (f'failed to delete server: {e}')