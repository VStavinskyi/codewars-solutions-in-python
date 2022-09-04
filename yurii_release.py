import jenkins
import xml.etree.ElementTree as ET

# CREATE NEW VIEW WITH NEW JOBS FOR NEW RELEASE

# constants
JENKINS_ADDRESS = "MY_JENKINS"
USERNAME = "admin"
PW = "<>" # API TOKEN

# global vars
VIEW_NAME = "<>" # name of the previous view

# connector to Jenkins
class My_Jenkins():
    def __init__(self, host, username, api_token):
        self.host = host
        self.username = username
        self.api_token = api_token
        self.server = jenkins.Jenkins(self.host, username=username, password=api_token)
        self.user = self.server.get_whoami()
        self.version = self.server.get_version() 

        print(f"Jenkins '{self.host}' version {self.version}. Logged in with '{self.user['fullName']}' username")
    
    def get_view_config_by_name(self, view_name):
        if self.server.view_exists(view_name):
            return self.server.get_view_config(view_name)

# save job/view/folder config to local file
def save_config(config_as_string, filename):
    f = open(f"{filename}.xml", "w")
    f.write(config_as_string)
    f.close()

# for new object config have to be updated
def update_config(filename):
    # use ET
    pass

#######################################################################

J = My_Jenkins(JENKINS_ADDRESS, USERNAME, PW)

# lets create a view (tab) for new release
old_release_view_config = J.get_view_config_by_name(VIEW_NAME) # get old config
save_config(old_release_view_config, VIEW_NAME) # save it locally

print(old_release_view_config) # debug line - delete later
