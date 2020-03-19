import json
import hmac as HMAC
import hashlib
import requests
from urllib.parse import quote as urlencode

class MulticraftAPI:
    _key = ''
    _url = ''

    _lastResponse = ''

    _methods = {

        # User functions
        'listUsers': (),
        'findUsers': ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'getUser': ('id',),
        'updateUser': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}, {'name': 'send_mail', 'default': 0}),
        'createUser': ('name', 'email', 'password', {'name': 'lang', 'default': ''}, {'name': 'send_mail', 'default': 0}),
        'deleteUser': ('id',),
        'getUserRole': ('user_id', 'server_id'),
        'setUserRole': ('user_id', 'server_id', 'role'),
        'getUserFtpAccess':('user_id', 'server_id'),
        'setUserFtpAccess':('user_id', 'server_id', 'mode'),
        'getUserId': ('name',),
        'validateUser': ('name', 'password'),
        'generateUserApiKey': ('user_id',),
        'getUserApiKey': ('user_id',),
        'removeUserApiKey': ('user_id',),
        'getOwnApiKey': ('password', {'name': 'generate', 'default': 0}, {'name': 'gauth_code', 'default': ''}),

        # Player functions
        'listPlayers': ('server_id',),
        'findPlayers': ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'getPlayer': ('id',),
        'updatePlayer': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'createPlayer': ('server_id', 'name'),
        'deletePlayer': ('id',),
        'assignPlayerToUser':('player_id', 'user_id'),

        # Command functions
        'listCommands': ('server_id',),
        'findCommands': ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'getCommand': ('id',),
        'updateCommand': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'createCommand': ('server_id', 'name', 'role', 'chat', 'response', 'run'),
        'deleteCommand': ('id',),

        # Server functions
        'listServers': (),
        'findServers': ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'listServersByConnection': ('connection_id',),
        'listServersByOwner': ('user_id',),
        'getServer': ('id',),
        'updateServer': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'createServerOn': ({'name': 'daemon_id', 'default': 0}, {'name': 'no_commands', 'default': 0}, {'name': 'no_setup_script', 'default': 0}),
        'createServer': ({'name': 'name', 'default': ''}, {'name': 'port', 'default': 0}, {'name': 'base', 'default': ''}, {'name': 'players', 'default': 0}, {'name': 'no_commands', 'default': 0}, {'name': 'no_setup_script', 'default': 0}),
        'createAndConfigureServer': ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}, {'name': 'configField', 'type': 'array'}, {'name': 'configValue', 'type': 'array'}, {'name': 'no_commands', 'default': 0}, {'name': 'no_setup_script', 'default': 0}),
        'suspendServer': ('id', {'name': 'stop', 'default': 1}),
        'resumeServer': ('id', {'name': 'start', 'default': 1}),
        'deleteServer': ('id', {'name': 'delete_dir', 'default': 'no'}),
        'getServerStatus': ('id', {'name': 'player_list', 'default': 0}),
        'getServerOwner': ('server_id',),
        'setServerOwner': ('server_id', 'user_id', {'name': 'send_mail', 'default': 0}),
        'getServerConfig': ('id',),
        'updateServerConfig': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'startServerBackup': ('id',),
        'getServerBackupStatus': ('id',),
        'startServer': ('id',),
        'stopServer': ('id',),
        'restartServer': ('id',),
        'killServer': ('id',),
        'startAllServers': (),
        'stopAllServers': (),
        'restartAllServers': (),
        'killAllServers': (),
        'sendConsoleCommand': ('server_id', 'command'),
        'sendAllConsoleCommand': ('command',),
        'runCommand': ('server_id', 'command_id', {'name': 'run_for', 'default': 0}),
        'getServerLog': ('id',),
        'clearServerLog': ('id',),
        'getServerChat': ('id',),
        'clearServerChat': ('id',),
        'sendServerControl': ('id', 'command'),
        'getServerResources': ('id',),
        'moveServer': ('server_id', 'daemon_id'),
        'listServerPorts': ('id',),
        'addServerPort': ('id', {'name': 'port', 'default': 0}),
        'removeServerPort': ('id', 'port'),

        # Daemon functions
        'listConnections': (),
        'findConnections': ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'getConnection': ('id',),
        'removeConnection': ('id',),
        'getConnectionStatus': ('id',),
        'getConnectionMemory': ('id', {'name': 'include_suspended', 'default': 0}),
        'getStatistics': ({'name': 'daemon_id', 'default': 0}, {'name': 'include_suspended', 'default': 0}),

        # Settings functions
        'listSettings': (),
        'getSetting': ('key',),
        'setSetting': ('key', 'value'),
        'deleteSetting': ('key',),

        # Schedule functions
        'listSchedules': ('server_id',),
        'findSchedules': ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'getSchedule': ('id',),
        'updateSchedule': ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
        'createSchedule': ('server_id', 'name', 'ts', 'interval', 'cmd', 'status', 'for'),
        'deleteSchedule': ('id',),

        # Database functions
        'getDatabaseInfo': ('server_id',),
        'createDatabase': ('server_id',),
        'changeDatabasePassword': ('server_id',),
        'deleteDatabase': ('server_id',)
    }

    def __init__(self, url, username, api_key):
        self._url = url
        self.user = username
        self._key = api_key

    def __call__(self, function, *args):

        if function not in self._methods.keys():
            return {'success': False, 'errors': [f'Unknown API method "{function}()"'], 'data': []}

        argnames = self._methods[function]
        callargs = {}
        name = ''
        value = ''

        for c, v in enumerate(argnames):

            if isinstance(v, dict):
                name = v['name']
            else:
                name = v

            if  c < len(args):
                value = args[c]
            elif isinstance(v, dict) and 'default' in v.keys():
                if c >= len(args):
                    value = v['default']
                else:
                    value = args[c]
            else:
                return {'success': False, 'errors': [f'"{function}()": Not enough arguments ({len(args)})'], 'data': []}
            
            if isinstance(v, dict) and 'type' in v.keys():
                if v['type'] == 'array':
                    value = json.dumps(value)
            callargs[name] = value
        
        return self.call(function, callargs)

    def call(self, method, params = {}):

        if not self._url:
            return {'success': False, 'errors': ['Invalid target URL'], 'data': []}

        if not self._key:
            return {'success': False, 'errors': ['Invalid target URL'], 'data': []}
        
        url = self._url
        query = ''
        string = ''

        if not isinstance(params, dict):
            params = {params: params}
        
        params['_MulticraftAPIMethod'] = method
        params['_MulticraftAPIUser'] = self.user

        for k, v in params.items():
            string += k + str(v)
            query += f'&{urlencode(k)}={urlencode(str(v))}'
        
        hmac = HMAC.new(bytes(self._key, 'utf-8'), digestmod=hashlib.sha256)
        hmac.update(string.encode(encoding="UTF-8"))
        params['_MulticraftAPIKey'] = hmac.hexdigest()

        ret = self.send(url, params)
        if isinstance(ret, dict) and len(ret['errors']) > 0 and ret['errors'][0] == 'Invalid API key.': # This is an old panel, use MD5 method instead
            md5 = hashlib.md5()
            md5.update(self._key+"".join(params.values()))
            params['_MulticraftAPIKey'] = md5.hexdigest()
            ret = self.send(url, params)
        return ret
    
    def send(self, url, params):
        r = requests.get(url, params=params, headers={"user-agent":"Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
        try:
            return r.json()
        except:
            return {'success': False, 'errors': ['Received invalid response, contact module\'s author'], 'data': []}
