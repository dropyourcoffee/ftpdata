import unittest
import docker
import os
from datetime import datetime
import rsa
from ftpdata.util import unzip
from collections import namedtuple
from time import sleep
import subprocess


class MockSFTP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        manifest_dir = os.path.dirname(os.path.realpath(__file__))
        keyfile = "key.pem"
        key_pub = "id_rsa.pub"
        hostPort = 10022
        username = 'user'
        passwd = ''

        """
         Step 1. Make a new ssh key pair
         
        """
        publicKey, privateKey = rsa.newkeys(2048)

        with open(os.path.join(manifest_dir, keyfile), 'w', 600) as f:
            f.write(privateKey.save_pkcs1().decode('utf8'))
        os.chmod(os.path.join(manifest_dir, keyfile), 0o600)

        cmd = ["ssh-keygen", "-y", "-f", os.path.join(manifest_dir, keyfile)]
        with open(os.path.join(manifest_dir, key_pub), 'wb') as f:
            pub = subprocess.run(cmd, stdout=subprocess.PIPE)
            f.write(pub.stdout)


        """
         Step 2. Create User profile.
        
        """
        with open(os.path.join(manifest_dir, 'users.conf'), 'w') as f:
            f.write(f"{username}:{passwd}")


        """
         Step 3. Create SFTP Container
         
        """
        container_name = "test-sftp"
        client = docker.from_env()
        api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

        client.containers.run("atmoz/sftp",
                              detach=True,
                              name=container_name,
                              volumes={
                                  os.path.join(manifest_dir, "users.conf"): {'bind': '/etc/sftp/users.conf', 'mode': 'ro'},
                                  os.path.join(manifest_dir, "testdata")  : {'bind': f'/home/{username}/testdata'},
                                  os.path.join(manifest_dir, "id_rsa.pub"): {'bind': f'/home/{username}/.ssh/keys/id_rsa.pub', 'mode': 'ro'},
                              },
                              ports={'22/tcp': hostPort})
        cls._container = client.containers.get(container_name)
        ports = api_client.inspect_container(cls._container.id)['NetworkSettings']['Ports']
        cls._client = client

        """
         Step 4. Parse Access Configurations to test scripts.
        
        """
        keys, values = unzip({
            'host': "localhost",
            'port': ports['22/tcp'][0]["HostPort"],
            'username': username,
            'keyfile': os.path.join(manifest_dir, keyfile),
            'url': f"sftp://localhost:{ports['22/tcp'][0]['HostPort']}"
        })

        cls.mock_sftp_config = namedtuple('config', keys)(*values)

        print(f"Mock SFTP setup...  ", end='')
        sleep(1)
        print("OK")
        print(cls.mock_sftp_config)


    @classmethod
    def tearDownClass(cls):
        cls._container.remove(force=True)
        cls._client.close()
