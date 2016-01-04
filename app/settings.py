"""
This file is used to configure application settings.

Do not import this file directly.

You can use the settings API via:

    from ferris import settings

    mysettings = settings.get("mysettings")

The settings API will load the "settings" dictionary from this file. Anything else
will be ignored.

Optionally, you may enable the dynamic settings plugin at the bottom of this file.
"""

settings = {}

settings['timezone'] = {
    'local': 'US/Eastern'
}

settings['email'] = {
    # Configures what address is in the sender field by default.
    'sender': None
}

settings['app_config'] = {
    'webapp2_extras.sessions': {
        # WebApp2 encrypted cookie key
        # You can use a UUID generator like http://www.famkruithof.net/uuid/uuidgen
        'secret_key': '9a788030-837b-11e1-b0c4-0800200c9a66',
    },
    'webapp2_extras.auth': {
        'user_model': 'plugins.custom_auth.models.user.User',
        'user_attributes': ['email'],
    }
}

settings['oauth2'] = {
    # OAuth2 Configuration should be generated from
    # the google cloud console (Credentials for Web Application)
    'client_id': None,  # XXXXXXXXXXXXXXX.apps.googleusercontent.com
    'client_secret': None,
    'developer_key': None  # Optional
}

settings['oauth2_service_account'] = {
    # OAuth2 service account configuration should be generated
    # from the google cloud console (Service Account Credentials)
    'client_email': None,  # XXX@developer.gserviceaccount.com
    'private_key': None,  # Must be in PEM format
    'developer_key': None  # Optional
}


#Facebook Login
# get your own consumer key and consumer secret by registering at https://developers.facebook.com/apps
#Very Important: set the site_url= your domain in the application settings in the facebook app settings page
# callback url must be: http://[YOUR DOMAIN]/login/facebook/complete
settings['fb_api_key'] = '1752596521627997'
settings['fb_secret'] = 'cf9236540880c94364c188f1c43f0f8e'

# Enable Federated login (OpenID and OAuth)
# Google App Engine Settings must be set to Authentication Options: Federated Login
settings['enable_federated_login'] = True

settings['social_providers'] = {
        'facebook': {'name': 'facebook', 'label': 'Facebook', 'uri': ''},
        #'myopenid': {'name': 'myopenid', 'label': 'MyOpenid', 'uri': 'myopenid.com'},
    }


# If true, it will write in datastore a log of every email sent
settings['log_email'] = False

# If true, it will write in datastore a log of every visit
settings['log_visit'] = False

# local
# settings['web'] = {"web":{"client_id":"387750085819-5eid7rok0df3bct6nbskjlout21o1gdq.apps.googleusercontent.com","project_id":"care-rental","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"08abKZNvJ8qXkJZUzZ6A4fNS","javascript_origins":["http://localhost:8080"]}}

# staging
settings['web'] = {"web":{"client_id":"387750085819-5eid7rok0df3bct6nbskjlout21o1gdq.apps.googleusercontent.com","project_id":"care-rental","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://accounts.google.com/o/oauth2/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"08abKZNvJ8qXkJZUzZ6A4fNS","javascript_origins":["care-rental.appspot.com"]}}


settings['provider.facebook'] = {
    'client_id': '1752596521627997',
    'client_secret': 'cf9236540880c94364c188f1c43f0f8e',
    'scope': 'email',
}




settings['upload'] = {
    # Whether to use Cloud Storage (default) or the blobstore to store uploaded files.
    'use_cloud_storage': True,
    # The Cloud Storage bucket to use. Leave as "None" to use the default GCS bucket.
    # See here for info: https://developers.google.com/appengine/docs/python/googlecloudstorageclient/activate#Using_the_Default_GCS_Bucket
    'bucket': None
}

# Enables or disables app stats.
# Note that appstats must also be enabled in app.yaml.
settings['appstats'] = {
    'enabled': False,
    'enabled_live': False
}

# Optionally, you may use the settings plugin to dynamically
# configure your settings via the admin interface. Be sure to
# also enable the plugin via app/routes.py.

#import plugins.settings

# import any additional dynamic settings classes here.

# import plugins.my_plugin.settings

# Un-comment to enable dynamic settings
#plugins.settings.activate(settings)


# get your own recaptcha keys by registering at http://www.google.com/recaptcha/
settings['captcha_public_key'] = "6LdKYRQTAAAAANT1G2wcvssO-S_F-GOf35uqKLRC"
settings['captcha_private_key'] = "6LdKYRQTAAAAADMRlYxoUN6eGn11SywlqT01WrrE"
