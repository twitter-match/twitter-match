import textwrap
from api import api
from api import consts


def make_class_name(API_NAME):
    
    class_name = ''.join(
        [elem.title() for elem in API_NAME.split('_')])
    
    return class_name


def make_doc_string(API_CONSTS):

    doc_string = '\nArgs:\n    session: An OAuth1 session.\n'
    for k, v in API_CONSTS['PARAMETERS'].items():
        descriptions = textwrap.wrap(
            '{}: {}'.format(k, v['description']), width=70)
        for idx, description in enumerate(descriptions):
            spaces = ' '*4 if idx == 0 else ' '*8
            doc_string += '{}{}\n'.format(spaces, description)
    return doc_string


def make_api_modules():
    
    for API_NAME, API_CONSTS in consts.APIS_CONSTS.items():

        if API_NAME.startswith('GET'):
            api_parent_class = api.GetAPI
        elif API_NAME.startswith('POST'):
            api_parent_class = api.PostAPI
        else:
            message = 'API_NAME must start with GET or POST.'
            raise ValueError(message)

        api_class_name = make_class_name(API_NAME)
        api_doc_string = make_doc_string(API_CONSTS)
        api_class = type(
            api_class_name, (api_parent_class,), {'__doc__': api_doc_string})
        globals()[API_NAME.lower()] = api_class(API_CONSTS)


make_api_modules()