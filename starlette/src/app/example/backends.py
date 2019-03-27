from enum import Enum
import ldap3
from starlette.authentication import BaseUser


class LDAPUser(BaseUser):

    def __init__(self, username: str) -> None:
        self.username = username
        self.config = {
            'LDAP_HOST': 'ldap',
            'LDAP_BASE_DN': 'dc=planetexpress,dc=com',
            'LDAP_ALWAYS_SEARCH_BIND': True,
            'LDAP_USER_DN': 'ou=people',
            'LDAP_USER_OBJECT_FILTER': '(objectclass=inetOrgPerson)',
            'LDAP_GROUP_DN': 'ou=people',
            'LDAP_GROUP_MEMBERS_ATTR': 'member',
            'LDAP_GROUP_OBJECT_FILTER': '(objectclass=Group)'
        }

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username


class AuthenticationResponseStatus(Enum):
    FAIL = False
    SUCCESS = True


class AuthenticationResponse:
    def __init__(
        self,
        status: AuthenticationResponseStatus = AuthenticationResponseStatus.FAIL,
        user_info: dict = None,
        user_id: str = None,
        user_dn: str = None,
        user_groups: list = None
    ):
        self.status = status
        self.user_info = user_info or {},
        self.user_id = user_id,
        self.user_dn = user_dn,
        self.user_groups = user_groups or []


class LDAPAuthentication:
    def __init__(self, config: dict = None):
        self.config = config or {}

        self._server_pool = ldap3.ServerPool(
            [],
            ldap3.FIRST,
            active=1,
            exhaust=10
        )

        self.init_servers()
        self.init_config()

    def init_servers(self):
        servers = list(self._server_pool)
        for s in servers:
            self._server_pool.remove(s)

    def init_config(self):
        self.config.setdefault('LDAP_PORT', 389)
        self.config.setdefault('LDAP_HOST', None)
        self.config.setdefault('LDAP_USE_SSL', False)
        self.config.setdefault('LDAP_READONLY', True)
        self.config.setdefault('LDAP_CHECK_NAMES', True)
        self.config.setdefault('LDAP_BIND_DIRECT_CREDENTIALS', False)
        self.config.setdefault('LDAP_BIND_DIRECT_PREFIX', '')
        self.config.setdefault('LDAP_BIND_DIRECT_SUFFIX', '')
        self.config.setdefault('LDAP_BIND_DIRECT_GET_USER_INFO', True)
        self.config.setdefault('LDAP_ALWAYS_SEARCH_BIND', False)
        self.config.setdefault('LDAP_BASE_DN', '')
        self.config.setdefault('LDAP_BIND_USER_DN', None)
        self.config.setdefault('LDAP_BIND_USER_PASSWORD', None)
        self.config.setdefault('LDAP_SEARCH_FOR_GROUPS', True)
        self.config.setdefault('LDAP_FAIL_AUTH_ON_MULTIPLE_FOUND', False)

        # Prepended to the Base DN to limit scope when searching for Users/Groups.
        self.config.setdefault('LDAP_USER_DN', '')
        self.config.setdefault('LDAP_GROUP_DN', '')

        self.config.setdefault('LDAP_BIND_AUTHENTICATION_TYPE', 'SIMPLE')

        # Ldap Filters
        self.config.setdefault('LDAP_USER_SEARCH_SCOPE', 'LEVEL')
        self.config.setdefault('LDAP_USER_OBJECT_FILTER', '(objectclass=person)')
        self.config.setdefault('LDAP_USER_LOGIN_ATTR', 'uid')
        self.config.setdefault('LDAP_USER_RDN_ATTR', 'uid')
        self.config.setdefault('LDAP_GET_USER_ATTRIBUTES', ldap3.ALL_ATTRIBUTES)

        self.config.setdefault('LDAP_GROUP_SEARCH_SCOPE', 'LEVEL')
        self.config.setdefault('LDAP_GROUP_OBJECT_FILTER', '(objectclass=group)')
        self.config.setdefault('LDAP_GROUP_MEMBERS_ATTR', 'uniqueMember')
        self.config.setdefault('LDAP_GET_GROUP_ATTRIBUTES', ldap3.ALL_ATTRIBUTES)
        self.config.setdefault('LDAP_ADD_SERVER', True)

        if self.config['LDAP_ADD_SERVER']:
            self.add_server(
                hostname=self.config['LDAP_HOST'],
                port=self.config['LDAP_PORT'],
                use_ssl=self.config['LDAP_USE_SSL']
            )

    def add_server(self, hostname, port, use_ssl, tls_ctx=None):
        if not use_ssl and tls_ctx:
            raise ValueError("Cannot specify a TLS context and not use SSL!")

        server = ldap3.Server(
            hostname,
            port=port,
            use_ssl=use_ssl,
            tls=tls_ctx
        )

        self._server_pool.add(server)

        return server

    def authenticate(self, username, password) -> AuthenticationResponse:
        if self.config.get('LDAP_BIND_DIRECT_CREDENTIALS'):
            result = self.authenticate_direct_credentials(username, password)

        elif not self.config.get('LDAP_ALWAYS_SEARCH_BIND') and \
                self.config.get('LDAP_USER_RDN_ATTR') == \
                self.config.get('LDAP_USER_LOGIN_ATTR'):
            # Since the user's RDN is the same as the login field, we can do a direct bind.
            result = self.authenticate_direct_bind(username, password)
        else:
            # We need to search the User's DN to find who the user is (and
            # their DN) so we can try bind with their password.
            result = self.authenticate_search_bind(username, password)

        return result

    def authenticate_direct_credentials(self, username, password) -> AuthenticationResponse:
        bind_user = '{}{}{}'.format(
            self.config.get('LDAP_BIND_DIRECT_PREFIX'),
            username,
            self.config.get('LDAP_BIND_DIRECT_SUFFIX')
        )
        connection = self._make_connection(
            bind_user=bind_user,
            bind_password=password,
        )

        response = AuthenticationResponse()
        try:
            connection.bind()
            response.status = AuthenticationResponseStatus.SUCCESS
            response.user_id = username

            if self.config.get('LDAP_BIND_DIRECT_GET_USER_INFO'):
                # User wants extra info about the bind
                user_filter = '({search_attr}={username})'.format(
                    search_attr=self.config.get('LDAP_USER_LOGIN_ATTR'),
                    username=username
                )
                search_filter = '(&{0}{1})'.format(
                    self.config.get('LDAP_USER_OBJECT_FILTER'),
                    user_filter,
                )

                connection.search(
                    search_base=self.full_user_search_dn,
                    search_filter=search_filter,
                    search_scope=getattr(ldap3, self.config.get('LDAP_USER_SEARCH_SCOPE')),
                    attributes=self.config.get('LDAP_GET_USER_ATTRIBUTES'),
                )

                if len(connection.response) == 0 or \
                        (self.config.get('LDAP_FAIL_AUTH_ON_MULTIPLE_FOUND') and len(connection.response) > 1):
                    # Don't allow them to log in.
                    pass
                else:

                    user = connection.response[0]
                    user['attributes']['dn'] = user['dn']
                    response.user_info = user['attributes']
                    response.user_dn = user['dn']

        except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
            response.status = AuthenticationResponseStatus.FAIL
        except Exception:
            response.status = AuthenticationResponseStatus.FAIL

        self.destroy_connection(connection)
        return response

    def authenticate_direct_bind(self, username, password) -> AuthenticationResponse:
        bind_user = '{rdn}={username},{user_search_dn}'.format(
            rdn=self.config.get('LDAP_USER_RDN_ATTR'),
            username=username,
            user_search_dn=self.full_user_search_dn,
        )

        connection = self._make_connection(
            bind_user=bind_user,
            bind_password=password,
        )

        response = AuthenticationResponse()

        try:
            connection.bind()
            response.status = AuthenticationResponseStatus.SUCCESS
            # Get user info here.

            user_info = self.get_user_info(dn=bind_user, _connection=connection)
            response.user_dn = bind_user
            response.user_id = username
            response.user_info = user_info
            if self.config.get('LDAP_SEARCH_FOR_GROUPS'):
                response.user_groups = self.get_user_groups(dn=bind_user, _connection=connection)

        except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
            response.status = AuthenticationResponseStatus.FAIL
        except Exception:
            response.status = AuthenticationResponseStatus.FAIL

        self.destroy_connection(connection)
        return response

    def authenticate_search_bind(self, username, password) -> AuthenticationResponse:
        connection = self._make_connection(
            bind_user=self.config.get('LDAP_BIND_USER_DN'),
            bind_password=self.config.get('LDAP_BIND_USER_PASSWORD'),
        )

        try:
            connection.bind()
        except Exception:
            self.destroy_connection(connection)
            return AuthenticationResponse()

        # Find the user in the search path.
        user_filter = '({search_attr}={username})'.format(
            search_attr=self.config.get('LDAP_USER_LOGIN_ATTR'),
            username=username
        )
        search_filter = '(&{0}{1})'.format(
            self.config.get('LDAP_USER_OBJECT_FILTER'),
            user_filter,
        )

        connection.search(
            search_base=self.full_user_search_dn,
            search_filter=search_filter,
            search_scope=getattr(ldap3, self.config.get('LDAP_USER_SEARCH_SCOPE')),
            attributes=self.config.get('LDAP_GET_USER_ATTRIBUTES')
        )

        response = AuthenticationResponse()

        if len(connection.response) == 0 or \
                (self.config.get('LDAP_FAIL_AUTH_ON_MULTIPLE_FOUND') and len(connection.response) > 1):
            # Don't allow them to log in.
            pass

        else:
            for user in connection.response:
                # Attempt to bind with each user we find until we can find
                # one that works.

                if 'type' not in user or user.get('type') != 'searchResEntry':
                    # Issue #13 - Don't return non-entry results.
                    continue

                user_connection = self._make_connection(
                    bind_user=user['dn'],
                    bind_password=password
                )

                try:
                    user_connection.bind()
                    response.status = AuthenticationResponseStatus.SUCCESS

                    # Populate User Data
                    user['attributes']['dn'] = user['dn']
                    response.user_info = user['attributes']
                    response.user_id = username
                    response.user_dn = user['dn']
                    if self.config.get('LDAP_SEARCH_FOR_GROUPS'):
                        response.user_groups = self.get_user_groups(dn=user['dn'], _connection=connection)
                    self.destroy_connection(user_connection)
                    break

                except ldap3.core.exceptions.LDAPInvalidCredentialsResult:
                    response.status = AuthenticationResponseStatus.FAIL
                except Exception:  # pragma: no cover
                    # This should never happen, however in case ldap3 does ever
                    # throw an error here, we catch it and log it
                    response.status = AuthenticationResponseStatus.FAIL

                self.destroy_connection(user_connection)

        self.destroy_connection(connection)
        return response

    def get_user_groups(self, dn, group_search_dn=None, _connection=None):
        connection = _connection
        if not connection:
            connection = self._make_connection(
                bind_user=self.config.get('LDAP_BIND_USER_DN'),
                bind_password=self.config.get('LDAP_BIND_USER_PASSWORD')
            )
            connection.bind()

        safe_dn = ldap3.utils.conv.escape_filter_chars(dn)
        search_filter = '(&{group_filter}({members_attr}={user_dn}))'.format(
            group_filter=self.config.get('LDAP_GROUP_OBJECT_FILTER'),
            members_attr=self.config.get('LDAP_GROUP_MEMBERS_ATTR'),
            user_dn=safe_dn
        )

        connection.search(
            search_base=group_search_dn or self.full_group_search_dn,
            search_filter=search_filter,
            attributes=self.config.get('LDAP_GET_GROUP_ATTRIBUTES'),
            search_scope=getattr(ldap3, self.config.get('LDAP_GROUP_SEARCH_SCOPE'))
        )

        results = []
        for item in connection.response:
            if 'type' not in item or item.get('type') != 'searchResEntry':
                # Issue #13 - Don't return non-entry results.
                continue

            group_data = item['attributes']
            group_data['dn'] = item['dn']
            results.append(group_data)

        if not _connection:
            # We made a connection, so we need to kill it.
            self.destroy_connection(connection)

        return results

    def get_user_info(self, dn, _connection=None):
        return self.get_object(
            dn=dn,
            filter=self.config.get('LDAP_USER_OBJECT_FILTER'),
            attributes=self.config.get("LDAP_GET_USER_ATTRIBUTES"),
            _connection=_connection,
        )

    def get_user_info_for_username(self, username, _connection=None):
        ldap_filter = '(&({0}={1}){2})'.format(
            self.config.get('LDAP_USER_LOGIN_ATTR'),
            username,
            self.config.get('LDAP_USER_OBJECT_FILTER')
        )

        return self.get_object(
            dn=self.full_user_search_dn,
            filter=ldap_filter,
            attributes=self.config.get("LDAP_GET_USER_ATTRIBUTES"),
            _connection=_connection,
        )

    def get_group_info(self, dn, _connection=None):
        return self.get_object(
            dn=dn,
            filter=self.config.get('LDAP_GROUP_OBJECT_FILTER'),
            attributes=self.config.get("LDAP_GET_GROUP_ATTRIBUTES"),
            _connection=_connection,
        )

    def get_object(self, dn, filter, attributes, _connection=None):
        connection = _connection
        if not connection:
            connection = self._make_connection(
                bind_user=self.config.get('LDAP_BIND_USER_DN'),
                bind_password=self.config.get('LDAP_BIND_USER_PASSWORD')
            )
            connection.bind()

        connection.search(
            search_base=dn,
            search_filter=filter,
            attributes=attributes,
        )

        data = None
        if len(connection.response) > 0:
            data = connection.response[0]['attributes']
            data['dn'] = connection.response[0]['dn']

        if not _connection:
            # We made a connection, so we need to kill it.
            self.destroy_connection(connection)

        return data

    @property
    def connection(self):
        connection = self._make_connection(
            bind_user=self.config.get('LDAP_BIND_USER_DN'),
            bind_password=self.config.get('LDAP_BIND_USER_PASSWORD')
        )
        connection.bind()
        return connection

    def make_connection(self, bind_user=None, bind_password=None, **kwargs):
        return self._make_connection(bind_user, bind_password, **kwargs)

    def _make_connection(self, bind_user=None, bind_password=None, **kwargs):
        authentication = ldap3.ANONYMOUS
        if bind_user:
            authentication = getattr(ldap3, self.config.get('LDAP_BIND_AUTHENTICATION_TYPE'))

        connection = ldap3.Connection(
            server=self._server_pool,
            read_only=self.config.get('LDAP_READONLY'),
            user=bind_user,
            password=bind_password,
            client_strategy=ldap3.SYNC,
            authentication=authentication,
            check_names=self.config['LDAP_CHECK_NAMES'],
            raise_exceptions=True,
            **kwargs
        )

        return connection

    def destroy_connection(self, connection):
        connection.unbind()

    @property
    def full_user_search_dn(self):
        return self.compiled_sub_dn(self.config.get('LDAP_USER_DN'))

    @property
    def full_group_search_dn(self):
        return self.compiled_sub_dn(self.config.get('LDAP_GROUP_DN'))

    def compiled_sub_dn(self, prepend):
        prepend = prepend.strip()
        if prepend == '':
            return self.config.get('LDAP_BASE_DN')

        return '{prepend},{base}'.format(
            prepend=prepend,
            base=self.config.get('LDAP_BASE_DN')
        )
