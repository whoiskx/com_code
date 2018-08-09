import ssl
import json
import urllib2


output_file_name = 'accountkit_export.csv'
url_fmt = 'https://graph.accountkit.com/{version}/{app_id}/accounts/?access_token=AA|{app_id}|{app_secret}&limit={limit}'
header_string = 'ID, Phone, Email'
E_FAILED = 'failed'
E_RETRY = 'retry'

import argparse
def parse_args(parser):
    parser.add_argument('-a', '--appid', type=int, help='Your facebook application id', required=True)
    parser.add_argument('-s', '--appsecret', help='Your application secret', required=True)
    parser.add_argument('-l', '--limit', type=int, default=1000, help='Number of items per the page. Range 1 to 1000')
    parser.add_argument('-f', '--file', default=output_file_name, help='Name of the output file')
    parser.add_argument('-v', '--version', default='v1.3', help='Api version')
    return parser.parse_args()

import re
def verify_params(params):
    error_msg = ''
    if (params.limit < 1 or params.limit > 1000):
        error_msg = 'limit should be in the range 1-1000'
    elif (re.match(r'^v\d+\.\d+$', params.version) == None):
        error_msg = 'double check your api version number'
    return error_msg

def get_url_config(params):

    config = {
        'version':    params.version,
        'app_id':     params.appid,
        'app_secret': params.appsecret,
        'limit':      params.limit
    }
    return config

def get_json_attrs(jdata, *names):
    if (not jdata):
        raise Exception('empty json data')

    val = jdata
    for name in names:
        try:
            val = val[name]
            if (not val):
                return None
        except:
            return None
    return val

def get_request_data_in_csv_format(url):
    try:
        response = urllib2.urlopen(url, context=get_request_data_in_csv_format.gcontext)
    except urllib2.HTTPError as e:
        print 'HTTPError = ' + str(e.code)
        print e.read()
        raise Exception(E_RETRY)
    except urllib2.URLError as e:
        print 'URLError = ' + str(e.reason)
        raise Exception(E_FAILED)
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    try:
        json_resp = json.loads(response.read())
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    try:
        next_url = get_json_attrs(json_resp, 'paging', 'next')
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    data = json_resp['data']
    result = ''
    for ditem in data:
        try:
            acc_id = get_json_attrs(ditem, 'id')
            ph_num = get_json_attrs(ditem, 'phone', 'number');
            email = get_json_attrs(ditem, 'email', 'address');
            result = result + '{},{},{}\n'.format(acc_id, ph_num, email)
        except Exception as e:
            print e
            raise Exception(E_FAILED)

    return {
        'next_url': next_url,
        'csv_data': result
    }

def export_to_file(file, url):
    file.write(header_string + '\n')

    current_url = url
    retry = 0
    while current_url != None:
        try:
            print 'Quering url ' + current_url
            data = get_request_data_in_csv_format(current_url)

        except Exception as e:
            if (e[0] == E_RETRY and retry < 3):
                retry = retry + 1
                print 'retrying: ' + retry + ' with url ' + current_url
            else:
                raise Exception('abort')
        else:
            file.write(data['csv_data'])
            retry = 0
            current_url = data['next_url']

def main():
    parser = argparse.ArgumentParser()
    params = parse_args(parser)
    error_msg = verify_params(params)
    if (error_msg != ''):
        print 'ERROR:' + error_msg
        parser.print_help()
        return

    get_request_data_in_csv_format.gcontext = ssl.create_default_context()

    config = get_url_config(params)
    url = url_fmt.format(**config)
    try:
        file = open(params.file, 'w')
        print 'File opened for Write: ' + params.file
        try:
            export_to_file(file, url)
        except:
            print 'Could not export to a file'
    except:
        print 'Could not open file'
    else:
        print 'File closed'
        file.close();

if __name__ == "__main__":
    main()import ssl
import json
import urllib2


output_file_name = 'accountkit_export.csv'
url_fmt = 'https://graph.accountkit.com/{version}/{app_id}/accounts/?access_token=AA|{app_id}|{app_secret}&limit={limit}'
header_string = 'ID, Phone, Email'
E_FAILED = 'failed'
E_RETRY = 'retry'

import argparse
def parse_args(parser):
    parser.add_argument('-a', '--appid', type=int, help='Your facebook application id', required=True)
    parser.add_argument('-s', '--appsecret', help='Your application secret', required=True)
    parser.add_argument('-l', '--limit', type=int, default=1000, help='Number of items per the page. Range 1 to 1000')
    parser.add_argument('-f', '--file', default=output_file_name, help='Name of the output file')
    parser.add_argument('-v', '--version', default='v1.3', help='Api version')
    return parser.parse_args()

import re
def verify_params(params):
    error_msg = ''
    if (params.limit < 1 or params.limit > 1000):
        error_msg = 'limit should be in the range 1-1000'
    elif (re.match(r'^v\d+\.\d+$', params.version) == None):
        error_msg = 'double check your api version number'
    return error_msg

def get_url_config(params):

    config = {
        'version':    params.version,
        'app_id':     params.appid,
        'app_secret': params.appsecret,
        'limit':      params.limit
    }
    return config

def get_json_attrs(jdata, *names):
    if (not jdata):
        raise Exception('empty json data')

    val = jdata
    for name in names:
        try:
            val = val[name]
            if (not val):
                return None
        except:
            return None
    return val

def get_request_data_in_csv_format(url):
    try:
        response = urllib2.urlopen(url, context=get_request_data_in_csv_format.gcontext)
    except urllib2.HTTPError as e:
        print 'HTTPError = ' + str(e.code)
        print e.read()
        raise Exception(E_RETRY)
    except urllib2.URLError as e:
        print 'URLError = ' + str(e.reason)
        raise Exception(E_FAILED)
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    try:
        json_resp = json.loads(response.read())
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    try:
        next_url = get_json_attrs(json_resp, 'paging', 'next')
    except Exception as e:
        print e
        raise Exception(E_FAILED)

    data = json_resp['data']
    result = ''
    for ditem in data:
        try:
            acc_id = get_json_attrs(ditem, 'id')
            ph_num = get_json_attrs(ditem, 'phone', 'number');
            email = get_json_attrs(ditem, 'email', 'address');
            result = result + '{},{},{}\n'.format(acc_id, ph_num, email)
        except Exception as e:
            print e
            raise Exception(E_FAILED)

    return {
        'next_url': next_url,
        'csv_data': result
    }

def export_to_file(file, url):
    file.write(header_string + '\n')

    current_url = url
    retry = 0
    while current_url != None:
        try:
            print 'Quering url ' + current_url
            data = get_request_data_in_csv_format(current_url)

        except Exception as e:
            if (e[0] == E_RETRY and retry < 3):
                retry = retry + 1
                print 'retrying: ' + retry + ' with url ' + current_url
            else:
                raise Exception('abort')
        else:
            file.write(data['csv_data'])
            retry = 0
            current_url = data['next_url']

def main():
    parser = argparse.ArgumentParser()
    params = parse_args(parser)
    error_msg = verify_params(params)
    if (error_msg != ''):
        print 'ERROR:' + error_msg
        parser.print_help()
        return

    get_request_data_in_csv_format.gcontext = ssl.create_default_context()

    config = get_url_config(params)
    url = url_fmt.format(**config)
    try:
        file = open(params.file, 'w')
        print 'File opened for Write: ' + params.file
        try:
            export_to_file(file, url)
        except:
            print 'Could not export to a file'
    except:
        print 'Could not open file'
    else:
        print 'File closed'
        file.close();

if __name__ == "__main__":
    main()