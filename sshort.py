#!/usr/bin/python
import os
import optparse
import sys

"""
@summary: sshort - ssh connection helper 
@author: Dawid Lorenz, dawid@lorenz.co
"""

class SshortConnection():
    """
    A single connection entity object
    """
    name = None
    target = None
    extra_args = None
    
    def __init__(self, name, target, extra_args=None):
        self.name = name
        self.target = target
        self.extra_args = extra_args
        
    def execute(self):
        ssh = 'ssh'
        args = [ssh, self.target]
        if self.extra_args != None:
            args.extend(self.extra_args.split(' '))
        os.execvp(ssh, args)

class Storage():
    """
    Object managing persistence of connections within a storage file 
    which is located in $HOME/.sshort by default
    """
    storage_file = None
    connections = {}
    separator = '|'
    
    def __init__(self):
        home_dir = os.environ.get('HOME')
        self.storage_file = home_dir + '/.sshort'
        self.load_connections_from_storage()
        
    def load_connections_from_storage(self):
        """
        Reads connections from storage and loads into self.connections
        """
        if not os.path.exists(self.storage_file):
            return
        f = open(self.storage_file, 'r')
        self.connections = {}
        for line in f:
            params = line.strip('\n').split(self.separator)
            name = params[0]
            target = params[1]
            try:
                extra_args = params[2]
            except IndexError:
                extra_args = None
            connection = SshortConnection(name, target, extra_args)
            self.connections.update({name: connection})
        f.close()
        
    def add_connection_to_storage(self, connection):
        """
        Adds a connection to storage file
        """
        f = open(self.storage_file, 'a')
        # I bet conditional below can be really done in single line
        # (I'd use ternary operator in PHP here, btw)
        if connection.extra_args == None:
            extra_args = ''
        else:
            extra_args = connection.extra_args
        f.write(self.separator.join([connection.name, connection.target, extra_args]) + "\n")
        f.close()
            
    def reset_storage(self):
        """
        Rewrites all connections from self.connections into storage file
        """
        f = open(self.storage_file, 'w')    # Truncate storage file first
        f.close()
        for conn in self.connections.values():
            self.add_connection_to_storage(conn)
        
    def get(self, name):
        """
        Get connection by name
        """
        if not self.connections.has_key(name):
            raise NameError('Connection ' + name + ' has not been defined')
        return self.connections.get(name)
    
    def store(self, connection):
        """
        Store connection
        """
        if not self.connections.has_key(connection.name):
            self.add_connection_to_storage(connection)
            self.load_connections_from_storage()
    
    def remove(self, name):
        """
        Remove connection by name
        """
        if self.connections.has_key(name):
            self.connections.pop(name)
            self.reset_storage()
            self.load_connections_from_storage()

if __name__ == "__main__":
    # Setup option parser first
    parser = optparse.OptionParser("Usage: %prog NAME")
    
    group_create = optparse.OptionGroup(parser, 'Creating new sshort connection')
    group_create.add_option('-s', '--store',
                            dest='store',
                            help='name of sshort connection',
                            metavar="NAME")
    group_create.add_option('-t', '--target',
                            dest='target',
                            help='ssh connection target, ie. user@host.com')
    group_create.add_option('-p', '--params',
                            dest='target_extra_args',
                            help='optional ssh parameters for connection',
                            metavar="PARAMS")
    parser.add_option_group(group_create)
    
    group_remove = optparse.OptionGroup(parser, 'Removing sshort connection')
    group_remove.add_option('-r', '--remove',
                            dest='remove',
                            metavar='NAME')
    parser.add_option_group(group_remove)
    
    parser.add_option('-l', '--list', 
                      action="store_true", 
                      dest="listing", 
                      help='list all saved sshort connections')
    
    parser.add_option('-e', '--export', 
                      action="store_true", 
                      dest="export", 
                      help='export all connections into ~/.ssh/config friendly format')
    
    (params, args) = parser.parse_args()

    try:
        # Try executing a connection
        connection_name = args[0]
        connection = Storage().get(connection_name)
        sys.stdout.write('Executing connection %s\n' % connection.name)
        connection.execute()
    except NameError as e:
        # Display error if connection doesn't exist
        sys.stderr.write(e.message + "\n")
    except IndexError:
        # Handle parameters
        if params.listing != None:
            for conn in Storage().connections.values():
                # Another possibly lame, non-Python-fu conditional below 
                if conn.extra_args != '':
                    extra_args = conn.extra_args + ' '
                else:
                    extra_args = ''
                sys.stdout.write("%s: %s%s\n" % (conn.name, extra_args, conn.target))
        elif params.export != None:
            for conn in Storage().connections.values():
                h = conn.target.split('@')
                username = h[0]
                hostname = h[1]
                if conn.extra_args != '' and conn.extra_args.find('-p') != -1:
                    port = conn.extra_args.replace('-p', 'Port') + '\n'
                else:
                    port = ''
                sys.stdout.write("Host %s\nHostName %s\nUser %s\n%s\n" % (conn.name, hostname, username, port))
        elif params.store != None and params.target != None:
            name = params.store
            target = params.target
            extra_args = params.target_extra_args
            connection = SshortConnection(name, target, extra_args)
            Storage().store(connection)
            sys.stdout.write('Saved connection %s\n' % connection.name)
        elif params.remove != None:
            Storage().remove(params.remove)
            sys.stdout.write('Deleted connection %s\n' % params.remove)