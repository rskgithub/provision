"""This module contains various monkey patches to libcloud libraries
necessary for aws support.

see: http://stackoverflow.com/questions/3765222/monkey-patch-python-class
"""

import os
import libcloud.compute.deployment

# FileDeployment can be used by all drivers, a general replacement for ex_files param

class FileDeployment(libcloud.compute.deployment.Deployment):
    """
    Install a file.
    """

    def __init__(self, source, target):
        """
        @type source: C{str}
        @keyword source: Local path of file to be installed

        @type target: C{str}
        @keyword target: Path on node to install file
        """
        self.source = source
        self.target = target

    def run(self, node, client):
        """
        Upload the file, retaining permissions

        See also L{Deployment.run}
        """
        perms = os.stat(self.source).st_mode
        client.put(path=self.target, chmod=perms,
                   contents=open(self.source, 'rb').read())
        return node

libcloud.compute.deployment.FileDeployment = FileDeployment


import libcloud.compute.types
class DeploymentError(libcloud.compute.types.LibcloudError):
    """
    Exception used when a Deployment Task failed.

    @ivar node: L{Node} on which this exception happened, you might want to call L{Node.destroy}
    """
    def __init__(self, node, original_exception=None, driver=None):
        self.node = node
        self.value = original_exception
        self.driver = driver

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (('<DeploymentError: node=%s, error=%s>'
                % (self.node.id, str(self.value))))

libcloud.compute.types.DeploymentError = DeploymentError


import time
from libcloud.common.types import LibcloudError
from libcloud.compute.types import NodeState

def NodeDriver_wait_until_running(self, node, wait_period=3, timeout=600,
                                  ssh_interface='public_ips'):
    """
    Block until node is fully booted and has an IP address assigned.

    @keyword    node: Node instance.
    @type       node: C{Node}

    @keyword    wait_period: How many seconds to between each loop
                             iteration (default is 3)
    @type       wait_period: C{int}

    @keyword    timeout: How many seconds to wait before timing out
                         (default is 600)
    @type       timeout: C{int}

    @return: C{Node} Node instance on success.
    """
    start = time.time()
    end = start + timeout

    while time.time() < end:
        nodes = self.list_nodes()
        nodes = list([n for n in nodes if n.uuid == node.uuid])

        if len(nodes) > 1:
            raise LibcloudError(value=('Booted single node[%s], ' % node
                                + 'but multiple nodes have same UUID'),
                                driver=self)

        if (len(nodes) == 1 and nodes[0].state == NodeState.RUNNING and \
                hasattr(nodes[0], ssh_interface) and getattr(nodes[0], ssh_interface)):
            return (nodes[0], getattr(nodes[0], ssh_interface))
        else:
            time.sleep(wait_period)
            continue

    raise LibcloudError(value='Timed out after %s seconds' % (timeout),
                        driver=self)

import libcloud.compute.base
libcloud.compute.base.NodeDriver._wait_until_running = NodeDriver_wait_until_running
