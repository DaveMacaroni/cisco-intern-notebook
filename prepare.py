#This logs into umbrella using umbrellalogin.py and creates a new tunnel based on information in addtunnel.py
from selenium import webdriver #Bot can do stuff in chrome
from time import sleep #Can pause so page can load and stuff
import pyperclip #Let's me paste stuff into txt file from clipboard
import os.path #So I can save tunnel id info in group_vars folder

from umbrellalogin import umbrella_username, umbrella_password #My umbrella login info
from addtunnel import tunnel_name, tunnel_id, tunnel_pwd #Tunnel info

class UmbrellaBot():
  def __init__(self):
    self.driver = webdriver.Chrome() #Open an empty browser

  def login(self): #Log into umbrella
    self.driver.get('https://login.umbrella.com/?_ga=2.27223029.918000454.1594230857-856797775.1594230857') #Umbrella login page
    sleep(3) #Wait 3 seconds for page to load
    
    umbrella_email_in = self.driver.find_element_by_xpath('//*[@id="username"]') #Umbrella login email
    umbrella_email_in.send_keys(umbrella_username) #Input umbrella email

    umbrella_pwd_in = self.driver.find_element_by_xpath('//*[@id="password"]') #Umbrella login password
    umbrella_pwd_in.send_keys(umbrella_password) #Input umbrella password

    umbrella_login_btn = self.driver.find_element_by_xpath('//*[@id="sign-in"]') #Login button
    umbrella_login_btn.click() #Click it

  def add_tunnel(self): #Add a tunnel
    sleep(3) #Wait because it takes a while for everything to load

    umbrella_deployments = self.driver.find_element_by_xpath('//*[@id="left"]/div/div[2]/div/div[1]/div[1]/ul/li[2]/div/div')
    umbrella_deployments.click() #Go to deployments

    umbrella_deployments_networktunnels = self.driver.find_element_by_xpath('//*[@id="left"]/div/div[2]/div/div[1]/div[1]/ul/li[2]/div/ul/li[1]/div/ul/li[6]/div/div')
    umbrella_deployments_networktunnels.click() #Go to network tunnels

    sleep(7) #Wait for add button to show

    add_tunnel = self.driver.find_element_by_xpath('//*[@id="react-header-container"]/div/div/div[3]/h1/div[2]/div/a/i')
    add_tunnel.click() #Click on add tunnel

    tunnel_name_in = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/input')
    tunnel_name_in.send_keys(tunnel_name) #Name the tunnel CHANGE IN ADDTUNNEL.PY WHENEVER DOING NEW TUNNELS

    device_type = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[2]/div/div[1]/div[2]/div[4]/button') #Click on device type drop down and select other
    device_type.click()
    device_type_other = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[2]/div/div[1]/div[2]/div[4]/ul/li[8]/button')
    device_type_other.click()

    save_tunnel_btn = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[2]/div/div[2]/div/div[2]/div/button[2]') #Save tunnel
    save_tunnel_btn.click()

    set_tunnel_id = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div/div[1]/div[3]/div[2]/div[1]/input')
    set_tunnel_id.send_keys(tunnel_id) #Alot of the same thing isn't it

    set_tunnel_pwd = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div/div[1]/input[1]') #Enter and confirm random password
    set_tunnel_pwd.send_keys(tunnel_pwd)
    set_tunnel_pwd_confirm = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div/div[1]/input[2]')
    set_tunnel_pwd_confirm.send_keys(tunnel_pwd)

    save_tunnel_btn_2 = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div/div[3]/div/div/div[2]/button') #Click the button
    save_tunnel_btn_2.click()

  def write_info(self): #Copy and write the id and passphrase and stuff to a new file that will be used by ipsec.conf template
    #Copy the new tunnel ID b/c it's different now
    tunnel_id_new = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div[1]/div/div/div/div[3]/div[1]/div[2]/span/span[1]/button/i') 
    tunnel_id_new.click() 
    a = pyperclip.paste() #Paste the copied new tunnel id into temp variable
    tunnel_info = os.path.expanduser('~/Documents/tests/autoipsec/group_vars/local') #Save the file in group_vars
    open(tunnel_info, 'w+').write('---\n' + 'tunnel_id: \"' + repr(a)[1:-1] + '\"' + '\ntunnel_pwd: \"' + tunnel_pwd + '\"' + '\ntunnel_name: \"' + tunnel_name + '\"') #Write tunnel name, id, and PSK to group_vars folder. Has to be written a specific way because it's YAML
    #repr(a)[1:-1] is done because pyperclip pastes something as an object and repr turn that into a string but it adds single quotes when it does and we need double quotes. [1:-1] just cuts off the endpoints which are in this case the single quotes.
    
    done_btn = self.driver.find_element_by_xpath('//*[@id="dashx-shim-content"]/div/div/div/div[3]/div/div[1]/div/div/div/div[4]/div/button') #Press done
    done_btn.click()

#Run the bot when you run the program
bot = UmbrellaBot()
bot.login()
sleep(5)
bot.add_tunnel()
sleep(5)
bot.write_info()
sleep(5)
bot.driver.quit()

