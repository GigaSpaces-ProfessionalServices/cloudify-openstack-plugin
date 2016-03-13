#########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  * See the License for the specific language governing permissions and
#  * limitations under the License.

from cloudify import ctx
from cloudify.decorators import operation
from openstack_plugin_common import (
    with_neutron_client,
    is_external_relationship,
    OPENSTACK_ID_PROPERTY
)
from openstack_plugin_common.floatingip import (
    create_floatingip,
    delete_floatingip,
    floatingip_creation_validation
)


@operation
@with_neutron_client
def create(neutron_client, **kwargs):
    create_floatingip(neutron_client, None, kwargs)


@operation
@with_neutron_client
def delete(neutron_client, **kwargs):
    delete_floatingip(neutron_client)


@operation
@with_neutron_client
def creation_validation(neutron_client, **kwargs):
    floatingip_creation_validation(neutron_client, 'floating_ip_address')


@operation
@with_neutron_client
def connect_port(neutron_client, **kwargs):
    if is_external_relationship(ctx):
        return

    port_id = ctx.source.instance.runtime_properties[OPENSTACK_ID_PROPERTY]
    floating_ip_id = ctx.target.instance.runtime_properties[
        OPENSTACK_ID_PROPERTY]
    fip = {'port_id': port_id}
    neutron_client.update_floatingip(floating_ip_id, {'floatingip': fip})


@operation
@with_neutron_client
def disconnect_port(neutron_client, **kwargs):
    if is_external_relationship(ctx):
        ctx.logger.info('Not disassociating floatingip and port since '
                        'external floatingip and port are being used')
        return

    floating_ip_id = ctx.target.instance.runtime_properties[
        OPENSTACK_ID_PROPERTY]
    fip = {'port_id': None}
    neutron_client.update_floatingip(floating_ip_id, {'floatingip': fip})
