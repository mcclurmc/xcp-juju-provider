from twisted.internet.defer import inlineCallbacks, returnValue

from juju.errors import ProviderInteractionError
from juju.providers.common.launch import LaunchMachine


class XCPLaunchMachine(LaunchMachine):
    """XCP operation for launching an instance"""

    def start_machine(self, machine_id, zookeepers):
        """Actually launch a domain on an XCP pool.

        :param str machine_id: the juju machine ID to assign

        :param zookeepers: the machines currently running zookeeper, to which
            the new machine will need to connect
        :type zookeepers: list of :class:`juju.machine.ProviderMachine`

        :return: a singe-entry list containing a provider-specific
            :class:`juju.machine.ProviderMachine` representing the newly-
            launched machine
        :rtype: :class:`twisted.internet.defer.Deferred`
        """
        cloud_init = self._create_cloud_init(machine_id, zookeepers)
        cloud_init.set_provider_type("xcp")
        # TODO: determine policy for setting and getting instance id.
        # From the set_instance_id_accessor documentation, it seems
        # that we need a way to get the instance id from the machine
        # by running a shell script on it. The snippet below is from
        # the ec2 provider.
        cloud_init.set_instance_id_accessor(
            "$(curl http://169.254.169.254/1.0/meta-data/instance-id)")
        user_data = cloud_init.render()
        image_id = yield get_image_id(self._provider.config, self._constraints)

        raise NotImplementedError()

