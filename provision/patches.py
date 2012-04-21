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

    def __init__(self, target, source):
        """
        @type target: C{str}
        @keyword target: Path on node to install file

        @type source: C{str}
        @keyword source: Local path of file to be installed
        """
        self.target = target
        self.source = source

    def run(self, node, client):
        """
        Upload the file, retaining permissions

        See also L{Deployment.run}
        """
        perms = os.stat(self.source).st_mode
        client.put(path=self.target, chmod=perms, contents=open(self.source).read())
        return node

libcloud.compute.deployment.FileDeployment = FileDeployment
