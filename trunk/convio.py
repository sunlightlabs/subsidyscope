import httplib
import json
from collections import namedtuple
from itertools import izip, imap
from copy import deepcopy
from urllib2 import urlopen, HTTPError
from urllib import urlencode 
from failure import Success, Failure

class ConvioApiError(Exception):
    pass

ConvioServerMethod = namedtuple(
    'ConvioServerMethod',
    'name endpoint http_method'
)

class ConvioClient(object):
    VERSION = '1.0'
    METHOD_ENDPOINTS = [
        ConvioServerMethod('getUser', 'SRConsAPI', 'POST'),
        ConvioServerMethod('create', 'SRConsAPI', 'POST'),
        ConvioServerMethod('update', 'SRConsAPI', 'POST'),
        ConvioServerMethod('getUserGroups', 'SRConsAPI', 'POST'),
        ConvioServerMethod('getGroupInfo', 'SRGroupAPI', 'POST')
    ]
    METHOD_ENDPOINTS = dict(izip(imap(lambda m: m.name, METHOD_ENDPOINTS),
                                 METHOD_ENDPOINTS))

    def __init__(self, api_key, login_name, login_password, url_base=None):
        self.url_base = url_base
        self.api_key = api_key
        self.login_name = login_name
        self.login_password = login_password

    # Generic HTTP plumbing
    def call(self, method_name, param_dict):
        try:
            method = self.METHOD_ENDPOINTS[method_name]
        except KeyError:
            raise ConvioApiError("Unsupported method {0}".format(method_name))
        params = deepcopy(param_dict)
        params['method'] = method_name
        params['login_name'] = self.login_name
        params['login_password'] = self.login_password
        params['api_key'] = self.api_key
        params['response_format'] = 'json'
        params['v'] = self.VERSION
        data = urlencode(params)
        try:
            if method.http_method == 'GET':
                url = "{0}/{1}?{2}".format(self.url_base, 
                                           method.endpoint,
                                           data)
                response = urlopen(url)
            else:
                url = "{0}/{1}".format(self.url_base,
                                       method.endpoint)
                response = urlopen(url, data=data)
            return Success(json.load(response))

        except HTTPError, httperr:
            if httperr.code == httplib.FORBIDDEN:
                error_response = json.load(httperr)["errorResponse"]
                return Failure(error_response)

        except ValueError, err:
            # probably a JSON parsing error
            return Failure(err)

    # Methods corresponding to a server-side method
    def getUser(self, cons_id=None, member_id=None, primary_email=None):
        """Pass-through call to the remote method of the same name."""
        assert (cons_id, member_id, primary_email) != (None, None, None)
        params = {}
        if cons_id is not None:
            params['cons_id'] = cons_id
        if member_id is not None:
            params['member_id'] = member_id
        if primary_email is not None:
            params['primary_email'] = primary_email
        (response, error) = self.call('getUser', params)
        if error:
            return Failure(error)
        else:
            result = response["getConsResponse"]
            constituent = Constituent(cons_id=result["cons_id"],
                            member_id=result["member_id"],
                            primary_email=result["email"]["primary_address"])
            return Success(constituent)

    def create(self, primary_email):
        """Pass-through call to the remote method of the same name."""
        (response, error) = self.call('create', 
                                      {'primary_email': primary_email})
        if error:
            return Failure(error)
        else:
            return Success(response["createConsResponse"]["cons_id"])

    def update(self, cons_id, **kwargs):
        """Pass-through call to the remote method of the same name."""
        params = deepcopy(kwargs)
        params["cons_id"] = cons_id
        (response, error) = self.call('update', params)
        if error:
            return Failure(error)
        else:
            result = response["updateConsResponse"]
            if result["message"] == "User updated.":
                return Success(result["cons_id"])

    def getGroupInfo(self, group_id):
        """Pass-through call to the remote method of the same name."""
        assert group_id is not None
        (response, error) = self.call('getGroupInfo', 
                                  {'group_id': group_id})
        if error:
            return Failure(error)
        else:
            group_info = response["getGroupInfoResponse"]["groupInfo"]
            group = Group(group_id=int(group_info["id"]), 
                          name=group_info["name"])
            return Success(group)

    def getUserGroups(self, cons_id):
        """Pass-through call to the remote method of the same name."""
        assert cons_id is not None
        (response, error) = self.call('getUserGroups', {'cons_id': cons_id})
        if error:
            return Failure(error)
        else:
            result = response["getConsGroupsResponse"]
            group_from_dict = lambda d: Group(int(d["id"]), d["label"])
            if result == {}:
                return Success([])

            elif type(result["group"]) is dict:
                return Success([group_from_dict(result["group"])])

            elif type(result["group"]) is list:
                group_dicts = result["group"]
                return Success([group_from_dict(grp) 
                                for grp in group_dicts])
            else:
                return Failure("Unrecognized response body: {0}".format(
                               repr(response)))

    # Convenience methods wrapping the actual server-side API methods
    def constituent(self, cons_id=None, member_id=None, primary_email=None):
        """Returns a constituent matching the given criteria. If any of
        the supplied fields matches but not all of them match, an 
        exception is thrown. If none of these three fields match any 
        constituent and a primary_email value was given, then a 
        new constituent is created and returned."""

        (c, error) = self.getUser(cons_id, 
                                  member_id, 
                                  primary_email)
        if error and primary_email:
            (c, error) = self.create(primary_email=primary_email)
            if error:
                raise ConvioApiError(error)

            return self.constituent(cons_id=cons_id,
                                    member_id=member_id,
                                    primary_email=primary_email)

        if cons_id is not None and cons_id != c.cons_id:
            raise ConvioApiError("cons_id<{0}> != c.cons_id<{1}>".format(
                                 cons_id, c.cons_id))

        if member_id is not None and member_id != c.member_id:
            raise ConvioApiError("member_id<{0}> != c.member_id<{1}>".format(
                                 member_id, c.member_id))

        if primary_email is not None and primary_email.lower() != c.primary_email.lower():
            # Convio apparently lower-cases all email addresses when they are imported.
            raise ConvioApiError("primary_email<{0!r}> != c.primary_email<{1!r}>".format(
                                 primary_email, c.primary_email))

        c.bind(self)
        return c

    def group(self, group_id, name=None):
        """Returns the group for the given group_id. If a name value is 
        passed in and the name of the group corresponding to the group_id
        is different, an API exception is raised. If no group exists with
        the given group_id, an API exception is raised."""
        (g, error) = self.getGroupInfo(group_id)
        if error:
            raise ConvioApiError(error)

        elif name is not None and name != g.name:
            return Failure("name<{0}> != g.name<{1}>".format(
                name, g.name))

        g.bind(self)
        return g

    def memberships(self, cons_id):
        (groups, error) = self.getUserGroups(cons_id)
        if error:
            return Failure(error)
        else:
            for g in groups:
                g.bind(self)
            return Success(groups)


class Constituent(object):
    def __init__(self, cons_id, member_id, primary_email):
        self.client = None
        self.cons_id = cons_id
        self.member_id = member_id
        self.primary_email = primary_email

    def __eq__(self, other):
        if self.cons_id != other.cons_id:
            return False
        elif self.member_id != other.member_id:
            return False
        elif self.primary_email != other.primary_email:
            return False
        else:
            return True

    def __repr__(self):
        return "<Constituent({0})>".format(self.cons_id)

    def bind(self, client):
        self.client = client

    def is_member_of(self, group):
        if isinstance(group, Group):
            g = group
        elif type(group) in (int, long):
            g = self.client.group(group_id=group)
        elif type(group) in (str, unicode):
            g = self.client.group(group_id=int(group))
        else:
            raise ConvioApiError("group was not one of Group, int, long, or a numeric string.")

        (memberships, error) = self.client.memberships(self.cons_id)
        if error:
            raise ConvioApiError(error)
        else:
            return g in memberships

    def add_to_group(self, group):
        params = {'add_group_ids': str(group.group_id)}
        (cons_id1, error) = self.client.update(self.cons_id, **params)
        if error:
            raise ConvioApiError(error)

class Group(object):
    def __init__(self, group_id, name):
        self.client = None
        self.group_id = group_id
        self.name = name
 
    def __repr__(self):
        return "<Group({0}, {1})>".format(self.group_id, self.name)

    def __contains__(self, constituent):
        if isinstance(constituent, Constituent):
            return constituent.is_member_of(self)
        else:
            return False

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False

        if self.name is not None and other.name is not None and self.name != other.name:
            return False
        return self.group_id == other.group_id

    def bind(self, client):
        self.client = client


