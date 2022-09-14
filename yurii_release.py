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

def update_config(filename, G, current_release):
    out_file = f"{filename}.xml"
    config_file = ET.parse(out_file)
    config_file_tree = config_file.getroot()

    for token in config_file_tree.iter('name'):
        # change invoke token
        name.text = "MY NEW VERSION"
    
    for script_body in config_file_tree.iter('script'):
        # get old pipeline script by tag
        script_body.text = G.get_job_script(filename, current_release)

    config_file.write(out_file)

    config_as_string = ""
    with open(out_file, 'r') as file:
        config_as_string = file.read()
    
    os.remove(out_file)

    # change shared lib
    config_as_string = config_as_string.replace("@Library('shared_lib') _", f"@Library('shared_lib@{current_release}') _")

    # change branch inside pipeline to git checkout by tag
    if "git credentialsId" in config_as_string:
        config_as_string = script_body_iter(config_as_string, current_release)
        
    return config_as_string

# Q.server.upsert_job(name=f"{prod_job['name']}", config_xml=release_job_config)

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
