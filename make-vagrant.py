# -*- coding: utf-8 -*-
import click
from jinja2 import Template


# List of box ordered by distribution
vagrantbox = {
    'amazonlinux2': {
        'name': 'moonphase/amazonlinux2',
        'version': '2017.12.0.20171212.2'
    },
    'centos7': {
        'name': 'centos/7',
        'version': '1802.01'
    },
    'debian8': {
        'name': 'debian/jessie64',
        'version': '8.10.0'
    }
}


# Vagrant file template
vagrantfile = Template(
'''Vagrant.configure('2') do | config |

    config.vm.define 'default' do | anchore |
        anchore.vm.box='{{ vagrantbox_name }}'
{% if vagrantbox_version %}
        anchore.vm.box_version='{{ vagrantbox_version }}'
{% endif %}
        anchore.vm.provider 'virtualbox' do | v |
            v.memory={% if memory %}{{ memory }}{% else %}4096{% endif %}
            v.cpus={% if cpu %}{{ cpu }}{% else %}2{% endif %}
        end
{% if provider == 'ansible' %}
        anchore.vm.provision 'it', type: 'ansible' do | ansible |
            # ansible.verbose = 'vvv'
            ansible.playbook='playbook.yml'
        end
{% endif %}{% for machine_port, host_port in forwarded_port.items() %}
        anchore.vm.network :forwarded_port, guest: {{ machine_port }}, host: {{ host_port }}{% endfor %}
    end
end'''
)


def ports_filter(forwarded_ports):
    machine_port = []
    host_port = []
    for port in forwarded_ports:
        link = port.split(':')
        machine_port.append(link[0])
        host_port.append(link[1])

    port_link = dict(zip(machine_port, host_port))
    return port_link


@click.command()
@click.option('-b', '--box', type=str, help='Vagrant box name')
@click.option('-c', '--cpu', type=int, help='Custom VM CPU')
@click.option('-d', '--distrib', help='Box configuration from configuration dictionnary - Used only if box parameter is not set')
@click.option('-m', '--memory', type=int, help='Custom VM memory')
@click.option('-p', '--port', help='Ports to forward - machine:host format', multiple=True)
@click.option('-v', '--version', help='Vagrant box version')
@click.option('--provision', help='Vagrant provisionner')
def init(box, distrib, port, provision, cpu, memory, version):
    '''Simple process to create Vagrant file from given distribution'''

    template_context = {
        'vagrantbox_name': box if box else vagrantbox[distrib],
        'vagrantbox_version': version if box else vagrantbox[distrib],
        'forwarded_port': ports_filter(list(port)),
        'cpu': cpu,
        'memory': memory
    }

    with open('Vagrantfile', 'w') as f:
        f.write(vagrantfile.render(template_context))
        f.close()


if __name__ == '__main__':
    init()


