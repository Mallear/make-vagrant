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

    config.vm.define 'default' do | default |
        default.vm.box='{{ vagrantbox_name }}'
{% if vagrantbox_version %}
        default.vm.box_version='{{ vagrantbox_version }}'
{% endif %}
        default.vm.provider 'virtualbox' do | v |
            v.memory={{ memory }}
            v.cpus={{ cpu }}
        end
{% if shell_script %}
        default.vm.provision "shell", path: '{{shell_script}}'
{% endif %}
{% if ansible_playbook %}
        default.vm.provision 'it', type: 'ansible' do | ansible |
            # ansible.verbose = 'vvv'
            ansible.playbook='{{ ansible_playbook }}'
        end
{% endif %}{% for machine_port, host_port in forwarded_port.items() %}
        default.vm.network :forwarded_port, guest: {{ machine_port }}, host: {{ host_port }}{% endfor %}
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
@click.option('-a', '--ansible', help='Ansible playbook for provisionning')
@click.option('-b', '--box', type=str, help='Vagrant box name')
@click.option('-c', '--cpu', type=int, default=2, help='Custom VM CPU - Default = 2')
@click.option('-d', '--distrib', help='Box configuration from configuration dictionnary - Used only if box parameter is not set')
@click.option('-m', '--memory', type=int, default=4096, help='Custom VM memory - Default = 4096')
@click.option('-p', '--port', help='Ports to forward - machine:host format', multiple=True)
@click.option('-s', '--shell', help='Shell script for provisionning')
@click.option('-v', '--version', help='Vagrant box version')
def init(ansible, box, distrib, port, cpu, memory, shell, version):
    '''Simple process to create Vagrant file from given distribution'''

    template_context = {
        'ansible_playbook': ansible,
        'cpu': cpu,
        'forwarded_port': ports_filter(list(port)),
        'memory': memory,
        'shell_script': shell,
        'vagrantbox_name': box if box else vagrantbox[distrib],
        'vagrantbox_version': version if box else vagrantbox[distrib],
    }

    with open('Vagrantfile', 'w') as f:
        f.write(vagrantfile.render(template_context))
        f.close()


if __name__ == '__main__':
    init()


