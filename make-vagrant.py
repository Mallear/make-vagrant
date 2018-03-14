# -*- coding: utf-8 -*-
import click
from jinja2 import Template

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

vagrantfile = Template(
'''Vagrant.configure('2') do | config |

    config.vm.define 'default' do | anchore |
        anchore.vm.box='{{ vagrantbox.name }}'
        anchore.vm.box_version='{{ vagrantbox.version }}'

        anchore.vm.provider 'virtualbox' do | v |
            v.memory={% if memory %}{{ memory }}{% else %}4096{% endif %}
            v.cpus={% if cpu %}{{ cpu }}{% else %}2{% endif %}
        end
{% if provider == 'ansible' %}
        anchore.vm.provision 'it', type: 'ansible' do | ansible |
            # ansible.verbose = 'vvv'
            ansible.playbook='playbook.yml'
        end
{% endif %}
{% for machine_port, host_port in forwarded_port.items() %}
        anchore.vm.network :forwarded_port, guest: {{ machine_port }}, host: {{ host_port }}
{% endfor %}
    end
end'''
)


def ports_filter(forwarded_ports):
    machine_port = []
    host_port = []
    for port in forwarded_ports:
        link = port.split(":")
        print(link)
        machine_port = link[0]
        host_port = link[1]

    port_link = dict(zip([machine_port], [host_port]))
    print(port_link)
    return port_link


@click.command()
@click.option('-d', '--distrib', help='Box distribution')
@click.option('-p', '--port', help='Ports to forward')
@click.option('--provider', help='Prodiver')
@click.option('-m', '--memory', type=int, help='Custom VM memory')
@click.option('-c', '--cpu', type=int, help='Custom VM CPU')
def init(distrib, port, provider, cpu, memory):
    '''Simple process to create Vagrant file from given distrib'''

    template_context = {
        'vagrantbox': vagrantbox[distrib],
        'forwarded_port': ports_filter([port]),
        'cpu': cpu,
        'memory': memory
    }

    with open('Vagrantfile', 'w') as f:
        f.write(vagrantfile.render(template_context))
        f.close()


if __name__ == '__main__':
    init()


