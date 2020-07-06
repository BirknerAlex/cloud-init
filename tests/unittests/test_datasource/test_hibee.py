# Author: Alexander Birkner <alexander.birkner@hibee.io>
#
# This file is part of cloud-init. See LICENSE file for license information.

from cloudinit.sources import DataSourceHiBee
import cloudinit.sources.helpers.hibee as bee_helper
from cloudinit import util

from cloudinit.tests.helpers import CiTestCase

METADATA = util.load_yaml("""{
  "id": "3f657fa2-7b72-466e-bad4-f83a31fbe5cd",
  "type": "BARE_METAL",  
  "fqdn": "server1",
  "region": "FRA01",
  "public_keys": [
    "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCdggAqqRKDj8X9ckZzJ0tB/r/VF6pD5JqP6c2/BHL9ctSae5TQClyOpSJdbp395MCjF3xOe89uK2MeOzUsYNMsTrwYPpFfpndnyAmY8Dc8L/iniqtFnHBCFS+z5VAx1mZNHdRS3NEhTkzPrt7PdmcJ1+cyfrUo9+w3kJMLuc3iyj5ZsoAp7anGtQKLCCxIL5fFCAQcYZR8w/AvLIj4B8sCb6Mon4TF9QhAJB1KbUhEwe3PY3tP1IkjYve9mKM6D5JF/b27ylRvliLLiq92LD/tBjJWjAaw92BqC3fa+Yfx9O+bCrNyP2yFX15L3/nbkppxmlZkk7aHuovkc3W6I5FlcbQfXMUjmMafdA/5Kmss5mgoq0q0E5nWhUu4L2NMW5VAkeTv+lsWLhj1vCo9JC3408mgiNaUn0XNq+uC4J6nXF/qYFNq5XvJPDsaxcxDBJip9dl9a/5BGbo6gAfORMJ1NTzpumKlEIoWZjk/TYVP7Za81UppUkk/n5x8spN70ZxoSIjQ8mXsY/GJ0uAycmy8UYH2hnDmNXiFFEh2E3iDwHYxUaoCVy/kwKBZc7kf1Rc3Fnf+Bt0PU2+k3msqBbpej3ZIoHGMdAaHpI6yYj6c60HC6PYClskkFufbGqyAtN6DcnDD3BthHS096BaTvwpIRRpyrYcPBs4gAccDbX//qw=="
  ],
  "interfaces": {
    "public": [
      {
        "ipv4": {
          "address": "176.57.186.5",
          "netmask": "255.255.255.0",
          "gateway": "176.57.186.1"
        },
        "mac": "40:9a:4c:8d:96:77",
        "type": "public"
      }
    ]
  },
  "dns": {
    "nameservers": [
      "8.8.8.8",
      "1.1.1.1"
    ]
  }
}""")

USERDATA = b"""#cloud-config
runcmd:
- [touch, /root/cloud-init-worked ]
"""


class TestDataSourceHiBee(CiTestCase):
    """
    Test reading the meta-data
    """
    def setUp(self):
        super(TestDataSourceHiBee, self).setUp()
        self.tmp = self.tmp_dir()
