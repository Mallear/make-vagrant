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
{% for port in forwarded_port %}
        anchore.vm.network :forwarded_port, guest: {{ port }}, host: {{ port }}
{% endfor %}
    end
end'''
)

@click.command()
@click.option('-d', '--distrib', help='Box distribution')
@click.option('-p', '--port', type=int, help='Ports to forward')
@click.option('--provider', help='Prodiver')
@click.option('-m', '--memory', type=int, help='Custom VM memory')
@click.option('-c', '--cpu', type=int, help='Custom VM CPU')
def init(distrib, port, provider, cpu, memory):
    '''Simple process to create Vagrant file from given distrib'''

    template_context = {
        'vagrantbox': vagrantbox[distrib],
        'forwarded_port': [port],
        'cpu': cpu,
        'memory': memory
    }

    with open('Vagrantfile', 'w') as f:
        f.write(vagrantfile.render(template_context))
        f.close()


if __name__ == '__main__':
    init()


