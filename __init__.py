import os, xmlrpclib

from twisted.internet.defer import succeed, fail, inlineCallbacks, returnValue

from juju.errors import (MachinesNotFound, ProviderError,
                         EnvironmentNotFound, ProviderInteractionError)
from juju.providers.common.base import MachineProviderBase
from juju.providers.common.connect import ZookeeperConnect
from juju.providers.common.utils import get_user_authorized_keys

_XENAPI_VERSION = '1.1'

class MachineProvider(MachineProviderBase):
    """MachineProvider for XCP environment"""

    def __init__(self, environment_name, config):
        super(MachineProvider, self).__init__(environment_name, config)

        self._pool_master = config.get("pool-master")
        if not self._pool_master:
            return fail(ProviderError(
                "Cannot launch a machine without specifying a pool master"))

        self._user = config.get("master-username","root")
        self._pass = config.get("master-password","juju")

        # Create a new session
        self.server = xmlrpclib.ServerProxy(
            'http://%s' % self._pool_master)
        self.session = self.server.session.login_with_password(
            self._user, self._pass, _XENAPI_VERSION)

    @property
    def provider_type(self):
        return "xcp"

    def get_file_storage(self):
        """Retrieve the XCP FileStorage abstraction."""
        nfs_path = self.config.get("nfs-path")
        #return FileStorage(nfs_path)
        raise NotImplementedError()

    def start_machine(self, machine_data, master=False):
        """Start a machine in the provider.

        :param dict machine_data: desired characteristics of the new machine;
            it must include a "machine-id" key, and may include a "constraints"
            key to specify the underlying OS and hardware (where available).

        :param bool master: if True, machine will initialize the juju admin
            and run a provisioning agent, in addition to running a machine
            agent.
        """
        if "machine-id" not in machine_data:
            return fail(ProviderError(
                "Cannot launch a machine without specifying a machine-id"))
        machine_id = machine_data["machine-id"]
        constraints = machine_data.get("constraints", {})
        raise NotImplementedError()

    def get_machines(self, instance_ids=()):
        """List machines running in the provider.

        :param list instance_ids: ids of instances you want to get. Leave empty
            to list every :class:`juju.machine.ProviderMachine` owned by
            this provider.

        :return: a list of :class:`juju.machine.ProviderMachine` instances
        :rtype: :class:`twisted.internet.defer.Deferred`

        :raises: :exc:`juju.errors.MachinesNotFound`
        """
        raise NotImplementedError()

    def shutdown_machines(self, machines):
        """Terminate machines associated with this provider.

        :param machines: machines to shut down
        :type machines: list of :class:`juju.machine.ProviderMachine`

        :return: list of terminated :class:`juju.machine.ProviderMachine`
            instances
        :rtype: :class:`twisted.internet.defer.Deferred`
        """
        raise NotImplementedError()

    def open_port(self, machine, machine_id, port, protocol="tcp"):
        """Authorizes `port` using `protocol` for `machine`."""
        raise NotImplementedError()

    def close_port(self, machine, machine_id, port, protocol="tcp"):
        """Revokes `port` using `protocol` for `machine`."""
        raise NotImplementedError()

    def get_opened_ports(self, machine, machine_id):
        """Returns a set of open (port, protocol) pairs for `machine`."""
        raise NotImplementedError()
