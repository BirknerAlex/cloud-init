# Author: Alexander Birkner <alexander.birkner@hibee.io>
#
# This file is part of cloud-init. See LICENSE file for license information.

from cloudinit import log as logging
from cloudinit import sources
from cloudinit import util

import cloudinit.sources.helpers.hibee as bee_helper

LOG = logging.getLogger(__name__)

BUILTIN_DS_CONFIG = {
    'metadata_url': 'http://169.254.169.254/metadata/v1.json',
}

class DataSourceHiBee(sources.DataSource):
    dsname = 'HiBee'

    # Available server types
    ServerTypeBareMetal = 'BARE_METAL'
    ServerTypeVirtual = 'VIRTUAL'

    def __init__(self, sys_cfg, distro, paths):
        sources.DataSource.__init__(self, sys_cfg, distro, paths)

        self.distro = distro
        self.metadata = dict()

        self.ds_cfg = util.mergemanydict([
            util.get_cfg_by_path(sys_cfg, ["datasource", "HiBee"], {}),
            BUILTIN_DS_CONFIG])

        self.metadata_address = self.ds_cfg['metadata_url']

        self.retries = self.ds_cfg.get('retries', 30)
        self.timeout = self.ds_cfg.get('timeout', 5)
        self.wait_retry = self.ds_cfg.get('wait_retry', 2)

        self._network_config = None
        self._server_type = None

    def _get_data(self):
        LOG.info("Running on HiBee")

        md = bee_helper.load_metadata(
            self.metadata_address, timeout=self.timeout,
            sec_between=self.wait_retry, retries=self.retries)

        self.metadata_full = md
        self.metadata['instance-id'] = md.get('id')
        self.metadata['local-hostname'] = md.get('fqdn')
        self.metadata['interfaces'] = md.get('interfaces')
        self.metadata['public-keys'] = md.get('public_keys')
        self.metadata['availability_zone'] = md.get('region', 'unknown')
        self.vendordata_raw = md.get("vendor_data", None)
        self.userdata_raw = md.get("user_data", None)
        self._server_type = md.get('type', self.ServerTypeBareMetal)

        LOG.debug("Detected server type %s", self._server_type)
        return True

    def check_instance_id(self, sys_cfg):
        # Currently we don't have a way on bare metal nodes
        # to detect if the instance-id matches.
        if self._server_type == self.ServerTypeBareMetal:
            return True

        return sources.instance_id_matches_system_uuid(self.get_instance_id())

    @property
    def network_config(self):
        if self._network_config:
            return self._network_config

        interfaces = self.metadata.get('interfaces')
        LOG.debug(interfaces)
        if not interfaces:
            raise Exception("Unable to get meta-data from server....")

        nameservers = self.metadata_full['dns']['nameservers']
        self._network_config = bee_helper.convert_network_configuration(
            interfaces, nameservers)
        return self._network_config


# Used to match classes to dependencies
datasources = [
    (DataSourceHiBee, (sources.DEP_FILESYSTEM, )),
]


# Return a list of data sources that match this set of dependencies
def get_datasource_list(depends):
    return sources.list_from_depends(depends, datasources)

# vi: ts=4 expandtab
